#!/usr/bin/env python3
"""Download one clip from a temporary URL, make a contact sheet, delete the clip.

Usage: python3 tools/broll_sheet.py <download_url> <out_dir> <name>
Prints JSON: duration, width, height, rotation, sheet path, frame timestamps.
The sheet is 6 evenly spaced frames, auto-rotated, each labelled with its time.
"""
import json
import subprocess
import sys
from pathlib import Path

url, out_dir, name = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
out_dir.mkdir(parents=True, exist_ok=True)
clip = out_dir / f"{name}.bin"
sheet = out_dir / f"{name}.jpg"
try:
    subprocess.run(["curl", "-sS", "-f", "-m", "600", "-o", str(clip), url], check=True)
    info = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:stream_side_data=rotation:format=duration",
         "-of", "json", str(clip)], capture_output=True, text=True, check=True).stdout)
    st = info["streams"][0]
    dur = float(info["format"]["duration"])
    rot = next((int(s.get("rotation", 0)) for s in st.get("side_data_list", []) if "rotation" in s), 0)
    times = [round(dur * (i + 0.5) / 6, 2) for i in range(6)]
    frames = []
    for i, t in enumerate(times):
        f = out_dir / f"{name}_{i}.jpg"
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(clip),
                        "-frames:v", "1", "-vf",
                        f"scale=-2:240,drawtext=text='{t}s':x=6:y=6:fontsize=20:fontcolor=yellow:box=1:boxcolor=black@0.6",
                        str(f)], check=True)
        frames.append(f)
    inputs = sum([["-i", str(f)] for f in frames], [])
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *inputs, "-filter_complex",
                    "".join(f"[{i}]" for i in range(6)) + "hstack=inputs=6", str(sheet)], check=True)
    for f in frames:
        f.unlink()
    w, h = st["width"], st["height"]
    if abs(rot) in (90, 270):
        w, h = h, w
    print(json.dumps({"duration": round(dur, 2), "width": w, "height": h,
                      "rotation": rot, "sheet": str(sheet), "times": times}))
finally:
    clip.unlink(missing_ok=True)
