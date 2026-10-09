#!/usr/bin/env python3
"""Make a video's audio as loud as possible without clipping, keeping it natural.

Chain (two passes):
  1. highpass 80 Hz        - removes rumble that eats headroom
  2. slow leveller         - evens out quiet and loud sections gradually
  3. gentle compressor     - tames individual loud words so nothing jumps out
  4. loudnorm (measured)   - linear gain to the loudness target, no pumping
  5. true-peak limiter     - ceiling just under 0 dBFS so nothing clips

The video stream is copied untouched.

Usage:
  python3 boost_audio.py input.mp4 [-o output.mp4]
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

TARGET_LUFS = -12.0    # loud, social-media level
TRUE_PEAK = -1.0       # dBTP; headroom so AAC encoding doesn't push peaks over 0
LIMIT = 10 ** (TRUE_PEAK / 20)  # linear ceiling for the limiter

PRE = ("highpass=f=80,"
       # slow leveller: lifts quiet sections over ~15 s windows, so no pumping
       "dynaudnorm=f=500:g=31:p=0.9:m=8:r=0,"
       "acompressor=threshold=-18dB:ratio=3:attack=15:release=250:makeup=1:knee=6")


def measure(src):
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-vn", "-af",
         f"{PRE},loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA=11:print_format=json",
         "-f", "null", "-"], text=True, capture_output=True, check=True).stderr
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err).group(0))


def audio_filter(m):
    return (f"{PRE},loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK}:LRA=11:"
            f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
            f"offset={m['target_offset']}:linear=true,"
            f"alimiter=limit={LIMIT:.4f}:attack=5:release=50:level=false,"
            f"aresample=48000")


def boost(src, out):
    m = measure(src)
    has_video = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
         "stream=index", "-of", "csv=p=0", str(src)],
        text=True, capture_output=True).stdout.strip() != ""
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
           "-af", audio_filter(m), "-c:a", "aac", "-b:a", "192k"]
    if has_video:
        cmd += ["-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-movflags", "+faststart"]
    subprocess.run(cmd + [str(out)], check=True)
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    out = args.output or args.input.with_name(f"{args.input.stem}_loud{args.input.suffix}")
    m = boost(args.input, out)
    print(f"Loudness {float(m['input_i']):.1f} LUFS -> {TARGET_LUFS} LUFS, "
          f"peaks capped at {TRUE_PEAK} dBTP: {out}")


if __name__ == "__main__":
    main()
