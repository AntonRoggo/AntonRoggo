#!/usr/bin/env python3
"""Edit a creator's raw talking-head footage into a TTT ad, in the style of skill tt-ad-edit
(the founder confession breakdown).

  python3 tallowed-truth/tools/tt_edit.py raw.mp4 --plan-only            # 1. numbered sentence list
  python3 tallowed-truth/tools/tt_edit.py raw.mp4 --drop-sentence 1,4,9 --hook "Esthetician shocked by 64 year old's skin:" \\
      --popups popups.json                                               # 2. render

What it does (rules in tallowed-truth/skills/tt-ad-edit/SKILL.md):
  * the sentence is the unit: the plan lists every sentence with a number; you choose which to drop
    (false starts, outtakes, wrong facts). Kept sentences are never cut into. A cut only happens where a
    sentence was dropped or between two sentences with more than 0.7 s of silence. No cut removes less
    than 0.3 s, no shot is shorter than 1.5 s, and a shot starts on the first word, not the breath
    before it (onsets are measured from the audio). J-cuts at every cut (the engine is edit_video.py)
  * captions: Proxima Nova Semibold 70 px, white, 4 px black outline + soft shadow, lowercase,
    apostrophes kept, 3-4 words, a new caption at each sentence or pause, timed to the measured
    start of speech, fixed at 68% of the height, hidden while a pop-up is up
  * text-on-screen hook (rules/tos-hook-rules.md): one short line in a white box above his head,
    from frame 1 for HOOK_SECONDS; no pop-up starts before it ends
  * pop-ups centred on the caption zone, 0.3 s fade in, starting/ending on cuts where one is close
  * audio: RNNoise, -12 LUFS, -1 dBTP (boost_audio.py), no music

popups.json, times found from the words said (see <out>.timeline.json after --plan-only):
  [{"say": "gives people glowing", "until": "feeling skin", "files": ["cust1.jpg", "cust2.jpg"]},
   {"say": "in the comments", "until": "good stuff", "file": "reviews_scroll.mp4"},
   {"say": "sent us this message", "review": "r-959aa813", "from": "She said she", "max_chars": 120,
    "highlight": "has never seen skin like mine"}]
  "files" = two images side by side, "file" = one image or video on a white panel, "review" = a
  review card rendered from reviews/reviews.csv: show only the main point ("from" = the sentence it
  starts at, "max_chars" to stop after it) with "highlight" on the key words. Use "start"/"end" (edited-timeline seconds)
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
MAX_GAP = 0.7          # silence between two kept sentences longer than this is cut; pauses inside a sentence always stay
MIN_REMOVED = 0.3      # a cut must remove at least this much, or it's just a jolt
MIN_SHOT = 1.5         # no shot shorter than this
ONSET_PAD = 0.04       # a shot starts this long before the first word's sound (not on the breath before it)
END_PAD = 0.2          # ...and ends this long after the last word's sound
WORDS = 4              # up to 4 words per caption (3-4)
HOOK_SECONDS = 4.0     # the text-on-screen hook stays up this long
MIN_CAPTION = 0.4      # no caption flashes by faster than this
CAPTION_LEAD = 0.05    # a caption goes up this long before the word's sound starts
CAPTION_Y = 0.668      # caption centre, fraction of the height (baseline lands at ~68%)
FONT_SIZE = 70         # at 1080 wide
OUTLINE, SHADOW = 4, 3
SHADOW_COLOUR = "&H66000000"   # black, ~60% opaque
POPUP_Y = 0.64         # pop-up centre, fraction of the height (the caption zone)
FADE_IN = 0.3
SNAP_START = 0.6       # a pop-up starts on a cut if one is this close
SNAP_END = 1.5         # ...and runs on to the next cut if it's this close after its end
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
        events.append([start, max(end, start + MIN_CAPTION), text])
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
        if cur[1] - cur[0] < MIN_CAPTION and nxt[0] - cur[1] < 0.05 and nxt[1] - (cur[0] + MIN_CAPTION) >= MIN_CAPTION:
            cur[1] = nxt[0] = cur[0] + MIN_CAPTION  # no flashes: borrow a moment from the next caption
    y = round(height * CAPTION_Y)
    for s, e, text in shown:
        lines.append(f"Dialogue: 0,{ev.ass_time(s)},{ev.ass_time(e)},TT,,0,0,0,,{{\\an5\\pos({width // 2},{y})}}{text}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(shown)


def hook_png(text, width, height, path, face):
    """Text-on-screen hook: one short line (two if it must wrap) in black Proxima Nova Semibold on a white
    rounded box, centred above his head (`face` = (x, y, w, h) in output pixels, or None)."""
    from PIL import Image, ImageDraw, ImageFont
    k = width / 1080
    f, _ = font_file(["semibold"])
    font = ImageFont.truetype(str(f), int(64 * k))
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    max_w, pad = int(900 * k), int(22 * k)
    words = text.split()
    lines = [text]
    if d.textlength(text, font=font) > max_w - 2 * pad:  # two balanced lines, never "64 / year old's"
        best = min(range(1, len(words)), key=lambda i: max(d.textlength(" ".join(words[:i]), font=font),
                                                            d.textlength(" ".join(words[i:]), font=font)))
        lines = [" ".join(words[:best]), " ".join(words[best:])]
    lh = int(64 * k * 1.25)
    box_w = int(max(d.textlength(ln, font=font) for ln in lines)) + 2 * pad
    box_h = lh * len(lines) + 2 * pad - int(10 * k)
    head_top = face[1] - int(face[3] * 0.35) if face is not None else int(height * 0.30)  # hair sits above the face box
    y0 = max(int(height * 0.06), head_top - box_h - int(20 * k))
    x0 = (width - box_w) // 2
    d.rounded_rectangle((x0, y0, x0 + box_w, y0 + box_h), radius=int(18 * k), fill="white")
    for i, ln in enumerate(lines):
        d.text((width // 2, y0 + pad + i * lh), ln, font=font, fill="black", anchor="mt")
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
        review_card.card(rows[p["review"]], p.get("name", True), p.get("max_chars", 420), p.get("from"),
                         p.get("highlight")).save(png)
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


def transcribe_chunked(path, model_size, hint, chunk=20.0):
    """Word timestamps that hold up: one pass over a whole long take drifts (up to 0.6 s on Pat's 2.5-min
    take, enough to put a cut inside a word), so transcribe ~20 s chunks split at pauses and offset them."""
    from faster_whisper import WhisperModel
    audio = ev.load_audio(path)
    sr = 16000
    talking, step = ev.speech_mask(path)
    bounds, t = [0.0], 0.0
    total = len(audio) / sr
    while total - t > chunk * 1.5:
        lo, hi = int((t + chunk * 0.75) / step), int(min(total, t + chunk * 1.25) / step)
        quiet = [i for i in range(lo, hi - 10) if not any(talking[i:i + 10])]  # 0.2 s of silence
        t = (quiet[len(quiet) // 2] + 5) * step if quiet else t + chunk
        bounds.append(t)
    bounds.append(total)
    model = WhisperModel(model_size, device="auto", compute_type="int8")
    words = []
    for a, b in zip(bounds, bounds[1:]):
        segs, _ = model.transcribe(audio[int(a * sr):int(b * sr)], word_timestamps=True, vad_filter=False,
                                   initial_prompt=("Um, uh, so, like, I mean... " + hint).strip())
        words += [{"text": w.word.strip(), "start": round(w.start + a, 3), "end": round(w.end + a, 3)}
                  for seg in segs for w in seg.words]
    return words


_local_model = None


def local_words(path, a, b, model_size, hint):
    """Words in source seconds a-b from a transcription of just that window. Word times from a long pass
    can be 0.5 s off; inside a few seconds they're exact, which is what a cut needs."""
    global _local_model
    from faster_whisper import WhisperModel
    if _local_model is None:
        _local_model = WhisperModel(model_size, device="auto", compute_type="int8")
    audio = ev.load_audio(path)[int(max(0.0, a) * 16000):int(b * 16000)]
    segs, _ = _local_model.transcribe(audio, word_timestamps=True, vad_filter=False, initial_prompt=hint)
    return [{"text": w.word.strip(), "start": w.start + max(0.0, a), "end": w.end + max(0.0, a)}
            for seg in segs for w in seg.words]


def heard(path, a, b, model_size, hint):
    """Words heard in source seconds a-b alone (normalised)."""
    return [norm(w["text"]) for w in local_words(path, a, b, model_size, hint) if norm(w["text"])]


def same(x, y):
    return bool(x) and bool(y) and (x == y or (min(len(x), len(y)) >= 3 and (x.startswith(y) or y.startswith(x))))


def place_edges(path, keep, words, sents, dropped, runs, model_size, hint):
    """Where a dropped sentence sits next to a kept one, find the exact edge by ear: step through in 30 ms
    and keep the first point where the shot, heard on its own, ends on its last word whole (or starts on its
    first word, with nothing of the dropped line before it). Needed where he talks straight through from one
    sentence into the next, and the transcript's times are 0.1-0.5 s off."""
    kept_sents = [n for n in range(len(sents)) if n not in dropped]
    out = [list(k) for k in keep]
    for k in range(len(out) - 1):
        b0, a1 = out[k][1], out[k + 1][0]
        last = max(n for n in kept_sents if words[sents[n][0]]["start"] < b0)
        first = min((n for n in kept_sents if words[sents[n][-1]]["end"] > a1), default=last)
        if last + 1 in dropped:
            want, ws, we = norm(words[sents[last][-1]]["text"]), words[sents[last][-1]]["start"], words[sents[last][-1]]["end"]
            after = [(e0, s1) for (_, e0), (s1, _) in zip(runs, runs[1:]) if we - 0.2 <= e0 <= we + 0.6 and s1 - e0 >= 0.15]
            if after:  # a real silence follows: end in it (the ear test can't hear where a drawn-out word ends)
                out[k][1] = min(after[0][0] + END_PAD, after[0][1] - 0.02)
            t = max(ws + 0.1, we - 0.15) if not after else we + 1.0
            while t <= we + 0.6:
                got = heard(path, t - 3.0, t, model_size, hint)
                if got and same(got[-1], want) and not (len(got) > 1 and same(got[-2], want) and got[-1] != want):
                    out[k][1] = t + 0.06
                    break
                t += 0.03
            else:
                if not after:
                    print(f"WARNING: sentence {last} runs straight into the dropped one; no clean end found")
        if first - 1 in dropped:
            want, ws = norm(words[sents[first][0]]["text"]), words[sents[first][0]]["start"]
            t = max(out[k][1] + 0.02, ws - 0.3)
            while t <= ws + 0.5:
                got = heard(path, t, t + 3.0, model_size, hint)
                if got and same(got[0], want):
                    nxt = [r[0] for r in runs if r[0] >= t and r[1] - r[0] >= 0.1]  # skip silence before the word
                    out[k + 1][0] = max(t, nxt[0] - ONSET_PAD) if nxt and nxt[0] - t < 0.8 else t
                    break
                t += 0.03
            else:
                print(f"WARNING: no clean start for sentence {first} (he runs into it from the dropped line); "
                      f"drop it or keep the line before it")
    return [(a, b) for a, b in out]


def check_cuts(path, keep, words, sents, dropped, model_size, hint):
    """Test every cut by ear, the way an editor would: play the shot up to its end on its own and hear its
    last words; play the next shot from its start and hear its first words. Prints both so a clipped word
    or the tail of a dropped line shows up before rendering (transcript times can be 0.5 s off)."""
    kept_sents = [n for n in range(len(sents)) if n not in dropped]
    bad = 0
    print("Cut check (heard alone: end of the shot || start of the next):")
    for (a0, b0), (a1, b1) in zip(keep, keep[1:]):
        last = max(n for n in kept_sents if words[sents[n][0]]["start"] < b0)
        first = min((n for n in kept_sents if words[sents[n][-1]]["end"] > a1), default=last)
        end = heard(path, b0 - 3.0, b0, model_size, hint)
        start = heard(path, a1, a1 + 3.0, model_size, hint)
        ok = (end and same(end[-1], norm(words[sents[last][-1]]["text"]))
              and start and same(start[0], norm(words[sents[first][0]]["text"])))
        bad += not ok
        print(f"  {'ok ' if ok else 'BAD'} {b0:7.2f} -> {a1:7.2f} | ...{' '.join(end[-4:])} || {' '.join(start[:4])}...")
    if bad:
        print(f"WARNING: {bad} cut(s) don't sound clean; fix them before rendering")
    return bad


def sentences(words):
    """Split the transcript into sentences: lists of word indices, ending at . ? ! or a trailing "..."."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if w["text"].rstrip().endswith((".", "?", "!")):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def speech_runs(path):
    """(start, end) of each stretch of sound at speaking level, short gaps (<= 40 ms) closed."""
    talking, step = ev.speech_mask(path)
    runs, start, gap = [], None, 0
    for i, t in enumerate(list(talking) + [False] * 3):
        if t:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap > 2:
                runs.append((start * step, (i - gap + 1) * step))
                start, gap = None, 0
    return runs


def word_onset(w, runs, floor=0.0):
    """When the word's sound really starts. The speech model's start runs ~0.2 s late, and a breath
    before a word is its own short run of sound: take the first run of at least 0.1 s that reaches the
    word, so the shot never opens on the inhale."""
    ws = w["start"]
    hits = [a for a, b in runs if b - a >= 0.1 and b >= ws - 0.05 and a <= ws + 0.25 and a >= ws - 0.6]
    return max(floor, min(hits) if hits else ws - 0.05)  # never reach back into the word before


def word_offset(w, runs, ceiling=1e9):
    """When the word's sound really ends (the model stretches words over the silence after them)."""
    we = w["end"]
    hits = [b for a, b in runs if b - a >= 0.1 and a <= we + 0.05 and b >= we - 0.3 and b <= we + 0.6]
    return min(ceiling, max(hits) if hits else we)  # never run into the next word


def sentence_keep(words, sents, dropped, runs, duration):
    """Kept source ranges built from whole sentences (see the rules at the top of the file)."""
    spans = []  # (sentence number, start, end) of each kept sentence
    for n, idx in enumerate(sents):
        if n in dropped:
            continue
        prev_end = words[idx[0] - 1]["end"] if idx[0] > 0 else 0.0
        next_start = words[idx[-1] + 1]["start"] if idx[-1] + 1 < len(words) else duration
        a = max(prev_end if n - 1 in dropped else 0.0, word_onset(words[idx[0]], runs, prev_end) - ONSET_PAD)
        b = min(duration, next_start if n + 1 in dropped else duration,
                word_offset(words[idx[-1]], runs, next_start) + END_PAD)
        spans.append((n, a, b))
    segs = []  # [first sentence, last sentence, start, end]
    for n, a, b in spans:
        if segs and n == segs[-1][1] + 1:
            # two kept sentences in a row: cut only if the audio has a real silence over MAX_GAP between them
            lo, hi = words[sents[n - 1][-1]]["end"] - 0.3, words[sents[n][0]]["start"] + 0.5
            gaps = [(e0, s1) for (_, e0), (s1, _) in zip(runs, runs[1:]) if e0 >= lo and s1 <= hi and s1 > e0]
            g = max(gaps, key=lambda x: x[1] - x[0], default=None)
            if g is None or g[1] - g[0] <= MAX_GAP:
                segs[-1][1], segs[-1][3] = n, max(segs[-1][3], b)  # no real pause: no cut
                continue
            segs[-1][3] = min(g[0] + END_PAD, (g[0] + g[1]) / 2)  # cut inside the silence itself
            segs.append([n, n, max(g[1] - ONSET_PAD, (g[0] + g[1]) / 2), b])
            continue
        segs.append([n, n, a, b])
    merged = True
    while merged:  # no pointless jolts, no slivers: join neighbours that follow on in the source
        merged = False
        for k in range(len(segs) - 1):
            cur, nxt = segs[k], segs[k + 1]
            follows = nxt[0] == cur[1] + 1
            short = min(cur[3] - cur[2], nxt[3] - nxt[2]) < MIN_SHOT
            if follows and (nxt[2] - cur[3] < MIN_REMOVED or short):
                segs[k] = [cur[0], nxt[1], cur[2], nxt[3]]
                del segs[k + 1]
                merged = True
                break
    for k, (n0, n1, a, b) in enumerate(segs):
        if b - a < MIN_SHOT:
            print(f"WARNING: sentences {n0}-{n1} make a {b - a:.1f}s shot (dropped sentences on both sides)")
    return [(a, b) for _, _, a, b in segs]


def onset_timed(words, runs):
    """Words with their start moved to the measured start of their sound wherever a word follows a
    pause (the model's start is off by -0.1 to +0.3 s there), so each caption goes up as he says it."""
    out = []
    for i, w in enumerate(words):
        if i == 0 or w["start"] - words[i - 1]["end"] > 0.15 or w["start"] - words[i - 1]["start"] > 0.6:
            w = dict(w, start=min(w["start"], word_onset(w, runs, words[i - 1]["end"] if i else 0.0)) - CAPTION_LEAD)
        out.append(w)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--model", default="small.en", help="whisper model (small.en is quick; medium.en is more accurate)")
    ap.add_argument("--hint", default="tallow, The Tallowed Truth, F-Balm, tallow balm, beeswax, raw honey",
                    help="words to help transcription")
    ap.add_argument("--hook", help="text-on-screen hook (rules/tos-hook-rules.md), e.g. \"Esthetician shocked by 64 year old's skin:\"")
    ap.add_argument("--popups", type=Path, help="JSON list of pop-ups (see top of file)")
    ap.add_argument("--drop-sentence", default="", metavar="N,N-M", help="sentence numbers from the plan to leave out")
    ap.add_argument("--fix", action="append", default=[], metavar="START-END=TEXT", help="caption fix for misheard words")
    ap.add_argument("--end", type=float, metavar="SEC", help="source time where the video ends")
    ap.add_argument("--plan-only", action="store_true", help="work out cuts and transcript, don't render")
    a = ap.parse_args()

    out = a.output or ROOT / "output" / f"{a.input.stem}_tt.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    width, height, duration = ev.probe(a.input)

    cache = out.with_suffix(".words.json")
    if cache.exists():
        words = json.loads(cache.read_text())
    else:
        print("Transcribing...")
        words = transcribe_chunked(a.input, a.model, a.hint)
        cache.write_text(json.dumps(words))
    for f in a.fix:
        words = ev.fix_words(words, f)
    if a.end is not None:
        words = [w for w in words if (w["start"] + w["end"]) / 2 <= a.end]

    sents = sentences(words)
    dropped = set()
    for part in filter(None, a.drop_sentence.split(",")):
        lo, _, hi = part.partition("-")
        dropped.update(range(int(lo), int(hi or lo) + 1))
    runs = speech_runs(a.input)
    # The detector's suggestions only: a sentence that's a filler, or restarted by the next one
    suspect = ev.mark_mistakes(words)
    plan = [f"{'  DROP' if n in dropped else '      '} {n:3d} [{words[idx[0]]['start']:6.2f}-{words[idx[-1]]['end']:6.2f}] "
            f"{' '.join(words[i]['text'] for i in idx)}"
            + ("   <- repeat/filler?" if any(i in suspect for i in idx) else "") for n, idx in enumerate(sents)]
    out.with_suffix(".sentences.txt").write_text("\n".join(plan) + "\n")

    keep = sentence_keep(words, sents, dropped, runs, duration)
    keep = place_edges(a.input, keep, words, sents, dropped, runs, a.model, a.hint)
    kept = [words[i] for n, idx in enumerate(sents) if n not in dropped for i in idx]
    kept_cap = onset_timed(kept, runs)  # captions go up when he starts the word, not when the model places it

    fps = ev.source_fps(a.input)
    timed = ev.timed_words(kept_cap, keep)
    total = sum(y - x for x, y in keep) - ev.AUDIO_OVERLAP * (len(keep) - 1)
    pic_cuts = ev.picture_cuts(keep, fps)[1][1:-1]
    print(f"{duration:.1f}s raw -> {total:.1f}s edit, {len(keep)} shots ({len(pic_cuts)} cuts), "
          f"{len(sents) - len(dropped)}/{len(sents)} sentences kept")
    print(f"Sentence list: {out.with_suffix('.sentences.txt')}")
    out.with_suffix(".timeline.json").write_text(json.dumps(
        [{"text": t, "start": round(s, 2), "end": round(e, 2)} for s, e, t in timed], indent=0))
    out.with_suffix(".keep.json").write_text(json.dumps([[round(x, 3), round(y, 3)] for x, y in keep]))

    popups = place_popups(json.loads(a.popups.read_text()), timed, pic_cuts, total) if a.popups else []
    if a.hook:  # the hook is never cut off by a pop-up
        popups = [dict(p, start=max(p["start"], HOOK_SECONDS)) for p in popups]
        popups = [p for p in popups if p["end"] - p["start"] >= 1.0]
    for p in popups:
        print(f"Pop-up {p['start']:.2f}-{p['end']:.2f}s: {p.get('say') or p.get('file') or p.get('review')}")
    font, _ = caption_font()
    ass = out.with_suffix(".ass")
    n = write_captions(timed, popups, width, height, ass, font)
    print(f"{n} captions")
    print("Cuts (source time | last words before | first words after):")
    for (a0, b0), (a1, b1) in zip(keep, keep[1:]):
        before = [w["text"] for w in kept if w["end"] <= b0 + 0.05][-4:]
        after = [w["text"] for w in kept if w["start"] >= a1 - 0.05][:4]
        print(f"  {b0:7.2f} -> {a1:7.2f} ({a1 - b0:.2f}s out) | ...{' '.join(before)} | {' '.join(after)}...")
    check_cuts(a.input, keep, words, sents, dropped, a.model, a.hint)
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
        if a.hook:
            png = tmp / "hook.png"
            hook_png(a.hook, width, height, png, ev.face_box(a.input, keep[0][0] + 1.0, width, height))
            banner = (png, HOOK_SECONDS)
        print("Hook + pop-ups...")
        layered = overlay_pass(rough, tmp / "layered.mp4", popups, banner, width, height, fps, tmp)
        print("Audio (RNNoise, -12 LUFS, -1 dBTP)...")
        ev.boost(layered, out)
    print(f"Done: {out}")


if __name__ == "__main__":
    main()
