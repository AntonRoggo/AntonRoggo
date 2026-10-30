#!/usr/bin/env python3
"""Edit a creator's raw talking-head footage into a TTT ad, in the style of skill tt-ad-edit
(the founder confession breakdown).

  python3 tallowed-truth/tools/tt_edit.py raw.mp4 --plan-only            # 1. cuts + transcript
  python3 tallowed-truth/tools/tt_edit.py raw.mp4 --headline "OFFICIAL STATEMENT|from The Tallowed Truth Founder" \\
      --popups popups.json                                               # 2. render

What it does (rules in tallowed-truth/skills/tt-ad-edit/SKILL.md):
  * cuts fumbles, restarts, fillers and pauses (pauses left at ~0.2 s), J-cuts at every cut
    (the engine is edit_video.py at the repo root)
  * captions: Proxima Nova Semibold 70 px, white, 4 px black outline + soft shadow, lowercase,
    apostrophes kept, 2 words, fixed at 68% of the height, hidden while a pop-up is up
  * headline banner: white box, black text ("LINE 1|line 2"), from frame 1 until the first
    pop-up (or 3 s)
  * pop-ups centred on the caption zone, 0.3 s fade in, starting/ending on cuts where one is close
  * audio: RNNoise, -12 LUFS, -1 dBTP (boost_audio.py), no music

popups.json, times found from the words said (see <out>.timeline.json after --plan-only):
  [{"say": "gives people glowing", "until": "feeling skin", "files": ["cust1.jpg", "cust2.jpg"]},
   {"say": "in the comments", "until": "good stuff", "file": "reviews_scroll.mp4"},
   {"say": "plastic surgeon", "review": "r-b072bac3"}]
  "files" = two images side by side, "file" = one image or video on a white panel, "review" = a
  review card rendered from reviews/reviews.csv. Use "start"/"end" (edited-timeline seconds)
  instead of "say"/"until" to place one by time. Optional "width" (fraction of the frame).

Fonts: put Proxima Nova Semibold / Bold / Extrabold (.otf/.ttf) in fonts/ at the repo root;
without them it falls back to Inter so the preview still renders.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
import edit_video as ev  # noqa: E402

# --- TTT house style (from the founder confession, FBA1400B) -----------------------------------
MAX_PAUSE = 0.3        # pauses longer than this are cut...
PAD_IN, PAD_OUT = 0.12, 0.2   # ...leaving about 0.2 s, so it never sounds rushed or robotic
WORDS = 2              # words per caption
CAPTION_Y = 0.668      # caption centre, fraction of the height (baseline lands at ~68%)
FONT_SIZE = 70         # at 1080 wide
OUTLINE, SHADOW = 4, 3
SHADOW_COLOUR = "&H66000000"   # black, ~60% opaque
POPUP_Y = 0.64         # pop-up centre, fraction of the height (the caption zone)
FADE_IN = 0.3
SNAP_START = 0.6       # a pop-up starts on a cut if one is this close
SNAP_END = 1.5         # ...and runs on to the next cut if it's this close after its end
BANNER_MAX = 3.0       # banner stays until the first pop-up, at most this long if there's none
# -------------------------------------------------------------------------------------------------

SYS_FONTS = Path("/usr/share/fonts/opentype/inter")


def font_file(weights):
    """Proxima Nova in fonts/ in the first matching weight, else Inter."""
    for f in sorted(ev.FONTS_DIR.glob("*")):
        name = f.name.lower().replace(" ", "").replace("-", "")
        if "proxima" in name and any(w in name for w in weights) and f.suffix.lower() in (".otf", ".ttf"):
            return f, True
    inter = {"extrabold": "Inter-ExtraBold.otf", "bold": "Inter-Bold.otf", "semibold": "Inter-SemiBold.otf"}
    return SYS_FONTS / inter[weights[0]], False


def caption_font():
    f, proxima = font_file(["semibold"])
    if not proxima:
        print("WARNING: Proxima Nova Semibold not in fonts/, captions use Inter SemiBold for this render",
              file=sys.stderr)
    return ("Proxima Nova Semibold" if proxima else "Inter SemiBold"), f.parent


def caption_text(word):
    """Lowercase, apostrophes kept ("i'll", "you've"), no other punctuation."""
    w = word.replace("’", "'").replace("‘", "'").replace("-", " ").lower()
    return re.sub(r"[^\w\s']", "", w).strip(" '")


def norm(t):
    return re.sub(r"[^a-z0-9']", "", t.lower().replace("’", "'"))


def find_phrase(timed, phrase, after=0.0):
    """(start, end) on the edited timeline of the first place the words of `phrase` are said."""
    want = [norm(w) for w in phrase.split() if norm(w)]
    toks = [norm(t) for _, _, t in timed]
    for i in range(len(toks) - len(want) + 1):
        if timed[i][0] >= after and toks[i:i + len(want)] == want:
            return timed[i][0], timed[i + len(want) - 1][1]
    raise SystemExit(f"pop-up phrase not found in the transcript: {phrase!r} (check <out>.timeline.json)")


def place_popups(specs, timed, cuts, total):
    out = []
    for p in specs:
        if "say" in p:
            s, e = find_phrase(timed, p["say"])
            if "until" in p:
                e = find_phrase(timed, p["until"], after=s)[1]
            elif "seconds" in p:
                e = s + p["seconds"]
            else:
                e = max(e, s + 2.5)
        else:
            s, e = float(p["start"]), float(p["end"])
        near = [c for c in cuts if abs(c - s) <= SNAP_START]
        if near:
            s = min(near, key=lambda c: abs(c - s))
        after = [c for c in cuts if e <= c <= e + SNAP_END]
        if after:
            e = after[0]
        e = min(e, total)
        if e - s >= 1.0:
            out.append(dict(p, start=round(s, 3), end=round(e, 3)))
    out.sort(key=lambda p: p["start"])
    for a, b in zip(out, out[1:]):
        a["end"] = min(a["end"], b["start"])
    return out


def write_captions(timed, popups, width, height, path, font):
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {width}", f"PlayResY: {height}",
        "ScaledBorderAndShadow: yes", "WrapStyle: 2", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
        "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: TT,{font},{round(FONT_SIZE * width / 1080)},&H00FFFFFF,&H00FFFFFF,&H00000000,{SHADOW_COLOUR},"
        f"0,0,0,0,100,100,0,0,1,{OUTLINE * width / 1080:.1f},{SHADOW * width / 1080:.1f},5,40,40,0,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    chunks = ev.caption_chunks(timed, max_words=WORDS)
    events = []
    for k, ch in enumerate(chunks):
        text = " ".join(t for t in (caption_text(w) for _, _, w in ch) if t)
        if not text:
            continue
        start = ch[0][0]
        nxt = chunks[k + 1][0][0] if k + 1 < len(chunks) else None
        end = nxt if nxt is not None and nxt - ch[-1][1] < 0.6 else ch[-1][1] + 0.3
        events.append([start, max(end, start + ev.MIN_CAPTION), text])
    shown = []
    for s, e, text in events:  # no captions while a pop-up is on screen
        for p in popups:
            if s < p["end"] and e > p["start"]:
                if s >= p["start"] - 0.05:
                    s = max(s, p["end"])
                else:
                    e = min(e, p["start"])
        if e - s >= 0.15:
            shown.append((s, e, text))
    shown = [list(c) for c in shown]
    for i in range(len(shown) - 1):  # never two captions at once (libass would stack them)
        cur, nxt = shown[i], shown[i + 1]
        cur[1] = min(cur[1], nxt[0])
        if cur[1] - cur[0] < 0.25 and nxt[0] - cur[1] < 0.05 and nxt[1] - (cur[0] + 0.25) >= 0.25:
            cur[1] = nxt[0] = cur[0] + 0.25  # no flashes: borrow a moment from the next caption
    y = round(height * CAPTION_Y)
    for s, e, text in shown:
        lines.append(f"Dialogue: 0,{ev.ass_time(s)},{ev.ass_time(e)},TT,,0,0,0,,{{\\an5\\pos({width // 2},{y})}}{text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(shown)


def banner_png(text, width, height, path):
    """White box, black text: 'LINE ONE|line two'. Measured from the founder ad: 77% wide, top at 57.7%."""
    from PIL import Image, ImageDraw, ImageFont
    top, bottom = (text.split("|", 1) + [""])[:2]
    k = width / 1080
    f1, _ = font_file(["extrabold", "black", "heavy"])
    f2, _ = font_file(["bold"])
    box_w, pad = int(831 * k), int(14 * k)
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def fit(fontfile, size, txt):
        while size > 20:
            font = ImageFont.truetype(str(fontfile), size)
            if d.textlength(txt, font=font) <= box_w - 2 * pad:
                return font
            size -= 2
        return ImageFont.truetype(str(fontfile), size)

    t1 = fit(f1, int(70 * k), top.strip())
    t2 = fit(f2, int(50 * k), bottom.strip()) if bottom.strip() else None
    h1 = t1.getbbox(top.strip())[3]
    h2 = t2.getbbox(bottom.strip())[3] if t2 else 0
    gap = int(8 * k) if t2 else 0
    box_h = pad + h1 + gap + h2 + pad
    y0 = int(height * 0.577)
    x0 = (width - box_w) // 2
    d.rectangle((x0, y0, x0 + box_w, y0 + box_h), fill="white")
    d.text((width // 2, y0 + pad), top.strip(), font=t1, fill="black", anchor="mt")
    if t2:
        d.text((width // 2, y0 + pad + h1 + gap), bottom.strip(), font=t2, fill="black", anchor="mt")
    im.save(path)


def popup_asset(p, width, tmp, idx):
    """Return (input args, filter for that input producing a scaled RGBA picture, is_video)."""
    from PIL import Image
    if "review" in p:
        import csv
        import review_card
        csv.field_size_limit(10**9)
        rows = {r["id"]: r for r in csv.DictReader(open(HERE.parent / "reviews" / "reviews.csv", encoding="utf-8"))}
        if p["review"] not in rows:
            raise SystemExit(f"review {p['review']} not in reviews.csv")
        png = tmp / f"pop{idx}.png"
        review_card.card(rows[p["review"]], p.get("name", True), p.get("max_chars", 420)).save(png)
        return ["-loop", "1", "-i", str(png)], f"scale={int(width * p.get('width', 0.85))}:-1", False
    if "files" in p:  # two pictures side by side, thin dark border
        w_each = int(width * p.get("width", 0.36))
        tiles = []
        for f in p["files"][:2]:
            im = Image.open(f).convert("RGB")
            im = im.resize((w_each, int(im.height * w_each / im.width)))
            tiles.append(im)
        h = min(t.height for t in tiles)
        gap, b = int(width * 0.05), max(2, width // 270)
        canvas = Image.new("RGBA", (w_each * 2 + gap + 4 * b, h + 2 * b), (0, 0, 0, 0))
        for i, t in enumerate(tiles):
            x = i * (w_each + 2 * b + gap)
            canvas.paste((40, 40, 40, 255), (x, 0, x + w_each + 2 * b, h + 2 * b))
            canvas.paste(t.crop((0, (t.height - h) // 2, w_each, (t.height - h) // 2 + h)), (x + b, b))
        png = tmp / f"pop{idx}.png"
        canvas.save(png)
        return ["-loop", "1", "-i", str(png)], "null", False
    f = Path(p["file"])
    video = f.suffix.lower() in (".mp4", ".mov", ".m4v", ".webm")
    w = int(width * p.get("width", 0.8))
    if video:
        cin = p.get("clip_in", 0)
        return ["-i", str(f)], f"trim=start={cin},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=30,scale={w}:-2", True
    return ["-loop", "1", "-i", str(f)], f"scale={w}:-1", False


def overlay_pass(rough, out, popups, banner, width, height, fps, tmp):
    inputs, chain, last, n = ["-i", str(rough)], [], "0:v", 1
    if banner:
        inputs += ["-loop", "1", "-i", str(banner[0])]
        chain.append(f"[{n}:v]format=rgba,trim=duration={banner[1]:.3f}[bn];"
                     f"[{last}][bn]overlay=0:0:eof_action=pass:enable='lt(t,{banner[1]:.3f})'[v{n}];")
        last, n = f"v{n}", n + 1
    cy = int(height * POPUP_Y)
    for i, p in enumerate(popups):
        args, filt, video = popup_asset(p, width, tmp, i)
        inputs += args
        s, e = p["start"], p["end"]
        chain.append(f"[{n}:v]{filt},fps={fps:.6f},format=rgba,trim=duration={e - s:.3f},setpts=PTS-STARTPTS+{s:.3f}/TB,"
                     f"fade=t=in:st={s:.3f}:d={FADE_IN}:alpha=1[p{i}];"
                     f"[{last}][p{i}]overlay=x=(W-w)/2:y={cy}-h/2:eof_action=pass:enable='between(t,{s:.3f},{e:.3f})'[v{n}];")
        last, n = f"v{n}", n + 1
    if n == 1:
        return rough
    graph = tmp / "overlay.txt"
    text = "".join(chain)
    graph.write_text(text[:text.rfind(f"[{last}];")] + "[vo]")
    ev.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *inputs, "-filter_complex_script", str(graph),
            "-map", "[vo]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            "-c:a", "copy", "-movflags", "+faststart", str(out)])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--model", default="small.en", help="whisper model (small.en is quick; medium.en is more accurate)")
    ap.add_argument("--hint", default="tallow, The Tallowed Truth, F-Balm, tallow balm, beeswax, raw honey",
                    help="words to help transcription")
    ap.add_argument("--headline", help='banner text, "LINE ONE|line two"; omit for no banner')
    ap.add_argument("--popups", type=Path, help="JSON list of pop-ups (see top of file)")
    ap.add_argument("--drop", action="append", default=[], metavar="START-END", help="source range to cut (outtakes)")
    ap.add_argument("--cut", action="append", default=[], metavar="START-END", help="source range removed exactly")
    ap.add_argument("--keep", action="append", default=[], metavar="START-END", help="source range always kept")
    ap.add_argument("--fix", action="append", default=[], metavar="START-END=TEXT", help="caption fix for misheard words")
    ap.add_argument("--end", type=float, metavar="SEC", help="source time where the video ends")
    ap.add_argument("--plan-only", action="store_true", help="work out cuts and transcript, don't render")
    a = ap.parse_args()

    ev.MAX_PAUSE, ev.PAD_IN, ev.PAD_OUT = MAX_PAUSE, PAD_IN, PAD_OUT
    out = a.output or ROOT / "output" / f"{a.input.stem}_tt.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    width, height, duration = ev.probe(a.input)

    cache = out.with_suffix(".words.json")
    if cache.exists():
        words = json.loads(cache.read_text())
    else:
        print("Transcribing...")
        words = ev.transcribe(a.input, a.model, a.hint)
        cache.write_text(json.dumps(words))
    for f in a.fix:
        words = ev.fix_words(words, f)
    if a.end is not None:
        words = [w for w in words if (w["start"] + w["end"]) / 2 <= a.end]
    span = lambda r: tuple(float(v) for v in r.split("-"))
    drop = ev.mark_mistakes(words)
    forced = [span(r) for r in a.keep]
    mid = lambda w: (w["start"] + w["end"]) / 2
    drop = {i for i in drop if not any(x <= mid(words[i]) <= y for x, y in forced)}  # --keep brings the captions back too
    cuts_src = [span(r) for r in a.cut]
    for i, w in enumerate(words):
        if any(x <= (w["start"] + w["end"]) / 2 <= y for x, y in [span(r) for r in a.drop] + cuts_src):
            drop.add(i)
    silences = ev.detect_silences(a.input, duration)
    keep, kept = ev.build_keep(words, drop, silences, duration)
    keep = ev.trim_to_speech(ev.cut_pauses(keep, ev.detect_pauses(a.input, MAX_PAUSE)), a.input)
    if forced:
        merged = []
        for x, y in sorted(keep + forced):
            if merged and x <= merged[-1][1] + 0.05:
                merged[-1] = (merged[-1][0], max(merged[-1][1], y))
            else:
                merged.append((x, y))
        keep = merged
    if cuts_src:
        keep = ev.subtract(keep, [(x - ev.PAD, y + ev.PAD) for x, y in cuts_src])
    if a.end is not None:
        keep = [(x, min(y, a.end)) for x, y in keep if x < a.end]

    fps = ev.source_fps(a.input)
    timed = ev.timed_words(kept, keep)
    total = sum(y - x for x, y in keep) - ev.AUDIO_OVERLAP * (len(keep) - 1)
    pic_cuts = ev.picture_cuts(keep, fps)[1][1:-1]
    removed = [words[i]["text"] for i in sorted(drop)]
    print(f"{duration:.1f}s raw -> {total:.1f}s edit, {len(keep)} segments ({len(pic_cuts)} cuts)")
    print(f"Cut words (fumbles, fillers, retakes): {' '.join(removed) or '-'}")
    out.with_suffix(".timeline.json").write_text(json.dumps(
        [{"text": t, "start": round(s, 2), "end": round(e, 2)} for s, e, t in timed], indent=0))
    out.with_suffix(".keep.json").write_text(json.dumps([[round(x, 3), round(y, 3)] for x, y in keep]))

    popups = place_popups(json.loads(a.popups.read_text()), timed, pic_cuts, total) if a.popups else []
    for p in popups:
        print(f"Pop-up {p['start']:.2f}-{p['end']:.2f}s: {p.get('say') or p.get('file') or p.get('review')}")
    font, _ = caption_font()
    ass = out.with_suffix(".ass")
    n = write_captions(timed, popups, width, height, ass, font)
    print(f"{n} captions")
    if a.plan_only:
        print(f"Transcript on the edited timeline: {out.with_suffix('.timeline.json')}")
        return

    import tempfile
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        tmp = Path(tmp)
        rough = tmp / "rough.mp4"
        print("Rendering cuts + captions...")
        ev.render(a.input, keep, ass, rough, (), (width, height))
        banner = None
        if a.headline:
            png = tmp / "banner.png"
            banner_png(a.headline, width, height, png)
            first = popups[0]["start"] if popups and popups[0]["start"] < 6 else BANNER_MAX
            banner = (png, min(first, 6.0))
        print("Banner + pop-ups...")
        layered = overlay_pass(rough, tmp / "layered.mp4", popups, banner, width, height, fps, tmp)
        print("Audio (RNNoise, -12 LUFS, -1 dBTP)...")
        ev.boost(layered, out)
    print(f"Done: {out}")


if __name__ == "__main__":
    main()
