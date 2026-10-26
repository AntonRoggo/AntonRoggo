#!/usr/bin/env python3
"""Cut a vertical reel out of a horizontal YouTube video (letterbox format).

The horizontal picture stays whole, full width, centred on a 1080x1920 black frame. A title sits in the
top bar and the house-style captions sit in the bottom bar, just under the picture. Same cutting rules as
the talking-head edits: clips trimmed to his voice, pauses over ~0.7 s cut, every join a J-cut (audio
overlaps 0.1 s, picture follows 0.1 s later), voice denoised then -12 LUFS / -1 dBTP, natural grade.

Plan JSON:
  {"source": "input/youtube/<id>.mp4",
   "words": "input/youtube/<id>.words.json",   # faster-whisper segments with "words" [{s, e, w}]
   "keep": [[15.2, 21.1], [135.3, 139.5]],     # source ranges, in order (the best take of each line)
   "title": "you dont need another european summer",
   "grade": "natural",                         # or "none" (finished YouTube exports are already graded)
   "max_pause": 0.7,
   "fix": {"283.6": "just"},                   # caption text by word start time (2 decimals)
   "out": "output/reels/<name>.mp4"}

  python3 tools/letterbox_reel.py plan.json [--preview]
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import edit_video as ev  # noqa: E402
import voiceover_edit as vo  # noqa: E402

W, H = 1080, 1920
PIC_H = 608                 # 16:9 at full width
PIC_Y = (H - PIC_H) // 2    # picture centred: 656..1264
TITLE_Y = PIC_Y - 130       # title block centre, in the top bar
CAPTION_Y = PIC_Y + PIC_H + 110   # captions centre, in the bottom bar
TITLE_SIZE = 62


def load_words(path, fix):
    words = []
    for seg in json.load(open(path)):
        for w in seg["words"]:
            text = fix.get(f"{w['s']:.2f}", w["w"]).strip()
            if text:
                words.append({"start": w["s"], "end": w["e"], "text": text})
    return words


def title_line(text, total):
    words = [w for w in (ev.caption_text(w) for w in text.split()) if w]
    if len(" ".join(words)) > 20 and len(words) > 1:
        k = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
        body = " ".join(words[:k]) + r"\N" + " ".join(words[k:])
    else:
        body = " ".join(words)
    return (f"Dialogue: 1,{ev.ass_time(0)},{ev.ass_time(total)},Default,,0,0,0,,"
            f"{{\\an5\\pos({W // 2},{TITLE_Y})\\fs{TITLE_SIZE}}}{body}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", type=Path)
    ap.add_argument("--preview", action="store_true", help="print captions and cuts, don't render")
    args = ap.parse_args()
    plan = json.loads(args.plan.read_text())
    src = ROOT / plan["source"]
    out = ROOT / plan["out"]
    out.parent.mkdir(parents=True, exist_ok=True)

    keep = ev.trim_to_speech([tuple(r) for r in plan["keep"]], src)
    keep = ev.cut_pauses(keep, ev.detect_pauses(src, plan.get("max_pause", ev.MAX_PAUSE)))
    words = load_words(ROOT / plan["words"], plan.get("fix", {}))
    kept = [w for w in words if any(a <= (w["start"] + w["end"]) / 2 <= b for a, b in keep)]
    total = sum(b - a for a, b in keep) - ev.AUDIO_OVERLAP * (len(keep) - 1)

    ass = out.with_suffix(".ass")
    ev.write_captions(kept, keep, W, H, ass)   # centred; moved into the bottom bar below
    text = re.sub(r"\\pos\(\d+,\d+\)", rf"\\pos({W // 2},{CAPTION_Y})", ass.read_text(encoding="utf-8"))
    if plan.get("title"):
        text = text.rstrip("\n") + "\n" + title_line(plan["title"], total) + "\n"
    ass.write_text(text, encoding="utf-8")
    print(f"{len(keep)} pieces, {total:.1f}s")
    for line in text.splitlines():
        if line.startswith("Dialogue: 0"):
            p = line.split(",", 9)
            print(f"  {p[1]}  {re.sub(r'{[^}]*}', '', p[9])}")
    if args.preview:
        return

    fps = ev.source_fps(src)
    grade = vo.grade_filter(plan.get("grade", "natural"))
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        tmp = Path(tmp)
        listing = []
        for i, (vs, ve) in enumerate(ev.jcut_video(keep, fps)):
            frames = int(round((ve - vs) * fps))
            if frames <= 0:
                continue
            piece = tmp / f"seg{i:03d}.mp4"
            vf = (vo.hdr_to_sdr(str(src)) + f"scale={W}:{PIC_H},setsar=1," + grade +
                  f"pad={W}:{H}:0:{PIC_Y}:black,fps={fps:.6f}")
            ev.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{vs:.4f}", "-i", str(src),
                    "-frames:v", str(frames), "-an", "-vf", vf,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(piece)])
            listing.append(f"file '{piece.name}'")
        (tmp / "list.txt").write_text("\n".join(listing) + "\n")
        voice = tmp / "voice.wav"
        vo.render_voice(src, [(a, b, 0) for a, b in keep], voice, linear=True)
        # gain + limiter, then once more by what the limiter took off, so it lands on -12 LUFS
        lim = (f"aresample={vo.SR * 4},alimiter=limit={10 ** (-2.2 / 20):.4f}:attack=5:release=50:level=false,"
               f"aresample={vo.SR}")
        mix = tmp / "mix.wav"
        gain = vo.TARGET_LUFS - float(vo.loudnorm_json(voice)["input_i"])
        for _ in range(8):
            ev.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(voice), "-af",
                    f"volume={gain:.2f}dB,{lim}", str(mix)])
            miss = vo.TARGET_LUFS - float(vo.loudnorm_json(mix)["input_i"])
            print(f"  audio gain {gain:+.1f} dB -> off by {miss:+.1f}")
            if abs(miss) < 0.3:
                break
            gain += miss * 1.5   # the limiter eats part of every boost
        ass_f = str(ass).replace("\\", "/").replace(":", r"\:")
        fonts = str(ev.FONTS_DIR).replace(":", r"\:")
        ev.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", str(tmp / "list.txt"), "-i", str(mix),
                "-filter_complex", f"[0:v]ass='{ass_f}':fontsdir='{fonts}'[v];[1:a]anull[a]",
                "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "aac", "-b:a", "192k", "-ar", str(vo.SR), "-movflags", "+faststart", str(out)])
    print(out)


if __name__ == "__main__":
    main()
