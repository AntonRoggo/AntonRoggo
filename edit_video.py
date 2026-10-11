#!/usr/bin/env python3
"""Edit a talking-head video according to the house guidelines.

Guidelines:
  * Captions: Proxima Nova Semibold, white fill, 4px black stroke.
  * Cut out mistakes (filler words, stumbles and retaken lines).
  * Cut out any silence longer than 1 second.
  * Audio as loud as possible without clipping (see boost_audio.py).

Usage:
  python3 edit_video.py input/clip.mp4 [-o output/clip_edited.mp4] [--model small] [--broll plan.json]

The first run writes <out>.timeline.json (words with times on the edited timeline). Pick
B-roll/action clips from broll/ for those moments, write a plan
[{"file": "input/broll/x.mov", "start": 3.2, "end": 5.0, "clip_in": 1.5}, ...] and re-run
with --broll; the transcript is cached so it isn't redone.

Requires ffmpeg and `pip install faster-whisper`. Put the Proxima Nova
Semibold font file (.otf/.ttf) in ./fonts.
"""
import argparse
import json
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
MAX_SILENCE = 1.0             # seconds; silences this long are found by ffmpeg silencedetect
MAX_PAUSE = 0.35              # any pause between words longer than this is cut (with a J-cut)
# -----------------------------------------------------------------------------

AUDIO_OVERLAP = 0.10        # at every cut the next clip's audio crossfades in over the last 0.1s of the previous one
J_CUT = 0.1                 # extra delay before the picture follows (picture cuts AUDIO_OVERLAP + J_CUT after the new audio starts)
CUT_FADE = 0.015            # seconds of audio fade at every cut, stops pops
PAD = 0.12                    # padding used when cutting out long silences
PAD_IN = 0.05                 # audio kept before the first word of a clip
PAD_OUT = 0.10                # audio kept after the last word of a clip (overlaps the next clip)
SILENCE_DB = -35              # threshold for ffmpeg silencedetect
FILLERS = {"um", "uh", "uhm", "umm", "erm", "er", "ah", "hmm", "mm"}


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def probe(path):
    """Output width, height and duration. Accounts for phone rotation; output is 1080p."""
    info = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                           "stream=width,height:stream_side_data=rotation:format=duration",
                           "-of", "json", str(path)]).stdout)
    st = info["streams"][0]
    w, h = st["width"], st["height"]
    rot = next((int(d.get("rotation", 0)) for d in st.get("side_data_list", []) if "rotation" in d), 0)
    if abs(rot) in (90, 270):
        w, h = h, w
    scale = 1920 / max(w, h)  # always deliver 1080x1920 (or 1920x1080), up- or downscaling
    w, h = int(round(w * scale / 2) * 2), int(round(h * scale / 2) * 2)
    return w, h, float(info["format"]["duration"])


def load_audio(path, sr=16000):
    """16 kHz mono float32 samples via ffmpeg (avoids PyAV version clashes in faster-whisper)."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-vn",
                          "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def transcribe(path, model_size, hint=""):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    segments, _ = model.transcribe(load_audio(path), word_timestamps=True,
                                   vad_filter=False,
                                   initial_prompt=("Um, uh, so, like, I mean... " + hint).strip())
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
        # A real retake is a short false start. If the first attempt is long or already
        # finished a sentence, it's deliberate repetition: keep it.
        span = [words[i]["text"] for i in idx[k:restart]]
        finished = sum(t.rstrip().endswith((".", "?", "!")) for t in span[:-1])
        if len(span) > 12 or finished >= 1:
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


def detect_pauses(path, min_pause=MAX_PAUSE):
    """Pauses in his speech, from the audio itself (word timestamps hide pauses, because the
    speech model stretches words over the silence after them). Loudness is measured on a
    noise-reduced copy so room noise doesn't count as talking."""
    import numpy as np
    from boost_audio import DENOISE_MODEL
    sr, hop = 16000, 320  # 20 ms frames
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-vn",
                          "-af", f"highpass=f=80,arnndn=m={DENOISE_MODEL}", "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    n = len(a) // hop
    db = 20 * np.log10(np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    quiet = db < np.percentile(db, 90) - 25  # 25 dB under his speaking level
    pauses, start = [], None
    for i, q in enumerate(np.append(quiet, False)):
        if q and start is None:
            start = i
        elif not q and start is not None:
            if (i - start) * hop / sr >= min_pause:
                pauses.append((start * hop / sr, i * hop / sr))
            start = None
    return pauses


def cut_pauses(keep, pauses):
    """Remove pauses from the kept ranges, leaving PAD_OUT after speech and PAD_IN before it."""
    return subtract(keep, [(a + PAD_OUT - PAD, b - PAD_IN + PAD) for a, b in pauses])


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
            s, e = max(0.0, w["start"] - PAD_IN), min(duration, w["end"] + PAD_OUT)
            if keep and s - keep[-1][1] <= MAX_PAUSE:
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
        offset += b - a - AUDIO_OVERLAP
    return None


def ass_time(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def caption_text(word):
    """Caption style: lowercase, no punctuation (hyphens become spaces)."""
    return re.sub(r"[^\w\s]", "", word.replace("-", " ").lower()).strip()


def caption_chunks(timed, max_words=WORDS_PER_CAPTION):
    """Group words into captions that never cross a sentence or phrase boundary.

    Each sentence/phrase (split at . ? ! , ; :) is cut into the fewest chunks of at most
    `max_words`, balanced so a 4-word phrase becomes 2+2 rather than 3+1.
    """
    phrases, cur = [], []
    for item in timed:
        cur.append(item)
        if item[2].rstrip().endswith((".", "?", "!", ",", ";", ":")):
            phrases.append(cur)
            cur = []
    if cur:
        phrases.append(cur)
    weak = {"a", "an", "the", "of", "to", "and", "in", "on", "at", "some", "like", "for", "with",
            "but", "or", "your", "my"}

    def score(sizes, ph):
        pen, i = 0.0, 0
        for size in sizes:
            last = caption_text(ph[i + size - 1][2])
            pen += 2.0 if last in weak else 0.0     # don't end a caption on a filler word
            pen += 0.5 * abs(size - len(ph) / len(sizes))
            pen += 1.5 if size == 1 and len(ph) > 1 else 0.0  # no orphaned single words
            i += size
        return pen

    def splits(n, parts):
        if parts == 1:
            return [[n]] if 1 <= n <= max_words else []
        return [[k] + rest for k in range(1, max_words + 1) for rest in splits(n - k, parts - 1)]

    chunks = []
    for ph in phrases:
        parts = -(-len(ph) // max_words)
        best = min(splits(len(ph), parts), key=lambda sz: score(sz, ph))
        i = 0
        for size in best:
            chunks.append(ph[i:i + size])
            i += size
    return chunks


def unremap(t, keep):
    """Edited-timeline time -> source time."""
    offset = 0.0
    for a, b in keep:
        if t <= offset + (b - a - AUDIO_OVERLAP):
            return a + (t - offset)
        offset += b - a - AUDIO_OVERLAP
    return keep[-1][1]


_face_model = None


def face_box(src, t, width, height):
    """Largest frontal face (x, y, w, h) in output pixels at source time t, or None."""
    global _face_model
    import cv2
    import numpy as np
    if _face_model is None:
        _face_model = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(src),
                          "-frames:v", "1", "-vf", f"scale={width}:{height}", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True).stdout
    if len(raw) != width * height:
        return None
    img = np.frombuffer(raw, dtype=np.uint8).reshape(height, width)
    faces = _face_model.detectMultiScale(img, scaleFactor=1.1, minNeighbors=6,
                                         minSize=(int(width * 0.12), int(width * 0.12)))
    if len(faces) == 0:
        return None
    return max(faces, key=lambda f: f[2] * f[3])


def caption_y(src, t_edit, keep, plan, width, height, font_size):
    """Vertical centre for a caption: middle of the frame, or just below the chin if the
    middle would cover his face. B-roll moments have no face to avoid."""
    centre = height / 2
    half = font_size * 0.65
    if src is None or any(b["start"] <= t_edit <= b["end"] for b in plan):
        return centre
    box = face_box(src, unremap(t_edit, keep), width, height)
    if box is None:
        return centre
    x, y, w, h = box
    chin = y + h * 1.12  # detector box stops around the mouth; chin sits a bit lower
    if centre + half < y or centre - half > chin:
        return centre
    return min(chin + half + 12, height * 0.85)


def write_captions(kept, keep, width, height, out_path, src=None, plan=()):
    font_size = FONT_SIZE_PX
    lines = [
        "[Script Info]", "ScriptType: v4.00+",
        f"PlayResX: {width}", f"PlayResY: {height}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{FONT_NAME},{font_size},{FONT_COLOR},{FONT_COLOR},"
        f"{STROKE_COLOR},&H00000000,0,0,0,0,100,100,0,0,1,{STROKE_PX},0,"
        f"5,{round(width * 0.06)},{round(width * 0.06)},0,1",
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
    chunks = caption_chunks(timed)
    events = []
    for k, chunk in enumerate(chunks):
        text = " ".join(t for t in (caption_text(w) for _, _, w in chunk) if t)
        if not text:
            continue
        start = chunk[0][0]
        nxt = chunks[k + 1][0][0] if k + 1 < len(chunks) else None
        end = nxt if nxt is not None and nxt - chunk[-1][1] < 0.6 else chunk[-1][1] + 0.3
        y = caption_y(src, (start + chunk[-1][1]) / 2, keep, plan, width, height, font_size)
        events.append([start, end, y, text])
    # keep the caption steady: within a run of nearby positions, use the lowest one
    for i in range(1, len(events)):
        if abs(events[i][2] - events[i - 1][2]) < 80 and events[i][0] - events[i - 1][1] < 0.3:
            events[i][2] = events[i - 1][2] = max(events[i][2], events[i - 1][2])
    for start, end, y, text in events:
        lines.append(f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,"
                     f"{{\\an5\\pos({width // 2},{round(y)})}}{text}")
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


MIN_FACE_GAP = 1.5   # never cut back to Anton for less than this between/after B-roll
MIN_BROLL = 0.8      # shortest B-roll shot worth showing
HOOK_SECONDS = 3.0   # the hook stays on his face: no B-roll before the first caption after this


def clip_duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)])
    return float(out.stdout.strip())


def snap_plan(plan, captions, total):
    """Make B-roll cut on words and never flash back to camera for a split second.

    `captions` is [(start_time, text)]. A plan entry can give times ("start"/"end", edited
    timeline seconds) or, preferably, words: "start_at": "and shoot" starts at the caption
    beginning with those words; "end_at": "lets do" ends where that caption starts
    ("end_at": "END" = end of video). Word anchors survive changes to the cut rules.

    - every B-roll start/end snaps to the nearest caption start (or the video end)
    - gaps shorter than MIN_FACE_GAP between clips, or before the end, are filled by
      running the earlier clip on
    - a clip that would run out before its slot ends starts earlier in the clip instead
    """
    if not plan:
        return []
    caption_starts = [t for t, _ in captions]
    marks = sorted(set(caption_starts) | {total})
    snap = lambda t: min(marks, key=lambda m: abs(m - t))

    def find(phrase, after):
        if phrase.upper() == "END":
            return total
        phrase = caption_text(phrase)
        for t, text in captions:
            if t >= after - 1e-6 and text.startswith(phrase):
                return t
        raise SystemExit(f"B-roll anchor not found in captions: '{phrase}'")

    resolved, cursor = [], 0.0
    for b in plan:
        b = dict(b)
        if "start_at" in b:
            b["start"] = find(b["start_at"], cursor)
        if "end_at" in b:
            b["end"] = find(b["end_at"], b["start"] + 0.01)
        cursor = b["start"]
        resolved.append(b)
    hook_end = min([t for t in caption_starts if t >= HOOK_SECONDS] or [total])
    out = []
    for b in sorted(resolved, key=lambda b: b["start"]):
        b = dict(b, start=snap(b["start"]), end=snap(b["end"]))
        if b["start"] < hook_end:  # keep the hook on camera
            b["start"] = hook_end
        if out and b["start"] < out[-1]["end"]:
            b["start"] = out[-1]["end"]
        if b["end"] - b["start"] >= MIN_BROLL:
            out.append(b)
    for i, b in enumerate(out):
        nxt = out[i + 1]["start"] if i + 1 < len(out) else total
        if nxt - b["end"] < MIN_FACE_GAP:
            b["end"] = nxt
    for b in out:
        length = clip_duration(b["file"])
        need = b["end"] - b["start"]
        if b.get("clip_in", 0) + need > length:
            b["clip_in"] = max(0.0, length - need - 0.05)
            if need > length:  # clip too short for the slot: freeze is worse than ending early
                b["end"] = b["start"] + length - 0.05
    return out


def broll_filters(plan, width, height, first_input, fps, total):
    """Picture with B-roll, built as back-to-back pieces of whole frames.

    The camera track [vc] is cut into the stretches between B-roll shots, every B-roll clip
    is conformed to the same frame rate and trimmed to an exact frame count, and everything
    is concatenated. Joins are frame-exact, so no frame of the camera shot can slip in.
    """
    import math
    # a caption appears on the first frame at/after its start time; cut the picture on that
    # same frame so B-roll and caption change together
    frame = lambda t: int(math.ceil(t * fps - 1e-6))
    total_f = int(round(total * fps))
    pieces, cursor = [], 0
    for b in plan:
        s, e = frame(b["start"]), min(frame(b["end"]), total_f)
        if s > cursor:
            pieces.append(("cam", cursor, s, None))
        if e > s:
            pieces.append(("broll", s, e, b))
        cursor = max(cursor, e)
    if cursor < total_f:
        pieces.append(("cam", cursor, total_f, None))
    cams = [p for p in pieces if p[0] == "cam"]
    chain = [f"[vc]fps={fps:.6f},split={len(cams)}" + "".join(f"[c{i}]" for i in range(len(cams))) + ";"
             if len(cams) > 1 else f"[vc]fps={fps:.6f}[c0];" if cams else "[vc]nullsink;"]
    labels, ci, bi = "", 0, 0
    for kind, s, e, b in pieces:
        if kind == "cam":
            chain.append(f"[c{ci}]trim=start_frame={s}:end_frame={e},setpts=PTS-STARTPTS[p{ci}c];")
            labels += f"[p{ci}c]"
            ci += 1
        else:
            n = first_input + bi
            cin = b.get("clip_in", 0)
            chain.append(f"[{n}:v]trim=start={cin:.3f},setpts=PTS-STARTPTS,fps={fps:.6f},"
                         f"tpad=stop_mode=clone:stop_duration=2,"
                         f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                         f"crop={width}:{height},setsar=1,"
                         f"trim=end_frame={e - s},setpts=PTS-STARTPTS[p{bi}b];")
            labels += f"[p{bi}b]"
            bi += 1
    chain.append(f"{labels}concat=n={len(pieces)}:v=1:a=0[vb];")
    return "".join(chain), "vb"


def jcut_video(keep, fps=30.0, j=J_CUT, overlap=AUDIO_OVERLAP):
    """Video in/out points for J-cuts.

    Audio segments are crossfaded with `overlap` seconds of overlap, so the next clip's
    sound starts while the previous clip is still finishing (no gap). The picture switches
    `overlap + j` seconds after the new audio starts. Inside each segment picture and sound
    come from the same source moment, so lips stay in sync.

    Cut points are placed on whole frames of the OUTPUT timeline, so frame rounding never
    accumulates into drift across many cuts.
    """
    frame = 1.0 / fps
    starts, t = [], 0.0          # audio start of each segment on the output timeline
    for a, b in keep:
        starts.append(t)
        t += b - a - overlap
    total = t + overlap
    cuts = [0.0] + [round((starts[i] + overlap + j) / frame) * frame for i in range(1, len(keep))]
    cuts.append(round(total / frame) * frame)
    out = []
    for i, (a, b) in enumerate(keep):
        vs = a + (cuts[i] - starts[i])
        ve = a + (cuts[i + 1] - starts[i])
        out.append((vs, ve))
    return out


def source_fps(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=avg_frame_rate", "-of", "default=nw=1:nk=1", str(path)]).stdout.split()[0]
    num, _, den = out.partition("/")
    return float(num) / float(den or 1)


def audio_join(n, overlap=AUDIO_OVERLAP):
    """Crossfade every cut: the next clip's audio overlaps the end of the previous one."""
    if n == 1:
        return "[a0]anull[ac];"
    chain, prev = [], "a0"
    for i in range(1, n):
        out = "ac" if i == n - 1 else f"x{i}"
        chain.append(f"[{prev}][a{i}]acrossfade=d={overlap}:c1=tri:c2=tri[{out}];")
        prev = out
    return "".join(chain)


def render(src, keep, ass_path, out, plan=(), size=None):
    """Render the edit. Each camera segment is cut to its own 1080p file first (exact frame
    counts, low memory even with 4K sources and many cuts), then the segments, B-roll and
    captions are put together with the crossfaded audio."""
    import tempfile
    fps = source_fps(src)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        tmp = Path(tmp)
        listing = []
        for i, (vs, ve) in enumerate(jcut_video(keep, fps)):
            frames = int(round((ve - vs) * fps))
            if frames <= 0:
                continue
            piece = tmp / f"seg{i:03d}.mp4"
            run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{vs:.4f}", "-i", str(src),
                 "-frames:v", str(frames), "-an",
                 "-vf", f"scale={size[0]}:{size[1]},setsar=1,fps={fps:.6f}",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(piece)])
            listing.append(f"file '{piece.name}'")
        (tmp / "list.txt").write_text("\n".join(listing) + "\n")
        alabels = "".join(
            f"[1:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(keep))
        ass = str(ass_path).replace("\\", "/").replace(":", r"\:")
        fonts = str(FONTS_DIR).replace(":", r"\:")
        total = sum(b - a for a, b in keep) - AUDIO_OVERLAP * (len(keep) - 1)
        over, last = broll_filters(plan, *size, 2, fps, total) if plan else ("", "vc")
        graph = (f"[0:v]setpts=PTS-STARTPTS[vc];" + alabels + audio_join(len(keep)) + over +
                 f"[{last}]ass='{ass}':fontsdir='{fonts}'[vo]")
        script = tmp / "graph.txt"
        script.write_text(graph)
        extra = sum([["-i", str(b["file"])] for b in plan], [])
        run(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
             "-i", str(src), *extra, "-filter_complex_script", str(script),
             "-map", "[vo]", "-map", "[ac]",
             "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--model", default="medium.en",
                    help="whisper model size (tiny/base/small/medium/large-v3)")
    ap.add_argument("--drop", action="append", default=[], metavar="START-END",
                    help="extra source-time range to cut (outtakes, asides), e.g. --drop 8.6-11.2")
    ap.add_argument("--hint", default="",
                    help="words/phrases to help transcription (names, slang), e.g. 'Mate, tallow, cheeky pint'")
    ap.add_argument("--keep", action="append", default=[], metavar="START-END",
                    help="source-time range to always keep, even if silent (e.g. the trick shot, a bite)")
    ap.add_argument("--broll", type=Path,
                    help="JSON list of {file, start, end, clip_in} overlays, times on the edited timeline")
    args = ap.parse_args()

    out = args.output or ROOT / "output" / f"{args.input.stem}_edited.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    check_font()

    width, height, duration = probe(args.input)
    cache = out.with_suffix(".words.json")
    if cache.exists():
        words = json.loads(cache.read_text())
        print(f"Using cached transcript {cache}")
    else:
        print("Transcribing...")
        words = transcribe(args.input, args.model, args.hint)
        cache.write_text(json.dumps(words))
    drop = mark_mistakes(words)
    manual = [tuple(float(v) for v in r.split("-")) for r in args.drop]
    for i, w in enumerate(words):
        if any(a <= (w["start"] + w["end"]) / 2 <= b for a, b in manual):
            drop.add(i)
    silences = detect_silences(args.input, duration)
    keep, kept = build_keep(words, drop, silences, duration)
    pauses = detect_pauses(args.input)
    keep = cut_pauses(keep, pauses)
    print(f"Pauses > {MAX_PAUSE}s cut: {len(pauses)}")
    forced = [tuple(float(v) for v in r.split("-")) for r in args.keep]
    if forced:
        merged = []
        for a, b in sorted(keep + forced):
            if merged and a <= merged[-1][1] + 0.05:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        keep = merged

    removed = [words[i]["text"] for i in sorted(drop)]
    print(f"Dropped {len(removed)} mistake/filler words: {' '.join(removed)}")
    print(f"Silences > {MAX_SILENCE}s found: {len(silences)}")
    new_len = sum(b - a for a, b in keep) - AUDIO_OVERLAP * (len(keep) - 1)
    print(f"Duration {duration:.1f}s -> {new_len:.1f}s ({len(keep)} segments)")

    ass_path = out.with_suffix(".ass")
    plan = json.loads(args.broll.read_text()) if args.broll else []
    if plan:
        timed = [(remap(w["start"], keep), remap(w["end"], keep), w["text"]) for w in kept]
        timed = [t for t in timed if t[0] is not None]
        captions = [(round(c[0][0], 3), " ".join(t for t in (caption_text(w) for _, _, w in c) if t))
                    for c in caption_chunks(timed)]
        total = sum(b - a for a, b in keep) - AUDIO_OVERLAP * (len(keep) - 1)
        plan = snap_plan(plan, captions, round(total, 3))
        out.with_suffix(".broll_final.json").write_text(json.dumps(plan, indent=1))
    write_captions(kept, keep, width, height, ass_path, args.input, plan)
    # transcript on the edited timeline, for planning B-roll
    timeline = [{"text": w["text"], "start": round(remap(w["start"], keep) or 0, 2),
                 "end": round(remap(w["end"], keep) or 0, 2)} for w in kept]
    out.with_suffix(".timeline.json").write_text(json.dumps(timeline, indent=0))
    if plan:
        print(f"Overlaying {len(plan)} B-roll/action clips")
    print("Rendering...")
    rough = out.with_name(f"{out.stem}_rough{out.suffix}")
    render(args.input, keep, ass_path, rough, plan, (width, height))
    print("Boosting audio...")
    try:
        boost(rough, out)
    finally:
        rough.unlink(missing_ok=True)
    print(f"Done: {out}  (captions: {ass_path})")


if __name__ == "__main__":
    main()
