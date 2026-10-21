#!/usr/bin/env python3
"""Edit a Lifestyle Legends reel from a plan file, in the style of the reference reel.

Reference reel: "It's simple really" (instagram.com/reel/DZF3QURNzQw, 1.18M views,
51x the channel average). See series/lifestyle-legends/EDITING_STYLE.md.

A plan (JSON) lists the footage in order and what goes on top of it:

  sequence   talk clips (transcribed; mistakes and >1 s silences cut unless
             "cut": false) and b-roll clips (trimmed, natural sound kept),
             joined in order
  cutaways   full-screen b-roll laid over the talk at a spoken word; the
             voice keeps playing underneath
  popups     a screenshot, photo or clip shown as a card mid-frame at a word
  label      white box with black capitals over the opening seconds
             ("end" in seconds, or "until" a word)
  music      optional bed, ducked under the voice

Words are anchors: "at": "spearfish" starts at the first word that begins
with "spearfish", "swim#2" at the second "swim", a number at that second.

Usage:
  python3 edit_legend.py series/lifestyle-legends/plans/fleming_1_day_in_the_life.json
  python3 edit_legend.py PLAN [-o output/x.mp4] [--model medium] [--draft]

Requires ffmpeg and `pip install faster-whisper`. Proxima Nova Semibold in
./fonts, as for edit_video.py.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from boost_audio import boost
from edit_video import (FONTS_DIR, ROOT, ass_time, build_keep, check_font,
                        detect_silences, mark_mistakes, norm, remap, transcribe)

# --- Reference style ---------------------------------------------------------
W, H, FPS = 1080, 1920, 30
FONT_NAME = "Proxima Nova Semibold"
CAPTION_SIZE = 66             # px; matches the reference text width (~52% of frame for "and go for a swim")
CAPTION_Y = 0.50              # caption centre as a fraction of height: chest level
CAPTION_OUTLINE = 4           # px black stroke
CAPTION_MAX_WORDS = 4         # one short phrase on screen at a time
CAPTION_MAX_CHARS = 22
LABEL_SIZE = 66               # white box, black capitals
LABEL_Y = 0.38
LABEL_PAD = 24
POPUP_WIDTH = 0.8             # card width as a fraction of the frame
POPUP_Y = 0.60
CUTAWAY_SECONDS = 2.0
POPUP_SECONDS = 2.5
MUSIC_VOLUME = 0.12
# -----------------------------------------------------------------------------

CUT_FADE = 0.015
NORM_V = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"setsar=1,fps={FPS},format=yuv420p")
NORM_A = "aformat=sample_rates=48000:channel_layouts=stereo"
I_WORDS = {"i", "i'm", "i'll", "i've", "i'd"}


def ff(args):
    proc = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + args,
                          text=True, capture_output=True)
    if proc.returncode:
        sys.exit(f"ffmpeg failed:\n{proc.stderr}")


def probe(path, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    out = subprocess.run(cmd + ["-show_entries", entries, "-of", "csv=p=0", str(path)],
                         text=True, capture_output=True, check=True).stdout
    return out.strip()


def duration(path):
    return float(probe(path, "format=duration"))


def has_audio(path):
    return probe(path, "stream=index", "a") != ""


def is_image(path):
    return path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")


# --- 1. the sequence ---------------------------------------------------------
def build_sequence(plan, footage, model):
    """Return (segments, words, broll_texts) on the output timeline."""
    segments, words, texts, t = [], [], [], 0.0
    for item in plan["sequence"]:
        if "talk" in item:
            src = footage / item["talk"]
            dur = duration(src)
            print(f"Transcribing {src.name}...")
            raw = transcribe(src, model)
            if item.get("cut", True):
                drop = mark_mistakes(raw)
                keep, kept = build_keep(raw, drop, detect_silences(src, dur), dur)
            else:                      # keep the whole take (e.g. talk, then dive)
                drop, keep, kept = set(), [(0.0, dur)], raw
            for w in kept:
                s, e = remap(w["start"], keep), remap(w["end"], keep)
                if s is None and e is None:
                    continue
                s = s if s is not None else e
                e = e if e is not None else s + 0.2
                words.append({"text": w["text"], "start": t + s, "end": t + e})
            segments += [(src, a, b, item.get("sound", 1.0)) for a, b in keep]
            cut = [raw[i]["text"] for i in sorted(drop)]
            new_len = sum(b - a for a, b in keep)
            print(f"  {dur:.1f}s -> {new_len:.1f}s, dropped: {' '.join(cut) or 'nothing'}")
            t += new_len
        elif "broll" in item:
            src = footage / item["broll"]
            a = float(item.get("in", 0.0))
            b = float(item.get("out", duration(src)))
            segments.append((src, a, b, item.get("sound", 1.0)))
            if item.get("text"):
                texts.append((t, t + b - a, item["text"]))
            t += b - a
        else:
            sys.exit(f"sequence item needs 'talk' or 'broll': {item}")
    return segments, words, texts


def render_base(segments, out, draft):
    files = list(dict.fromkeys(src for src, *_ in segments))
    audio = {f: has_audio(f) for f in files}
    parts, labels = [], ""
    for i, (src, a, b, vol) in enumerate(segments):
        k, d = files.index(src), b - a
        parts.append(f"[{k}:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,{NORM_V}[v{i}];")
        if audio[src]:
            parts.append(f"[{k}:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,{NORM_A},"
                         f"volume={vol},afade=t=in:d={CUT_FADE},"
                         f"afade=t=out:st={max(0.0, d - CUT_FADE):.3f}:d={CUT_FADE}[a{i}];")
        else:
            parts.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{i}];")
        labels += f"[v{i}][a{i}]"
    graph = "".join(parts) + f"{labels}concat=n={len(segments)}:v=1:a=1[v][a]"
    inputs = [x for f in files for x in ("-i", str(f))]
    encode(inputs, graph, "[v]", "[a]", out, draft, crf=16)


def encode(inputs, graph, vlabel, alabel, out, draft, crf=18):
    script = out.with_suffix(".filtergraph.txt")
    script.write_text(graph)
    try:
        ff(inputs + ["-filter_complex_script", str(script), "-map", vlabel, "-map", alabel,
                     "-c:v", "libx264", "-preset", "ultrafast" if draft else "medium",
                     "-crf", str(28 if draft else crf), "-r", str(FPS),
                     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    finally:
        script.unlink(missing_ok=True)


# --- 2. anchors --------------------------------------------------------------
def find_word(at, words):
    """Index of the word where phrase `at` starts ('swim#2' = 2nd match)."""
    m = re.match(r"^(.*?)(?:#(\d+))?$", str(at).strip())
    toks = [norm(t) for t in m.group(1).split()]
    nth = int(m.group(2) or 1)
    seq = [norm(w["text"]) for w in words]
    for match in (lambda x, y: x == y, lambda x, y: x.startswith(y)):
        hits = [i for i in range(len(seq) - len(toks) + 1)
                if all(match(seq[i + j], toks[j]) for j in range(len(toks)))]
        if len(hits) >= nth:
            return hits[nth - 1]
    return None


def resolve(entry, words, total, default_len, kind):
    """(start, end) on the output timeline for a cutaway/popup, or None."""
    at = entry.get("at", 0)
    if isinstance(at, (int, float)):
        start = float(at)
    else:
        i = find_word(at, words)
        if i is None:
            print(f"WARNING: {kind} '{entry['file']}': word '{at}' not in the transcript, "
                  "skipped. Check the transcript printed below.", file=sys.stderr)
            return None
        start = words[i]["start"]
    if "until" in entry:
        j = find_word(entry["until"], words)
        end = words[j]["end"] if j is not None else start + default_len
    else:
        end = start + float(entry.get("seconds", default_len))
    end = min(end, total)
    return (start, end) if end - start > 0.1 else None


# --- 3. captions and label ---------------------------------------------------
def clean(word, sentence_start, keep_case):
    text = word.strip().rstrip(".,;:")
    bare = norm(text)
    if (sentence_start and bare not in I_WORDS and text not in keep_case
            and not (len(text) > 1 and text.isupper())):
        text = text[:1].lower() + text[1:]
    return text.replace("{", "(").replace("}", ")").replace("\\", "")


def caption_events(words, keep_case, hidden):
    chunks, cur, start_of_sentence = [], [], True
    for w in words:
        text = clean(w["text"], start_of_sentence, keep_case)
        start_of_sentence = bool(re.search(r"[.!?]$", w["text"].strip()))
        if cur and text.startswith("-"):      # whisper splits "euro-maxing" into two words
            cur[-1] = {**cur[-1], "clean": cur[-1]["clean"] + text, "text": w["text"],
                       "end": w["end"]}
            continue
        if cur:
            prev = cur[-1]
            length = len(" ".join(x["clean"] for x in cur)) + 1 + len(text)
            prev_text = prev["text"].strip()
            if (len(cur) >= CAPTION_MAX_WORDS or length > CAPTION_MAX_CHARS
                    or w["start"] - prev["end"] > 0.4
                    or re.search(r"[.!?]$", prev_text)
                    # a comma ends the phrase, but never leave one word flashing alone
                    or (re.search(r"[,;:]$", prev_text) and len(cur) >= 2)):
                chunks.append(cur)
                cur = []
        cur.append({**w, "clean": text})
    if cur:
        chunks.append(cur)

    events = []
    for n, chunk in enumerate(chunks):
        s, e = chunk[0]["start"], chunk[-1]["end"] + 0.3
        if n + 1 < len(chunks):
            nxt = chunks[n + 1][0]["start"]
            # hold the phrase until the next one unless there's a real pause
            e = nxt if nxt - chunk[-1]["end"] < 0.6 else min(e, nxt)
        for h0, h1 in hidden:              # captions step aside for popups
            if h0 <= s < h1:
                s = e
            elif s < h0 < e:
                e = h0
        if e - s > 0.05:
            events.append((s, e, " ".join(x["clean"] for x in chunk)))
    return events


def write_ass(path, captions, texts, label):
    cx = W // 2
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Caption,{FONT_NAME},{CAPTION_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,"
        f"&H80000000,0,0,0,0,100,100,0,0,1,{CAPTION_OUTLINE},1,5,60,60,0,1",
        f"Style: Label,{FONT_NAME},{LABEL_SIZE},&H00000000,&H00000000,&H00FFFFFF,"
        f"&H00FFFFFF,0,0,0,0,100,100,0,0,3,{LABEL_PAD},0,5,90,90,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    pos = f"{{\\an5\\pos({cx},{round(H * CAPTION_Y)})}}"
    for s, e, text in captions + texts:
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Caption,,0,0,0,,{pos}{text}")
    if label:
        text = label["text"].upper().replace("\n", "\\N")
        lpos = f"{{\\an5\\pos({cx},{round(H * label.get('y', LABEL_Y))})}}"
        lines.append(f"Dialogue: 1,{ass_time(float(label.get('start', 0)))},"
                     f"{ass_time(float(label.get('end', 3)))},Label,,0,0,0,,{lpos}{text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --- 4. compose --------------------------------------------------------------
def render_final(base, total, cutaways, popups, music, ass_path, out, draft):
    inputs, parts, k = ["-i", str(base)], [], 1
    v, mix = "[0:v]", []
    for n, (c, (t0, t1)) in enumerate(cutaways):
        src, d = c["file"], t1 - t0
        inputs += ["-i", str(src)]
        parts.append(f"[{k}:v]trim=start={c.get('in', 0)}:duration={d:.3f},"
                     f"setpts=PTS-STARTPTS+{t0:.3f}/TB,{NORM_V}[cv{n}];")
        parts.append(f"{v}[cv{n}]overlay=enable='between(t,{t0:.3f},{t1:.3f})':"
                     f"eof_action=pass[vc{n}];")
        v = f"[vc{n}]"
        if c.get("sound", 0) and has_audio(src):
            ms = round(t0 * 1000)
            parts.append(f"[{k}:a]atrim=start={c.get('in', 0)}:duration={d:.3f},"
                         f"asetpts=PTS-STARTPTS,{NORM_A},volume={c['sound']},"
                         f"adelay={ms}|{ms}[ca{n}];")
            mix.append(f"[ca{n}]")
        k += 1
    for n, (p, (t0, t1)) in enumerate(popups):
        src, d = p["file"], t1 - t0
        pw = round(W * p.get("width", POPUP_WIDTH) / 2) * 2
        b = int(p.get("border", 0))
        if is_image(src):
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", str(src)]
            head = f"[{k}:v]"
        else:
            inputs += ["-i", str(src)]
            head = f"[{k}:v]trim=start={p.get('in', 0)}:duration={d:.3f},"
        parts.append(f"{head}setpts=PTS-STARTPTS+{t0:.3f}/TB,fps={FPS},"
                     f"scale={pw - 2 * b}:-2,"
                     f"pad=iw+{2 * b}:ih+{2 * b}:{b}:{b}:color={p.get('border_color', 'black')},"
                     f"format=yuva420p[pv{n}];")
        y = p.get("y", POPUP_Y)
        parts.append(f"{v}[pv{n}]overlay=x=(main_w-overlay_w)/2:y={H * y:.0f}-overlay_h/2:"
                     f"enable='between(t,{t0:.3f},{t1:.3f})':eof_action=pass[vp{n}];")
        v = f"[vp{n}]"
        k += 1

    voice = "[0:a]"
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music["file"])]
        vol = music.get("volume", MUSIC_VOLUME)
        parts.append(f"[0:a]asplit=2[voice][sc];[{k}:a]{NORM_A},atrim=duration={total:.3f},"
                     f"volume={vol},afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[mraw];"
                     f"[mraw][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=400[m];")
        voice = "[voice]"
        mix.append("[m]")
        k += 1
    if mix:
        parts.append(f"{voice}{''.join(mix)}amix=inputs={1 + len(mix)}:duration=first:"
                     f"normalize=0[ao];")
    else:
        parts.append(f"{voice}anull[ao];")

    ass = str(ass_path).replace("\\", "/").replace(":", r"\:")
    fonts = str(FONTS_DIR).replace(":", r"\:")
    parts.append(f"{v}ass='{ass}':fontsdir='{fonts}'[vo]")
    encode(inputs, "".join(parts), "[vo]", "[ao]", out, draft)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--model", default="small",
                    help="whisper model size (tiny/base/small/medium/large-v3)")
    ap.add_argument("--draft", action="store_true", help="fast low-quality render for review")
    args = ap.parse_args()

    plan = json.loads(args.plan.read_text())
    footage = ROOT / plan.get("footage", "input")
    missing = [footage / f for f in
               [i.get("talk") or i.get("broll") for i in plan["sequence"]]
               + [c["file"] for c in plan.get("cutaways", []) + plan.get("popups", [])]
               + ([plan["music"]["file"]] if plan.get("music") else [])
               if not (footage / f).exists()]
    if missing:
        sys.exit("Missing footage:\n  " + "\n  ".join(str(m) for m in missing))

    out = args.output or ROOT / "output" / f"{args.plan.stem}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    check_font()

    segments, words, texts = build_sequence(plan, footage, args.model)
    base = out.with_name(f"{out.stem}_base.mp4")
    rough = out.with_name(f"{out.stem}_rough.mp4")
    print("Joining the sequence...")
    render_base(segments, base, args.draft)
    total = duration(base)

    cutaways, popups = [], []
    for kind, dest, default in (("cutaways", cutaways, CUTAWAY_SECONDS),
                                ("popups", popups, POPUP_SECONDS)):
        for entry in plan.get(kind, []):
            when = resolve(entry, words, total, default, kind[:-1])
            if when:
                dest.append(({**entry, "file": footage / entry["file"]}, when))
    hidden = [w for p, w in popups if p.get("hide_captions", True)]

    label = plan.get("label")
    if label and "until" in label:            # e.g. hide the label when "please" is said
        i = find_word(label["until"], words)
        label = {**label, "end": words[i]["start"] if i is not None else label.get("end", 3)}

    ass_path = out.with_suffix(".ass")
    keep_case = set(plan.get("keep_case", []))
    write_ass(ass_path, caption_events(words, keep_case, hidden), texts, label)
    music = ({**plan["music"], "file": footage / plan["music"]["file"]}
             if plan.get("music") else None)

    print("Compositing cutaways, popups and captions...")
    try:
        render_final(base, total, cutaways, popups, music, ass_path, rough, args.draft)
        print("Boosting audio...")
        boost(rough, out)
    finally:
        base.unlink(missing_ok=True)
        rough.unlink(missing_ok=True)

    print("\nEdited transcript (anchor words for cutaways/popups):")
    line, t0 = [], 0.0
    for w in words:
        if not line:
            t0 = w["start"]
        line.append(w["text"])
        if re.search(r"[.!?]$", w["text"]) or len(line) >= 12:
            print(f"  {t0:6.2f}s  {' '.join(line)}")
            line = []
    if line:
        print(f"  {t0:6.2f}s  {' '.join(line)}")
    for c, (a, b) in cutaways:
        print(f"Cutaway {c['file'].name}: {a:.2f}-{b:.2f}s")
    for p, (a, b) in popups:
        print(f"Popup   {p['file'].name}: {a:.2f}-{b:.2f}s")
    print(f"\nDone: {out}  ({total:.1f}s, captions: {ass_path})")


if __name__ == "__main__":
    main()
