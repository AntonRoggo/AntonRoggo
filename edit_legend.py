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
            unless "cut": false) and b-roll clips, joined in order
  panels    each starts at a spoken word and holds until the next one:
              {"at": "fifteen", "file": "boat.jpg", "label": "OYSTER PIRATE"}
              {"at": "Namaste", "full": "talk"}        you, full screen
              {"at": "surf", "full": "surf.mp4"}       b-roll, full screen
            "censor": [x, y, w, h] pixelates part of a photo (fractions)
  title     {"text": "Following Cousteau\nalong the Riviera", "until": "1936"}
            big opening title (default 5 s)
  end_card  {"at": "follow", "title": "...", "sub": "..."} over the ending
  music     optional bed, ducked under the voice

Anchors: "swim" = first word starting with "swim", "swim#2" = the second,
a number = that many seconds in. Before the first panel you're full screen.

Usage:
  python3 edit_legend.py series/lifestyle-legends/plans/london_a_origin.json
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
# -----------------------------------------------------------------------------

CUT_FADE = 0.015
NORM_A = "aformat=sample_rates=48000:channel_layouts=stereo"


def cover(w, h):
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
            f"setsar=1")


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
            else:
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
        parts.append(f"[{k}:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS,"
                     f"{cover(W, H)},fps={FPS},format=yuv420p[v{i}];")
        if audio[src]:
            parts.append(f"[{k}:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,{NORM_A},"
                         f"volume={vol},afade=t=in:d={CUT_FADE},"
                         f"afade=t=out:st={max(0.0, d - CUT_FADE):.3f}:d={CUT_FADE}[a{i}];")
        else:
            parts.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{i}];")
        labels += f"[v{i}][a{i}]"
    graph = "".join(parts) + f"{labels}concat=n={len(segments)}:v=1:a=1[v][a]"
    encode([x for f in files for x in ("-i", str(f))], graph, "[v]", "[a]", out, draft, crf=16)


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
        chain = f"[{k}:v]{cover(2 * w, 2 * h)}"
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
    return (f"[{k}:v]trim=start={p.get('in', 0)},setpts=PTS-STARTPTS,{cover(w, h)},fps={FPS},"
            f"tpad=stop_mode=clone:stop_duration={d + 1:.3f},trim=end_frame={n},"
            f"setpts=PTS-STARTPTS,format=yuv420p")


def filler(w, h, n):
    return (f"color=c=black:s={w}x{h}:r={FPS}:d={n / FPS + 1:.3f},trim=end_frame={n},"
            f"setpts=PTS-STARTPTS,format=yuv420p")


def spans(timeline, kind):
    return "+".join(f"between(t,{e['start']:.4f},{e['end'] - 0.001:.4f})"
                    for e in timeline if e["kind"] == kind)


# --- 4. captions, labels, end card -------------------------------------------
def caption_events(words, highlight):
    chunks, cur = [], []
    for w in words:
        raw = w["text"].strip()
        text = re.sub(r"[.,;:\"“”]+", "", raw).upper()
        if cur and text.startswith("-"):              # "euro" "-maxing"
            cur[-1] = {**cur[-1], "clean": cur[-1]["clean"] + text, "text": raw,
                       "end": w["end"]}
            continue
        if not text:
            continue
        if cur:
            prev = cur[-1]["text"]
            length = len(" ".join(x["clean"] for x in cur)) + 1 + len(text)
            if (len(cur) >= CAPTION_MAX_WORDS or length > CAPTION_MAX_CHARS
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
            if norm(x["clean"]) in highlight or re.search(r"\d", x["clean"]) else x["clean"]
            for x in chunk)
        events.append((s, e, text))
    return events


def write_ass(path, captions, texts, timeline, tag, end_card, title=None):
    cx = W // 2
    head = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Caption,{FONT_NAME},{CAPTION_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,"
        f"&H90000000,-1,0,0,0,100,100,0,0,1,{CAPTION_OUTLINE},2,5,60,60,0,1",
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
    for s, e, text in captions + [(s, e, t.upper()) for s, e, t in texts]:
        if end_card:                   # the card owns the ending
            e = min(e, end_card["start"])
        for entry in timeline:
            a, b = max(s, entry["start"]), min(e, entry["end"])
            if b - a < 0.05:
                continue
            y = SEAM_Y if entry["kind"] == "split" else H * CAPTION_FULL_Y
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
    inputs, parts, k, v = ["-i", str(base)], [], 1, "[0:v]"
    # one continuous stream per layer; entries that don't use a layer get black
    # filler, and `enable` shows each layer only during its own entries
    for kind, w, h, name in (("split", W, PANEL_H, "top"), ("full", W, H, "fullv")):
        if not spans(timeline, kind):
            continue
        labels = []
        for i, entry in enumerate(timeline):
            if entry["kind"] == kind:
                inputs += ["-i", str(entry["src"])]
                parts.append(f"{visual(k, entry, w, h, entry['frames'])}[{name}{i}];")
                k += 1
            else:
                parts.append(f"{filler(w, h, entry['frames'])}[{name}{i}];")
            labels.append(f"[{name}{i}]")
        parts.append(f"{''.join(labels)}concat=n={len(labels)}:v=1:a=0[{name}];")

    if spans(timeline, "split"):
        cy = round(H * crop_y)
        parts.append(f"[0:v]split=2[bfull][bcrop];[bcrop]crop={W}:{BOTTOM_H}:0:{cy}[bottom];"
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
    panels = plan.get("panels", [])
    names = ([i.get("talk") or i.get("broll") for i in plan["sequence"]]
             + [p.get("file") or p.get("full") for p in panels if p.get("full") != "talk"]
             + ([plan["music"]["file"]] if plan.get("music") else []))
    missing = [footage / f for f in names if f and not (footage / f).exists()]
    if missing:
        sys.exit("Missing footage:\n  " + "\n  ".join(str(m) for m in missing))

    out = args.output or ROOT / "output" / f"{args.plan.stem}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    check_font()

    segments, words, texts = build_sequence(plan, footage, args.model)
    base = out.with_name(f"{out.stem}_base.mp4")
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
    write_ass(ass_path, caption_events(words, highlight), texts, timeline,
              plan.get("series_tag"), end_card, title)
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
    print(f"\nDone: {out}  ({total:.1f}s, captions: {ass_path})")


if __name__ == "__main__":
    main()
