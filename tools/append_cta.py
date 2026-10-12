"""Append a call-to-action clip to the end of a finished edit.

  python3 tools/append_cta.py <finished> <cta> <out> [--cut-at SECONDS]

--cut-at drops everything from that time on (e.g. an old CTA) before the new one.
The CTA is conformed to the edit's size and frame rate, its loudness is matched to the
edit, the edit's audio (music) fades out over the last 0.3 s (0.08 s with --cut-at) and crossfades into the CTA.
"""
import argparse, json, re, subprocess

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)

def probe(p):
    s = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,avg_frame_rate:format=duration", "-of", "json", p]).stdout)
    v = s["streams"][0]
    n, d = v["avg_frame_rate"].split("/")
    return v["width"], v["height"], float(n) / float(d), float(s["format"]["duration"])

def lufs(p, start=None, end=None):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner"]
    if start is not None:
        cmd += ["-ss", str(start)]
    if end is not None:
        cmd += ["-t", str(end - (start or 0))]
    cmd += ["-i", p, "-af", "ebur128", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])

ap = argparse.ArgumentParser()
ap.add_argument("finished"); ap.add_argument("cta"); ap.add_argument("out")
ap.add_argument("--cut-at", type=float)
a = ap.parse_args()
w, h, fps, dur = probe(a.finished)
end = min(a.cut_at or dur, dur)
end = int(end * fps) / fps                       # whole frames
gain = lufs(a.finished, max(0, end - 12), end) - lufs(a.cta)
xf = 0.12
fade = 0.08 if a.cut_at else 0.3   # cutting mid-talk: short fade so the last word stays
graph = (f"[0:v]trim=end={end:.4f},setpts=PTS-STARTPTS,fps={fps:.6f},scale={w}:{h},setsar=1[v0];"
         f"[1:v]fps={fps:.6f},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[v1];"
         f"[v0][v1]concat=n=2:v=1:a=0[v];"
         f"[0:a]atrim=end={end:.4f},asetpts=PTS-STARTPTS,aresample=48000,"
         f"afade=t=out:st={max(0, end - fade):.4f}:d={fade}[a0];"
         f"[1:a]aresample=48000,volume={gain:.2f}dB,apad=pad_dur={xf}[a1];"
         f"[a0][a1]acrossfade=d={xf}:c1=tri:c2=tri,alimiter=limit=0.85:level=false[a]")
run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", a.finished, "-i", a.cta,
     "-filter_complex", graph, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
     "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
     "-movflags", "+faststart", a.out])
# bring the whole thing to the brand loudness (-12 LUFS, peaks under -1 dB). Plain gain
# (linear loudnorm) + limiter: no denoise, since finished edits carry music.
m = json.loads(re.search(r"\{[^{}]*\}\s*$", subprocess.run(
    ["ffmpeg", "-nostdin", "-hide_banner", "-i", a.out, "-af",
     "loudnorm=I=-12:TP=-1:LRA=20:print_format=json", "-f", "null", "-"],
    capture_output=True, text=True).stderr).group(0))
norm = (f"loudnorm=I=-12:TP=0:LRA=20:linear=true:measured_I={m['input_i']}:"
        f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']},"
        f"aresample=48000,alimiter=limit={10 ** (-1.8 / 20):.4f}:level=false")
tmp = a.out + ".tmp.mp4"
run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", a.out, "-af", norm, "-c:v", "copy",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
import os; os.replace(tmp, a.out)
print(f"{a.out}: edit {end:.2f}s + CTA, CTA gain {gain:+.1f} dB, then to -12 LUFS (was {m['input_i']})")
