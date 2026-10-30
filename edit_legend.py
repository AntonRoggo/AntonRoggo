#!/usr/bin/env python3
"""Edit a Lifestyle Legends reel from a plan file: split-screen storyteller style.

The style comes from the top story-about-a-famous-person reels on Sandcastles
(see series/lifestyle-legends/EDITING_STYLE.md). Reference video for the
layout: "Can you guess this footballer from the story of their career?"
(instagram.com/reel/DdjfzUURsA3, 12x its channel average).

Layout
  header   thin paper-coloured strip with the series tag
  top      the story visual: archive photo (slow zoom), clip or map, with a
           blue pill label naming the beat
  bottom   you, talking to camera
  seam     uppercase captions sitting on the line between the two, numbers
           and chosen words in yellow

A plan (JSON) lists your talk clips in order and the panels that go on top:

  sequence  talk clips (transcribed; fillers, retakes, >1 s silences cut
            unless "cut": false) and b-roll clips, joined in order.
            "in"/"out" (seconds) use just that part of a talk clip, so one
            line can be picked from a long take: {"talk": "a.mp4", "in": 12.0,
            "out": 15.5}. In/out snap to the nearest pause in the
            audio, and only fillers and long pauses are cut inside a
            picked line. Only the parts used are decoded.
  panels    each starts at a spoken word and holds until the next one:
              {"at": "fifteen", "file": "boat.jpg", "label": "OYSTER PIRATE"}
              {"at": "Namaste", "full": "talk"}        you, full screen
              {"at": "surf", "full": "surf.mp4"}       b-roll, full screen
            "censor": [x, y, w, h] pixelates part of a photo (fractions)
  title     {"text": "Following Cousteau\nalong the Riviera", "until": "1936"}
            big opening title (default 5 s)
  end_card  {"at": "follow", "title": "...", "sub": "..."} over the ending
  music     optional bed, ducked under the voice
  fix       caption corrections for words the transcript got wrong:
            [["i forgot those", "Affogatos"]]
  captions  {"style": "lower"} for small lowercase captions with no split
            screen styling (the quick "do this" reels); default is the
            uppercase seam captions above

Anchors: "swim" = first word starting with "swim", "swim#2" = the second,
a number = that many seconds in. Before the first panel you're full screen.

Usage:
  python3 edit_legend.py series/lifestyle-legends/plans/london_a_origin.json
  python3 edit_legend.py PLAN [-o output/x.mp4] [--model medium] [--draft] [--dry-run]

Requires ffmpeg and `pip install faster-whisper`. Proxima Nova Semibold in
./fonts, as for edit_video.py.
"""
import argparse
import functools
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from boost_audio import boost
from edit_video import (FILLERS, FONTS_DIR, ROOT, ass_time, build_keep, check_font,
                        detect_silences, load_audio, mark_mistakes, norm, remap, subtract,
                        transcribe, PAD)

# --- Reference style ---------------------------------------------------------
W, H, FPS = 1080, 1920, 30
HEADER_H = 96                 # paper strip with the series tag
PANEL_H = 806                 # story visual, ~42% of the frame
SEAM_Y = HEADER_H + PANEL_H   # captions sit on this line
BOTTOM_H = H - SEAM_Y         # talking head, ~53% of the frame
AROLL_CROP_Y = 0.12           # where the bottom crop starts in your full frame
HEADER_COLOR = "0xF1EEE7"
FONT_NAME = "Proxima Nova Semibold"
CAPTION_SIZE = 56             # uppercase, white, heavy black stroke
CAPTION_OUTLINE = 5
CAPTION_FULL_Y = 0.70         # caption height when you're full screen
CAPTION_MAX_WORDS = 4
CAPTION_MAX_CHARS = 20
ACCENT = "&H0000D4FF&"        # yellow for numbers and highlight words
PILL_SIZE = 46                # white capitals on a blue pill
PILL_COLOR = "&H00FE5A3D"     # #3D5AFE
TAG_SIZE = 32
TITLE_SIZE = 72               # opening title over the first seconds (footsteps format)
TITLE_Y = 0.14
ZOOM = 0.08                   # slow push on every photo (alternates in/out)
CENSOR_BLOCKS = 18            # pixel size of the "guess who" blur
MUSIC_VOLUME = 0.12
# caption looks: "legend" is the split-screen seam style, "lower" the small
# lowercase captions of the quick talk-to-camera reels
CAPTION_STYLES = {
    "legend": {"case": "upper", "size": CAPTION_SIZE, "outline": CAPTION_OUTLINE,
               "y": CAPTION_FULL_Y, "max_words": CAPTION_MAX_WORDS,
               "max_chars": CAPTION_MAX_CHARS, "accent_numbers": True},
    "lower": {"case": "lower", "size": 58, "outline": 3, "y": 0.63, "max_words": 3,
              "max_chars": 18, "accent_numbers": False},
}
# -----------------------------------------------------------------------------

CUT_FADE = 0.015
# picked lines ("in"/"out") are cut on the pauses in the audio, not on word
# times, which can be a few tenths of a second off
PAUSE_DB = -35                # quieter than this is a pause
PAUSE_MIN = 0.12              # shortest pause to snap to
SNAP_MAX = 0.6                # how far an in/out point may move to reach a pause
LEAD = 0.05                   # quiet kept before the first word of a line
TAIL = 0.07                   # and after the last
LONG_PAUSE = 0.4              # pauses longer than this inside a line are tightened
# where the picture cuts: up to SHIFT_MAX before or after the sound cut (an L
# or J cut), at the frame where you're looking into the lens, found with
# face tracking (pip install mediapipe, model in models/face_landmarker.task)
SHIFT_MAX = 0.3
FACE_MODEL = ROOT / "models" / "face_landmarker.task"
SIDE_OK = 0.25                # sideways eye score that still reads as "at the lens"
NORM_A = "aformat=sample_rates=48000:channel_layouts=stereo"


def cover(w, h, focus=0.5):
    """Fill w x h, cropping the overflow; focus 0 keeps the top, 1 the bottom."""
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
            f"crop={w}:{h}:(iw-{w})/2:(ih-{h})*{focus},setsar=1")


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


def encode(inputs, graph, vlabel, alabel, out, draft, crf=18, total=None):
    script = out.with_suffix(".filtergraph.txt")
    script.write_text(graph)
    extra = ["-t", f"{total:.3f}"] if total else []
    try:
        ff(inputs + ["-filter_complex_script", str(script), "-map", vlabel, "-map", alabel]
           + extra + ["-c:v", "libx264", "-preset", "ultrafast" if draft else "medium",
                      "-crf", str(28 if draft else crf), "-r", str(FPS), "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    finally:
        script.unlink(missing_ok=True)


# --- 1. your talk, joined ----------------------------------------------------
@functools.lru_cache(maxsize=None)
def words_for(src, model, start=0.0, end=None):
    """Transcript of a clip, or of start-end within it. Saved in
    output/.cache so re-cutting a plan skips transcription."""
    # a whole clip keeps every "um" for the retake and filler cuts; a picked
    # excerpt skips its silences first for steadier word times
    vad = end is not None
    real = src.resolve()
    st = real.stat()
    key = hashlib.sha1(f"{real}|{st.st_size}|{st.st_mtime}|{model}|{'vad' if vad else 'novad'}"
                       f"|{start}|{end}".encode()).hexdigest()[:12]
    saved = ROOT / "output" / ".cache" / f"{src.stem}_{key}.words.json"
    if saved.exists():
        return json.loads(saved.read_text())
    print(f"Transcribing {src.name}" + (f" {start:.1f}-{end:.1f}s" if end else "") + "...")
    words = transcribe(src, model, vad=vad, start=start, end=end)
    saved.parent.mkdir(parents=True, exist_ok=True)
    saved.write_text(json.dumps(words))
    return words


@functools.lru_cache(maxsize=None)
def silences_for(src):
    return detect_silences(src, duration(src))


@functools.lru_cache(maxsize=None)
def pauses_for(src):
    """Every pause of PAUSE_MIN or more in a clip's audio. The threshold rises
    above PAUSE_DB with the clip's background noise; when the noise is nearly
    as loud as you (wind, a busy street), there's no pause to trust and the
    cuts go on word times instead."""
    import numpy as np
    x = load_audio(src)
    x = x[: len(x) // 320 * 320].reshape(-1, 320)            # 20 ms blocks
    level = 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-9)
    floor, loud = np.percentile(level, [10, 95])
    if loud - floor < 15:
        return ()
    noise = max(PAUSE_DB, round(float(floor) + 8))
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(src), "-vn", "-af",
                          f"silencedetect=noise={noise}dB:d={PAUSE_MIN}",
                          "-f", "null", "-"], text=True, capture_output=True).stderr
    starts = [max(0.0, float(x)) for x in re.findall(r"silence_start: (-?[\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    ends += [duration(src)] * (len(starts) - len(ends))
    return tuple(zip(starts, ends))


def snap(a, b, pauses):
    """Move a picked line's in/out points into the pauses around it, so no
    word is clipped and only a breath of quiet is left at each end."""
    inside = [(s, e) for s, e in pauses if s <= a <= e]
    if inside:
        a = max(a, inside[0][1] - LEAD)
    else:
        prev = [(s, e) for s, e in pauses if e <= a and a - e <= SNAP_MAX]
        if prev:
            a = max(prev[-1][0], prev[-1][1] - LEAD)
    inside = [(s, e) for s, e in pauses if s <= b <= e]
    if inside:
        b = min(b, inside[0][0] + TAIL)
    else:
        nxt = [(s, e) for s, e in pauses if s >= b and s - b <= SNAP_MAX]
        if nxt:
            b = min(nxt[0][1], nxt[0][0] + TAIL)
    return a, b


def clip_ranges(ranges, a, b):
    out = [(max(x, a), min(y, b)) for x, y in ranges]
    return [(x, y) for x, y in out if y - x > 0.05]


def build_sequence(plan, footage, model):
    """Return (segments, words, broll_texts) on the output timeline."""
    segments, words, texts, t = [], [], [], 0.0
    for item in plan["sequence"]:
        if "talk" in item:
            src = footage / item["talk"]
            dur = duration(src)
            a = float(item.get("in", 0.0))
            b = min(float(item.get("out", dur)), dur)
            picked = "in" in item or "out" in item
            if picked:
                pauses = pauses_for(src)
                a, b = snap(a, b, pauses)
                a_sure, b_sure = (any(x <= t <= y for x, y in pauses) for t in (a, b))
                # transcribed on its own: on the whole clip, whisper can give
                # one take's words the times of the retake next to it
                every = words_for(src, model, round(max(0.0, a - (0.2 if a_sure else 0.6)), 2),
                                  round(min(dur, b + (0.2 if b_sure else 0.6)), 2))
                raw = [w for w in every if w["end"] > a + 0.05 and w["start"] < b - 0.05]
                # an in/out point that found no pause can sit inside a word:
                # widen to the whole word, stopping short of the next one
                if raw and not a_sure and raw[0]["start"] < a:
                    before = [w["end"] for w in every if w["end"] <= raw[0]["start"]]
                    a = max(raw[0]["start"] - LEAD, (before[-1] + 0.02) if before else 0.0)
                if raw and not b_sure and raw[-1]["end"] > b:
                    after = [w["start"] for w in every if w["start"] >= raw[-1]["end"]]
                    b = min(raw[-1]["end"] + TAIL, (after[0] - 0.02) if after else dur)
                # never replay the end of the line before from the same clip
                if segments and segments[-1][0] == src and segments[-1][1] < a < segments[-1][2]:
                    a = segments[-1][2]
            else:
                every = words_for(src, model)
            raw = [w for w in every if w["end"] > a + 0.05 and w["start"] < b - 0.05]
            if not item.get("cut", True):
                drop, keep, kept = set(), [(a, b)], raw
            elif picked:
                # a hand-picked line is already the right take, so only fillers
                # and long pauses go; retake detection would eat deliberate
                # repeats ("my whole year, but my whole year is...")
                drop = {i for i, w in enumerate(raw) if norm(w["text"]) in FILLERS}
                gaps = [(x, y) for x, y in pauses_for(src) if y - x > LONG_PAUSE and a < x and y < b]
                gaps += [(raw[i]["start"] - PAD, raw[i]["end"] + PAD) for i in drop]
                keep = clip_ranges(subtract([(a, b)], sorted(gaps)), a, b)
                kept = [w for i, w in enumerate(raw) if i not in drop]
            else:
                drop = mark_mistakes(raw)
                keep, kept = build_keep(raw, drop, silences_for(src), dur)
            for w in kept:
                s, e = remap(w["start"], keep), remap(w["end"], keep)
                if s is None and e is None:
                    continue
                s = s if s is not None else e
                e = e if e is not None else s + 0.2
                words.append({"text": w["text"], "start": t + s, "end": t + e})
            segments += [(src, a, b, item.get("sound", 1.0), True) for a, b in keep]
            cut = [raw[i]["text"] for i in sorted(drop)]
            new_len = sum(y - x for x, y in keep)
            print(f"  {src.name} {a:.1f}-{b:.1f}s -> {new_len:.1f}s, "
                  f"dropped: {' '.join(cut) or 'nothing'}")
            t += new_len
        elif "broll" in item:
            src = footage / item["broll"]
            a = float(item.get("in", 0.0))
            b = float(item.get("out", duration(src)))
            segments.append((src, a, b, item.get("sound", 1.0), False))
            if item.get("text"):
                texts.append((t, t + b - a, item["text"]))
            t += b - a
        else:
            sys.exit(f"sequence item needs 'talk' or 'broll': {item}")
    return segments, words, texts


@functools.lru_cache(maxsize=None)
def face_model():
    try:
        import mediapipe as mp
        from mediapipe.tasks.python import BaseOptions, vision
        return mp, vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(FACE_MODEL)),
            output_face_blendshapes=True, num_faces=1))
    except Exception as e:                       # no mediapipe/model: plain cuts
        print(f"  (no face tracking, cutting picture with sound: {e})")
        return None


def gaze_for(src, a, b):
    """How far you're looking away from the lens, one score (0-1) per frame
    from a to b. Cached, like the transcripts."""
    real = src.resolve()
    key = hashlib.sha1(f"{real}|{real.stat().st_mtime}|{a:.3f}|{b:.3f}|{FPS}".encode()).hexdigest()[:12]
    saved = ROOT / "output" / ".cache" / f"{src.stem}_{key}.gaze.json"
    if saved.exists():
        return json.loads(saved.read_text())
    fm = face_model()
    if fm is None:
        return None
    mp, lm = fm
    import numpy as np
    w, h = 360, 640
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, a):.3f}", "-t", f"{b - a:.3f}",
                          "-i", str(src), "-vf", f"{cover(w, h)},fps={FPS}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    scores = []
    for f in np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3):
        r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)))
        if not r.face_blendshapes:
            scores.append(1.0)
            continue
        d = {c.category_name: c.score for c in r.face_blendshapes[0]}
        side = max(d["eyeLookInLeft"] + d["eyeLookOutRight"],
                   d["eyeLookOutLeft"] + d["eyeLookInRight"]) / 2
        blink = (d["eyeBlinkLeft"] + d["eyeBlinkRight"]) / 2
        down = 0.0 if blink > 0.4 else (d["eyeLookDownLeft"] + d["eyeLookDownRight"]) / 2
        up = (d["eyeLookUpLeft"] + d["eyeLookUpRight"]) / 2
        away = (max(0.0, side - SIDE_OK) + max(0.0, down - 0.45) + max(0.0, up - 0.35)) / 0.2
        scores.append(round(min(1.0, away), 3))
    saved.write_text(json.dumps(scores))
    return scores


def picture_shift(prev, cur):
    """Seconds the picture cut moves from the sound cut between two talk
    pieces: negative cuts to the next piece early (L cut, hides a glance
    after your last word), positive holds the last piece (J cut, hides the
    look up before your first word). Picks the frames where you're at the lens."""
    (p, _, pb, *_), (q, qa, *_) = prev, cur
    n = round(SHIFT_MAX * FPS)
    gp = gaze_for(p, pb - SHIFT_MAX, pb + SHIFT_MAX)
    gq = gaze_for(q, qa - SHIFT_MAX, qa + SHIFT_MAX)
    if not gp or not gq or qa - SHIFT_MAX < 0:
        return 0.0
    gp, gq = (gp + [1.0] * 2 * n)[:2 * n], (gq + [1.0] * 2 * n)[:2 * n]
    best = min(range(-n, n + 1),
               key=lambda d: sum(gp[:n + d]) + sum(gq[n + d:]) + 0.03 * abs(d))
    return best / FPS


def render_video_piece(src, start, frames, cache, draft):
    key = hashlib.sha1(f"{src.resolve()}|v|{start:.3f}|{frames}|{draft}".encode()).hexdigest()[:12]
    out = cache / f"{src.stem}_{key}.mkv"
    if not out.exists():
        tmp = out.with_suffix(".part.mkv")
        ff(["-ss", f"{max(0.0, start):.3f}", "-i", str(src), "-an",
            "-vf", f"{cover(W, H)},fps={FPS},format=yuv420p", "-frames:v", str(frames),
            "-c:v", "libx264", "-preset", "ultrafast" if draft else "veryfast",
            "-crf", "24" if draft else "14", str(tmp)])
        tmp.rename(out)
    return out


def render_audio_piece(src, a, b, vol, cache):
    d = b - a
    key = hashlib.sha1(f"{src.resolve()}|a|{a:.3f}|{b:.3f}|{vol}".encode()).hexdigest()[:12]
    out = cache / f"{src.stem}_{key}.wav"
    if not out.exists():
        fades = (f"{NORM_A},volume={vol},afade=t=in:d={CUT_FADE},"
                 f"afade=t=out:st={max(0.0, d - CUT_FADE):.3f}:d={CUT_FADE}")
        src_in = (["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(src), "-vn", "-af", fades]
                  if has_audio(src) else
                  ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo"])
        tmp = out.with_suffix(".part.wav")
        ff(src_in + ["-t", f"{d:.3f}", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(tmp)])
        tmp.rename(out)
    return out


def concat(pieces, out, durations=None):
    """Join pieces without re-encoding. Give the exact durations for video:
    each piece's container counts one frame too many, which would add up
    to sound drifting out of sync."""
    listing = out.with_suffix(".txt")
    listing.write_text("".join(
        f"file '{p.resolve()}'\n" + (f"duration {durations[i]:.6f}\n" if durations else "")
        for i, p in enumerate(pieces)))
    try:
        ff(["-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(out)])
    finally:
        listing.unlink(missing_ok=True)


def render_base(segments, out, draft):
    """Join the pieces. Sound is cut exactly; the picture cut at each join
    between talk pieces may sit a few frames off it (picture_shift), on the
    frame grid so sound and picture never drift apart."""
    cache = out.parent / ".cache"
    cache.mkdir(exist_ok=True)
    starts = [0.0]
    for _, a, b, *_ in segments:
        starts.append(starts[-1] + b - a)
    cuts = [0]
    for i in range(1, len(segments)):
        shift = 0.0
        if segments[i - 1][4] and segments[i][4]:
            shift = picture_shift(segments[i - 1], segments[i])
        frame = round((starts[i] + shift) * FPS)
        if frame - cuts[-1] < 0.3 * FPS:        # never leave a sliver
            frame = round(starts[i] * FPS)
        cuts.append(frame)
        if shift:
            kind = "L" if shift < 0 else "J"
            print(f"  cut {i}: {kind} cut, picture {abs(shift):.2f}s "
                  f"{'early' if shift < 0 else 'late'}", flush=True)
    cuts.append(round(starts[-1] * FPS))
    video, audio = [], []
    for i, (src, a, b, vol, _) in enumerate(segments):
        print(f"  piece {i + 1}/{len(segments)}: {src.name} {a:.2f}-{b:.2f}s", flush=True)
        start = a + cuts[i] / FPS - starts[i]
        video.append(render_video_piece(src, start, cuts[i + 1] - cuts[i], cache, draft))
        audio.append(render_audio_piece(src, a, b, vol, cache))
    vpath, apath = out.with_name(out.stem + "_v.mkv"), out.with_name(out.stem + "_a.wav")
    try:
        concat(video, vpath, [(cuts[i + 1] - cuts[i]) / FPS for i in range(len(video))])
        concat(audio, apath)
        ff(["-i", str(vpath), "-i", str(apath), "-map", "0:v", "-map", "1:a",
            "-c", "copy", str(out)])
    finally:
        vpath.unlink(missing_ok=True)
        apath.unlink(missing_ok=True)


# --- 2. anchors and the panel timeline ---------------------------------------
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


def anchor_time(at, words, what):
    if isinstance(at, (int, float)):
        return float(at)
    i = find_word(at, words)
    if i is None:
        print(f"WARNING: {what}: word '{at}' not in the transcript, skipped. "
              "Check the transcript printed below.", file=sys.stderr)
        return None
    return words[i]["start"]


def build_timeline(panels, words, total, footage):
    """Panels -> contiguous entries on frame boundaries covering the whole video."""
    starts = []
    for p in panels:
        t = anchor_time(p.get("at", 0), words, f"panel '{p.get('file') or p.get('full')}'")
        if t is not None:
            starts.append((min(max(t, 0.0), total), p))
    starts.sort(key=lambda e: e[0])
    if not starts or starts[0][0] > 1.0:
        starts.insert(0, (0.0, {"full": "talk"}))      # open full screen on you
    else:
        starts[0] = (0.0, starts[0][1])
    frames = [round(t * FPS) for t, _ in starts] + [round(total * FPS)]
    timeline = []
    for (_, p), f0, f1 in zip(starts, frames, frames[1:]):
        if f1 <= f0:
            continue
        full = p.get("full")
        kind = "split" if not full else "talk" if full == "talk" else "full"
        src = footage / (p["file"] if kind == "split" else full) if kind != "talk" else None
        timeline.append({"start": f0 / FPS, "end": f1 / FPS, "frames": f1 - f0,
                         "kind": kind, "panel": p, "src": src})
    return timeline


# --- 3. visuals --------------------------------------------------------------
def visual(k, entry, w, h, n):
    """Filter chain that turns input k into exactly n frames at w x h."""
    p, src, d = entry["panel"], entry["src"], entry["frames"] / FPS
    if is_image(src):
        chain = f"[{k}:v]{cover(2 * w, 2 * h, p.get('focus', 0.5))}"
        regions = p.get("censor") or []
        if regions and not isinstance(regions[0], list):
            regions = [regions]
        for j, (x, y, cw, ch) in enumerate(regions):
            X, Y = int(x * 2 * w), int(y * 2 * h)
            CW, CH = max(2, int(cw * 2 * w)), max(2, int(ch * 2 * h))
            tag = f"cz{k}_{j}"
            chain += (f",split[{tag}a][{tag}b];[{tag}b]crop={CW}:{CH}:{X}:{Y},"
                      f"scale={max(1, CW // CENSOR_BLOCKS)}:-1,scale={CW}:{CH}:flags=neighbor"
                      f"[{tag}p];[{tag}a][{tag}p]overlay={X}:{Y}")
        z0, z1 = (1.0, 1.0 + ZOOM) if k % 2 else (1.0 + ZOOM, 1.0)
        z = f"{z0}{'+' if z1 >= z0 else '-'}{abs(z1 - z0)}*on/{max(1, n - 1)}"
        return (f"{chain},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d={n}:s={w}x{h}:fps={FPS},setsar=1,format=yuv420p")
    # clips are opened already seeked to their "in" point (see render_final)
    return (f"[{k}:v]setpts=PTS-STARTPTS,{cover(w, h)},fps={FPS},"
            f"tpad=stop_mode=clone:stop_duration={d + 1:.3f},trim=end_frame={n},"
            f"setpts=PTS-STARTPTS,format=yuv420p")


def filler(w, h, n):
    return (f"color=c=black:s={w}x{h}:r={FPS}:d={n / FPS + 1:.3f},trim=end_frame={n},"
            f"setpts=PTS-STARTPTS,format=yuv420p")


def spans(timeline, kind):
    # windows run half a frame early so each switch falls between two frames,
    # never on one where rounding could go either way
    h = 0.5 / FPS
    return "+".join(f"between(t,{e['start'] - h:.4f},{e['end'] - h:.4f})"
                    for e in timeline if e["kind"] == kind)


# --- 4. captions, labels, end card -------------------------------------------
def apply_fixes(words, fixes):
    """Swap misheard phrases for the right words, keeping their timing."""
    for wrong, right in fixes:
        toks = [norm(t) for t in wrong.split()]
        new = right.split()
        i = 0
        while i <= len(words) - len(toks):
            if [norm(w["text"]) for w in words[i:i + len(toks)]] != toks:
                i += 1
                continue
            s, e = words[i]["start"], words[i + len(toks) - 1]["end"]
            tail = re.search(r"[.,!?;:]*$", words[i + len(toks) - 1]["text"]).group()
            step = (e - s) / len(new)
            if re.search(r"[.,!?;:]$", new[-1]):
                tail = ""
            words[i:i + len(toks)] = [
                {"text": t + (tail if j == len(new) - 1 else ""),
                 "start": s + j * step, "end": s + (j + 1) * step}
                for j, t in enumerate(new)]
            i += len(new)
    return words


def caption_events(words, highlight, cap=CAPTION_STYLES["legend"]):
    chunks, cur = [], []
    for w in words:
        raw = w["text"].strip()
        text = re.sub(r"[,;:\"“”]+|\.(?!\d)", "", raw)   # keeps "$1.50"
        text = text.upper() if cap["case"] == "upper" else text.lower()
        if cur and text.startswith("-"):              # "euro" "-maxing"
            cur[-1] = {**cur[-1], "clean": cur[-1]["clean"] + text, "text": raw,
                       "end": w["end"]}
            continue
        if not text:
            continue
        if cur:
            prev = cur[-1]["text"]
            length = len(" ".join(x["clean"] for x in cur)) + 1 + len(text)
            if (len(cur) >= cap["max_words"] or length > cap["max_chars"]
                    or w["start"] - cur[-1]["end"] > 0.4
                    or re.search(r"[.!?]$", prev)
                    or (re.search(r"[,;:]$", prev) and len(cur) >= 2)):
                chunks.append(cur)
                cur = []
        cur.append({**w, "text": raw, "clean": text})
    if cur:
        chunks.append(cur)

    events = []
    for n, chunk in enumerate(chunks):
        s, e = chunk[0]["start"], chunk[-1]["end"] + 0.3
        if n + 1 < len(chunks):
            nxt = chunks[n + 1][0]["start"]
            e = nxt if nxt - chunk[-1]["end"] < 0.6 else min(e, nxt)
        text = " ".join(
            f"{{\\c{ACCENT}}}{x['clean']}{{\\c&H00FFFFFF&}}"
            if norm(x["clean"]) in highlight
            or (cap["accent_numbers"] and re.search(r"\d", x["clean"])) else x["clean"]
            for x in chunk)
        events.append((s, e, text))
    return events


def write_ass(path, captions, texts, timeline, tag, end_card, title=None,
              cap=CAPTION_STYLES["legend"]):
    cx = W // 2
    head = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Caption,{FONT_NAME},{cap['size']},&H00FFFFFF,&H00FFFFFF,&H00000000,"
        f"&H90000000,-1,0,0,0,100,100,0,0,1,{cap['outline']},2,5,60,60,0,1",
        f"Style: Pill,{FONT_NAME},{PILL_SIZE},&H00FFFFFF,&H00FFFFFF,{PILL_COLOR},"
        f"{PILL_COLOR},-1,0,0,0,100,100,0,0,3,18,0,5,90,90,0,1",
        f"Style: Tag,{FONT_NAME},{TAG_SIZE},&H00222222,&H00222222,&H00000000,"
        f"&H00000000,-1,0,0,0,100,100,6,0,1,0,0,5,40,40,0,1",
        f"Style: Card,{FONT_NAME},96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,"
        f"-1,0,0,0,100,100,4,0,1,0,0,5,60,60,0,1",
        f"Style: Title,{FONT_NAME},{TITLE_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,"
        f"&H70000000,-1,0,0,0,100,100,0,0,1,0,4,5,40,40,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    ev = []

    def at(x, y):
        return f"{{\\an5\\pos({x},{round(y)})}}"

    # captions follow the layout: on the seam when split, lower third when full
    case = str.upper if cap["case"] == "upper" else str.lower
    for s, e, text in captions + [(s, e, case(t)) for s, e, t in texts]:
        if end_card:                   # the card owns the ending
            e = min(e, end_card["start"])
        for entry in timeline:
            a, b = max(s, entry["start"]), min(e, entry["end"])
            if b - a < 0.05:
                continue
            y = SEAM_Y if entry["kind"] == "split" else H * cap["y"]
            ev.append(f"Dialogue: 2,{ass_time(a)},{ass_time(b)},Caption,,0,0,0,,{at(cx, y)}{text}")
    for entry in timeline:
        a, b, p = ass_time(entry["start"]), ass_time(entry["end"]), entry["panel"]
        if entry["kind"] == "split":
            if tag:
                ev.append(f"Dialogue: 1,{a},{b},Tag,,0,0,0,,{at(cx, HEADER_H / 2)}{tag.upper()}")
            if p.get("label"):
                ev.append(f"Dialogue: 1,{a},{b},Pill,,0,0,0,,"
                          f"{at(cx, SEAM_Y - 96)}{p['label'].upper()}")
        elif entry["kind"] == "full" and p.get("label"):
            ev.append(f"Dialogue: 1,{a},{b},Pill,,0,0,0,,{at(cx, H * 0.16)}{p['label'].upper()}")
    if title:                          # big opening title, as in the footsteps refs
        text = title["text"].replace("\n", "\\N")
        ev.append(f"Dialogue: 3,{ass_time(title['start'])},{ass_time(title['end'])},Title,,"
                  f"0,0,0,,{at(cx, H * TITLE_Y)}{text}")
    if end_card:
        a, b = ass_time(end_card["start"]), ass_time(end_card["end"])
        box = "m 0 0 l {0} 0 {0} {1} 0 {1}".format(W, H)
        ev.append(f"Dialogue: 3,{a},{b},Card,,0,0,0,,{{\\an7\\pos(0,0)\\p1\\c&H000000&"
                  f"\\1a&H38&\\bord0\\shad0}}{box}{{\\p0}}")
        ev.append(f"Dialogue: 4,{a},{b},Card,,0,0,0,,{at(cx, H * 0.42)}"
                  f"{end_card.get('title', 'LIFESTYLE LEGENDS').upper()}")
        if end_card.get("sub"):
            ev.append(f"Dialogue: 4,{a},{b},Card,,0,0,0,,{{\\fs44\\c{ACCENT}}}"
                      f"{at(cx, H * 0.50)}{end_card['sub'].upper()}")
    path.write_text("\n".join(head + ev) + "\n", encoding="utf-8")


# --- 5. compose ----------------------------------------------------------------
def render_final(base, total, timeline, music, ass_path, crop_y, out, draft):
    # exact frame times on the joined talk: its stamps are rounded to the
    # millisecond, which let a panel switch land a frame early (a flash frame)
    inputs, parts, k, v = ["-i", str(base)], [f"[0:v]setpts=N/({FPS}*TB)[base];"], 1, "[base]"
    # one continuous stream per layer; entries that don't use a layer get black
    # filler, and `enable` shows each layer only during its own entries
    for kind, w, h, name in (("split", W, PANEL_H, "top"), ("full", W, H, "fullv")):
        if not spans(timeline, kind):
            continue
        labels = []
        for i, entry in enumerate(timeline):
            if entry["kind"] == kind:
                if not is_image(entry["src"]):
                    d = entry["frames"] / FPS + 1
                    inputs += ["-ss", f"{float(entry['panel'].get('in', 0)):.3f}",
                               "-t", f"{d:.3f}"]
                inputs += ["-i", str(entry["src"])]
                parts.append(f"{visual(k, entry, w, h, entry['frames'])}[{name}{i}];")
                k += 1
            else:
                parts.append(f"{filler(w, h, entry['frames'])}[{name}{i}];")
            labels.append(f"[{name}{i}]")
        parts.append(f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0,"
                     f"setpts=N/({FPS}*TB)[{name}];")

    if spans(timeline, "split"):
        cy = round(H * crop_y)
        parts.append(f"[base]split=2[bfull][bcrop];[bcrop]crop={W}:{BOTTOM_H}:0:{cy}[bottom];"
                     f"color=c={HEADER_COLOR}:s={W}x{H}:r={FPS}:d={total + 1:.3f}[canvas];"
                     f"[canvas][top]overlay=0:{HEADER_H}[c1];"
                     f"[c1][bottom]overlay=0:{SEAM_Y}[splitv];"
                     f"[bfull][splitv]overlay=0:0:enable='{spans(timeline, 'split')}'[v1];")
        v = "[v1]"
    if spans(timeline, "full"):
        parts.append(f"{v}[fullv]overlay=0:0:enable='{spans(timeline, 'full')}'[v2];")
        v = "[v2]"

    voice = "[0:a]"
    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music["file"])]
        vol = music.get("volume", MUSIC_VOLUME)
        parts.append(f"[0:a]asplit=2[voice][sc];[{k}:a]{NORM_A},atrim=duration={total:.3f},"
                     f"volume={vol},afade=t=out:st={max(0, total - 1.5):.3f}:d=1.5[mraw];"
                     f"[mraw][sc]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=400[m];"
                     f"[voice][m]amix=inputs=2:duration=first:normalize=0[ao];")
    else:
        parts.append(f"{voice}anull[ao];")

    ass = str(ass_path).replace("\\", "/").replace(":", r"\:")
    fonts = str(FONTS_DIR).replace(":", r"\:")
    parts.append(f"{v}ass='{ass}':fontsdir='{fonts}'[vo]")
    encode(inputs, "".join(parts), "[vo]", "[ao]", out, draft, total=total)


def pick_font():
    """Proxima Nova if it's in ./fonts, else Montserrat SemiBold (free, close match)."""
    if check_font():
        return FONT_NAME
    for f in FONTS_DIR.glob("*"):
        if f.suffix.lower() not in (".otf", ".ttf"):
            continue
        name = subprocess.run(["fc-scan", "--format", "%{fullname}", str(f)],
                              text=True, capture_output=True).stdout.lower()
        if "montserrat" in name and "semibold" in name:
            print("Using Montserrat SemiBold for captions instead.", file=sys.stderr)
            return "Montserrat SemiBold"
    return FONT_NAME


def main():
    global FONT_NAME
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--model", default="small",
                    help="whisper model size (tiny/base/small/medium/large-v3)")
    ap.add_argument("--draft", action="store_true", help="fast low-quality render for review")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the cut, transcript and panels without rendering")
    args = ap.parse_args()

    plan = json.loads(args.plan.read_text())
    footage = ROOT / plan.get("footage", "input")
    panels = plan.get("panels", [])
    names = ([i.get("talk") or i.get("broll") for i in plan["sequence"]]
             + [p.get("file") or p.get("full") for p in panels if p.get("full") != "talk"]
             + ([plan["music"]["file"]] if plan.get("music") else []))
    missing = [footage / f for f in names if f and not (footage / f).exists()]
    if missing:
        sys.exit("Missing footage:\n  " + "\n  ".join(str(m) for m in missing))

    out = args.output or ROOT / "output" / f"{args.plan.stem}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    FONT_NAME = pick_font()

    segments, words, texts = build_sequence(plan, footage, args.model)
    words = apply_fixes(words, plan.get("fix", []))
    cap = CAPTION_STYLES[plan.get("captions", {}).get("style", "legend")]
    if args.dry_run:
        total = sum(seg[2] - seg[1] for seg in segments)
        report(words, build_timeline(panels, words, total, footage))
        print(f"\nDry run: {total:.1f}s, nothing rendered.")
        return
    base = out.with_name(f"{out.stem}_base.mkv")
    rough = out.with_name(f"{out.stem}_rough.mp4")
    print("Joining your talk clips...")
    render_base(segments, base, args.draft)
    total = duration(base)

    timeline = build_timeline(panels, words, total, footage)
    end_card = None
    if plan.get("end_card"):
        t = anchor_time(plan["end_card"].get("at", max(0, total - 3)), words, "end card")
        if t is not None:
            end_card = {**plan["end_card"], "start": t, "end": total}
    title = None
    if plan.get("title"):
        t = plan["title"]
        end = (anchor_time(t["until"], words, "title") if "until" in t else None) \
            or float(t.get("end", 5.0))
        title = {"text": t["text"], "start": 0.0, "end": min(end, total)}
    highlight = {norm(h) for h in plan.get("highlight", [])}
    ass_path = out.with_suffix(".ass")
    write_ass(ass_path, caption_events(words, highlight, cap), texts, timeline,
              plan.get("series_tag"), end_card, title, cap)
    music = ({**plan["music"], "file": footage / plan["music"]["file"]}
             if plan.get("music") else None)

    print("Building the split screen, panels and captions...")
    try:
        render_final(base, total, timeline, music, ass_path,
                     plan.get("aroll_crop_y", AROLL_CROP_Y), rough, args.draft)
        print("Boosting audio...")
        boost(rough, out)
    finally:
        base.unlink(missing_ok=True)
        rough.unlink(missing_ok=True)

    report(words, timeline)
    print(f"\nDone: {out}  ({total:.1f}s, captions: {ass_path})")


def report(words, timeline):
    print("\nEdited transcript (anchor words for panels):")
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
    print("\nPanels:")
    for e in timeline:
        what = "you, full screen" if e["kind"] == "talk" else e["src"].name
        label = f"  [{e['panel']['label']}]" if e["panel"].get("label") else ""
        print(f"  {e['start']:6.2f}-{e['end']:6.2f}s  {e['kind']:5}  {what}{label}")


if __name__ == "__main__":
    main()
