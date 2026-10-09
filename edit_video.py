#!/usr/bin/env python3
"""Edit a talking-head video according to the house guidelines.

Guidelines:
  * Captions: Proxima Nova Semibold, white fill, 4px black stroke.
  * Cut out mistakes (filler words, stumbles and retaken lines).
  * Cut out any silence longer than 1 second.
  * Audio as loud as possible without clipping (see boost_audio.py).

Usage:
  python3 edit_video.py input/clip.mp4 [-o output/clip_edited.mp4] [--model small]

Requires ffmpeg and `pip install faster-whisper`. Put the Proxima Nova
Semibold font file (.otf/.ttf) in ./fonts.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

from boost_audio import boost

ROOT = Path(__file__).resolve().parent
FONTS_DIR = ROOT / "fonts"

# --- Guidelines --------------------------------------------------------------
FONT_NAME = "Proxima Nova Semibold"
FONT_COLOR = "&H00FFFFFF"     # white (ASS is &HAABBGGRR)
STROKE_COLOR = "&H00000000"   # black
STROKE_PX = 4
FONT_SIZE_PX = 70
WORDS_PER_CAPTION = 3       # words on screen at a time
MAX_SILENCE = 1.0             # seconds; any longer pause is cut
# -----------------------------------------------------------------------------

CUT_FADE = 0.015            # seconds of audio fade at every cut, stops pops
PAD = 0.12                    # breathing room kept around speech at each cut
SILENCE_DB = -35              # threshold for ffmpeg silencedetect
FILLERS = {"um", "uh", "uhm", "umm", "erm", "er", "ah", "hmm", "mm"}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=width,height:format=duration",
               "-of", "default=nw=1", str(path)]).stdout
    vals = dict(line.split("=") for line in out.split())
    return int(vals["width"]), int(vals["height"]), float(vals["duration"])


def transcribe(path, model_size):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segments, _ = model.transcribe(str(path), word_timestamps=True,
                                   vad_filter=False,
                                   initial_prompt="Um, uh, so, like, I mean...")
    words = []
    for seg in segments:
        for w in seg.words:
            words.append({"text": w.word.strip(), "start": w.start, "end": w.end})
    return words


def norm(text):
    return re.sub(r"[^a-z0-9']", "", text.lower())


def mark_mistakes(words):
    """Return the set of word indices to drop.

    - filler words (um, uh, ...)
    - immediate stutters ("I I think" -> "I think")
    - retakes: when a run of >=3 words is re-said shortly after, the speaker
      restarted the line, so everything from the first attempt up to the
      restart is dropped and the last take is kept.
    """
    drop = set()
    toks = [norm(w["text"]) for w in words]
    for i, t in enumerate(toks):
        if t in FILLERS or not t:
            drop.add(i)
        elif i + 1 < len(toks) and toks[i + 1] == t and len(t) > 0:
            drop.add(i)

    # retake detection runs on the words that survived the filler pass
    idx = [i for i in range(len(toks)) if i not in drop]
    seq = [toks[i] for i in idx]
    n = 3
    k = 0
    while k + n <= len(seq):
        gram = seq[k:k + n]
        restart = next((j for j in range(k + 1, min(k + 25, len(seq) - n + 1))
                        if seq[j:j + n] == gram), None)
        if restart is None:
            k += 1
            continue
        # drop the abandoned take (and anything said between, e.g. "sorry")
        drop.update(range(idx[k], idx[restart]))
        k = restart
    return drop


def detect_silences(path, duration):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af",
                          f"silencedetect=noise={SILENCE_DB}dB:d={MAX_SILENCE}",
                          "-f", "null", "-"], text=True,
                         capture_output=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    ends += [duration] * (len(starts) - len(ends))
    return list(zip(starts, ends))


def subtract(keep, cuts):
    out = []
    for a, b in keep:
        segs = [(a, b)]
        for c0, c1 in cuts:
            c0, c1 = c0 + PAD, c1 - PAD
            if c1 <= c0:
                continue
            nxt = []
            for s0, s1 in segs:
                if c1 <= s0 or c0 >= s1:
                    nxt.append((s0, s1))
                    continue
                if c0 > s0:
                    nxt.append((s0, c0))
                if c1 < s1:
                    nxt.append((c1, s1))
            segs = nxt
        out.extend(segs)
    return [(a, b) for a, b in out if b - a > 0.05]


def build_keep(words, drop, silences, duration):
    kept = [w for i, w in enumerate(words) if i not in drop]
    if not kept:
        keep = [(0.0, duration)]
    else:
        keep = []
        for w in kept:
            s, e = max(0.0, w["start"] - PAD), min(duration, w["end"] + PAD)
            if keep and s - keep[-1][1] <= MAX_SILENCE:
                keep[-1] = (keep[-1][0], max(keep[-1][1], e))
            else:
                keep.append((s, e))
    keep = subtract(keep, silences)
    return keep, kept


def remap(t, keep):
    """Map a source timestamp to the edited timeline (None if cut)."""
    offset = 0.0
    for a, b in keep:
        if a <= t <= b:
            return offset + (t - a)
        offset += b - a
    return None


def ass_time(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def write_captions(kept, keep, width, height, out_path):
    font_size = FONT_SIZE_PX
    # bottom-anchored, offset so the line sits centred in the lower third
    margin_v = round(height / 6 - font_size / 2)
    lines = [
        "[Script Info]", "ScriptType: v4.00+",
        f"PlayResX: {width}", f"PlayResY: {height}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{FONT_NAME},{font_size},{FONT_COLOR},{FONT_COLOR},"
        f"{STROKE_COLOR},&H00000000,0,0,0,0,100,100,0,0,1,{STROKE_PX},0,"
        f"2,{round(width * 0.08)},{round(width * 0.08)},{margin_v},1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text",
    ]
    timed = []
    for w in kept:
        s, e = remap(w["start"], keep), remap(w["end"], keep)
        if s is None and e is None:
            continue
        s = s if s is not None else e
        e = e if e is not None else s + 0.2
        timed.append((s, e, w["text"]))
    for k in range(0, len(timed), WORDS_PER_CAPTION):
        chunk = timed[k:k + WORDS_PER_CAPTION]
        start = chunk[0][0]
        end = timed[k + WORDS_PER_CAPTION][0] if k + WORDS_PER_CAPTION < len(timed) else chunk[-1][1]
        end = min(end, chunk[-1][1] + 0.6)
        text = " ".join(t for _, _, t in chunk).replace("{", "(").replace("}", ")")
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{text}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def check_font():
    files = [p for p in FONTS_DIR.glob("*") if p.suffix.lower() in (".otf", ".ttf")]
    for f in files:
        names = run(["fc-scan", "--format", "%{family}|%{fullname}\n", str(f)]).stdout
        if "proxima nova" in names.lower() and "semibold" in names.lower():
            return True
    print(f"WARNING: no Proxima Nova Semibold font found in {FONTS_DIR}. "
          "Captions will fall back to a default font. Add the .otf/.ttf file "
          "there and re-run.", file=sys.stderr)
    return False


def render(src, keep, ass_path, out):
    parts, labels = [], ""
    for i, (a, b) in enumerate(keep):
        parts.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];")
        fade_out = max(0.0, b - a - CUT_FADE)
        parts.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={CUT_FADE},afade=t=out:st={fade_out:.3f}:d={CUT_FADE}[a{i}];")
        labels += f"[v{i}][a{i}]"
    ass = str(ass_path).replace("\\", "/").replace(":", r"\:")
    fonts = str(FONTS_DIR).replace(":", r"\:")
    graph = ("".join(parts) + f"{labels}concat=n={len(keep)}:v=1:a=1[vc][ac];"
             f"[vc]ass='{ass}':fontsdir='{fonts}'[vo]")
    script = out.with_suffix(".filtergraph.txt")
    script.write_text(graph)
    try:
        run(["ffmpeg", "-y", "-hide_banner", "-i", str(src),
             "-filter_complex_script", str(script),
             "-map", "[vo]", "-map", "[ac]",
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    finally:
        script.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--model", default="small",
                    help="whisper model size (tiny/base/small/medium/large-v3)")
    args = ap.parse_args()

    out = args.output or ROOT / "output" / f"{args.input.stem}_edited.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    check_font()

    width, height, duration = probe(args.input)
    print("Transcribing...")
    words = transcribe(args.input, args.model)
    drop = mark_mistakes(words)
    silences = detect_silences(args.input, duration)
    keep, kept = build_keep(words, drop, silences, duration)

    removed = [words[i]["text"] for i in sorted(drop)]
    print(f"Dropped {len(removed)} mistake/filler words: {' '.join(removed)}")
    print(f"Silences > {MAX_SILENCE}s found: {len(silences)}")
    new_len = sum(b - a for a, b in keep)
    print(f"Duration {duration:.1f}s -> {new_len:.1f}s ({len(keep)} segments)")

    ass_path = out.with_suffix(".ass")
    write_captions(kept, keep, width, height, ass_path)
    print("Rendering...")
    rough = out.with_name(f"{out.stem}_rough{out.suffix}")
    render(args.input, keep, ass_path, rough)
    print("Boosting audio...")
    try:
        boost(rough, out)
    finally:
        rough.unlink(missing_ok=True)
    print(f"Done: {out}  (captions: {ass_path})")


if __name__ == "__main__":
    main()
