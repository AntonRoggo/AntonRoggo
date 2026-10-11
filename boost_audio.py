#!/usr/bin/env python3
"""Make a video's audio as loud as possible without clipping, keeping it natural.

Chain (two passes):
  1. highpass 80 Hz        - removes rumble that eats headroom
  2. RNNoise denoiser      - background (crowd, room, wind) pushed well under the voice
  3. gentle compressor     - evens out words without lifting background in pauses
  4. presence EQ           - clearer voice
  5. loudnorm (measured)   - linear gain to the loudness target, no pumping
  6. true-peak limiter     - ceiling just under 0 dBFS so nothing clips

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
TRUE_PEAK = -1.0       # dBTP target after encoding
LIMIT = 10 ** (-1.8 / 20)  # limiter ceiling (sample peak), lower than TRUE_PEAK to leave
                           # room for inter-sample peaks and AAC encoding overshoot

DENOISE_MODEL = Path(__file__).resolve().parent / "tools" / "models" / "cb.rnnn"
PROCESS_DELAY = 0.015  # seconds of latency added by the denoiser + limiter
DENOISE_MIX = 0.9  # 1.0 = remove all background; 0.9 keeps a little room sound so it stays natural

PRE = ("highpass=f=80,"
       # neural speech denoiser (RNNoise): pulls crowd/room noise down under the voice
       f"arnndn=m={DENOISE_MODEL}:mix={DENOISE_MIX},"
       # gentle compression evens out words without lifting the background in pauses
       "acompressor=threshold=-20dB:ratio=2:attack=10:release=200:makeup=1:knee=6,"
       # voice clarity: a little presence, a little less boxiness
       "equalizer=f=3000:t=q:w=1.2:g=2,equalizer=f=250:t=q:w=1:g=-1.5")


def measure(src):
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-vn", "-af",
         f"{PRE},loudnorm=I={TARGET_LUFS}:TP=0:LRA=20:print_format=json",
         "-f", "null", "-"], text=True, capture_output=True, check=True).stderr
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err).group(0))


def audio_filter(m):
    return (f"{PRE},loudnorm=I={TARGET_LUFS}:TP=0:LRA=20:"
            f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
            f"offset={m['target_offset']}:linear=true,"
            # resample BEFORE limiting, so nothing after the limiter can create new peaks
            f"aresample=48000,"
            f"alimiter=limit={LIMIT:.4f}:attack=5:release=50:level=false,"
            # RNNoise (10 ms) + limiter (5 ms) delay the sound slightly: trim it back into sync
            f"atrim=start={PROCESS_DELAY},asetpts=PTS-STARTPTS")


def boost(src, out):
    m = measure(src)
    has_video = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
         "stream=index", "-of", "csv=p=0", str(src)],
        text=True, capture_output=True).stdout.strip() != ""
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
           "-af", audio_filter(m), "-c:a", "aac", "-b:a", "192k"]
    if has_video:
        cmd += ["-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-shortest", "-movflags", "+faststart"]
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
