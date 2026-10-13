"""Make a review copy of a finished edit for the review tool.

  python3 tools/review_proxy.py output/clip_edited.mp4 [-o output/review/clip_v2.mp4]

The review tool stores videos as artifact assets, which are capped at 15 MB. This re-encodes
the edit (same size and frame rate, H.264 + AAC, fast start) at the highest bitrate that fits
under --max-mb, then prints the facts the review tool needs as JSON:
{"file", "bytes", "duration", "width", "height", "fps"}.
The finished edit itself is never touched; only this copy is uploaded for review.
"""
import argparse, json, os, subprocess

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)

def probe(p):
    s = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,avg_frame_rate:format=duration", "-of", "json", p]).stdout)
    v = s["streams"][0]
    n, d = v["avg_frame_rate"].split("/")
    return v["width"], v["height"], float(n) / float(d), float(s["format"]["duration"])

ap = argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("-o", "--output")
ap.add_argument("--max-mb", type=float, default=14.0)
a = ap.parse_args()
out = a.output or os.path.join("output", "review", os.path.splitext(os.path.basename(a.input))[0] + ".mp4")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
w, h, fps, dur = probe(a.input)

audio_k = 160
size = os.path.getsize(a.input)
if size <= a.max_mb * 1e6 and a.input.endswith(".mp4"):
    # already small enough: only move the index to the front so it streams
    run(["ffmpeg", "-nostdin", "-y", "-i", a.input, "-c", "copy", "-movflags", "+faststart", out])
else:
    # 4% headroom for the container; cap at 12 Mbps (more is wasted on a phone screen)
    video_k = min(12000, int(a.max_mb * 8e3 * 0.96 / dur) - audio_k)
    log = out + ".2pass"   # per output, so several copies can encode at once
    for attempt in range(3):
        common = ["-c:v", "libx264", "-preset", "medium", "-b:v", f"{video_k}k",
                  "-maxrate", f"{int(video_k * 1.5)}k", "-bufsize", f"{video_k * 2}k",
                  "-pix_fmt", "yuv420p", "-passlogfile", log]
        run(["ffmpeg", "-nostdin", "-y", "-i", a.input, *common, "-pass", "1", "-an", "-f", "mp4", os.devnull])
        run(["ffmpeg", "-nostdin", "-y", "-i", a.input, *common, "-pass", "2",
             "-c:a", "aac", "-b:a", f"{audio_k}k", "-movflags", "+faststart", out])
        if os.path.getsize(out) <= a.max_mb * 1e6:
            break
        video_k = int(video_k * 0.85)
    for f in os.listdir(os.path.dirname(out) or "."):
        if f.startswith(os.path.basename(log)):
            os.remove(os.path.join(os.path.dirname(out) or ".", f))

bytes_ = os.path.getsize(out)
if bytes_ > a.max_mb * 1e6:
    raise SystemExit(f"{out} is still {bytes_ / 1e6:.1f} MB; lower the resolution and try again")
print(json.dumps({"file": out, "bytes": bytes_, "duration": round(dur, 3),
                  "width": w, "height": h, "fps": round(fps, 3)}))
