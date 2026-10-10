#!/usr/bin/env python3
"""Fingerprint video frames with CLIP so raw clips can be matched to finished edits.

Embed one clip from a temporary download URL (the video is deleted afterwards):
  python3 tools/clip_embed.py embed <url> <out.npz> --fps 1      # finished edit: 1 frame/s
  python3 tools/clip_embed.py embed <url> <out.npz> --frames 8   # raw clip: 8 evenly spaced frames

Match finished edits against raw clips (prints JSON usage counts):
  python3 tools/clip_embed.py match <finished_dir> <raw_dir> [--thresh 0.72] [--min-inliers 25]

Matching: CLIP similarity picks candidate frames, then ORB keypoints + RANSAC confirm it's
literally the same footage (survives the crop, zoom and captions an edit adds).

Each .npz holds `emb` (frames x 512, L2-normalised) and `t` (frame times in seconds).
"""
import argparse
import os
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

_model = None


def model():
    global _model
    if _model is None:
        import open_clip
        import torch
        torch.set_num_threads(int(os.environ.get("CLIP_THREADS", "4")))
        m, _, pre = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
        m.eval()
        _model = (m, pre, torch)
    return _model


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def embed(url, out, fps=None, frames=None):
    from PIL import Image
    m, pre, torch = model()
    with tempfile.TemporaryDirectory() as tmp:
        if url.startswith("http"):
            clip = Path(tmp) / "clip"
            subprocess.run(["curl", "-sS", "-f", "-m", "900", "-o", str(clip), url], check=True)
        else:
            clip = Path(url)
        dur = duration(clip)
        if fps:
            times = list(np.arange(0.25, max(dur, 0.3), 1.0 / fps))
        else:
            times = [dur * (i + 0.5) / frames for i in range(frames)]
        imgs, kept, thumbs = [], [], []
        for i, t in enumerate(times):
            f = Path(tmp) / f"{i}.jpg"
            subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", str(clip),
                            "-frames:v", "1", "-vf", "scale=-2:360", str(f)])
            if f.exists():
                imgs.append(pre(Image.open(f).convert("RGB")))
                kept.append(t)
                thumbs.append(np.frombuffer(f.read_bytes(), dtype=np.uint8))
        if not imgs:
            raise SystemExit(f"no frames decoded from {url[:60]}")
        with torch.no_grad():
            e = m.encode_image(torch.stack(imgs)).float()
        e = (e / e.norm(dim=-1, keepdim=True)).numpy().astype(np.float16)
    tb = np.empty(len(thumbs), dtype=object)
    tb[:] = thumbs
    np.savez(out, emb=e, t=np.array(kept, dtype=np.float32), duration=dur, thumbs=tb)
    print(json.dumps({"out": str(out), "frames": len(kept), "duration": round(dur, 2)}))


def inliers(a_jpg, b_jpg):
    """Number of geometrically consistent ORB matches between two frames (same footage => high)."""
    import cv2
    a = cv2.imdecode(a_jpg, cv2.IMREAD_GRAYSCALE)
    b = cv2.imdecode(b_jpg, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create(1500)
    ka, da = orb.detectAndCompute(a, None)
    kb, db = orb.detectAndCompute(b, None)
    if da is None or db is None or len(ka) < 10 or len(kb) < 10:
        return 0
    pairs = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2)
    good = [m for m, *n in pairs if n and m.distance < 0.75 * n[0].distance]
    if len(good) < 8:
        return 0
    pa = np.float32([ka[m.queryIdx].pt for m in good])
    pb = np.float32([kb[m.trainIdx].pt for m in good])
    # similarity transform covers the crop/zoom/shift an edit applies
    _, mask = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=6)
    return int(mask.sum()) if mask is not None else 0


def match(fin_dir, raw_dir, thresh, min_inliers=25):
    raw = {p.stem: np.load(p, allow_pickle=True) for p in Path(raw_dir).glob("*.npz")}
    names = list(raw)
    R = np.concatenate([raw[n]["emb"].astype(np.float32) for n in names])
    owner = np.concatenate([[i] * len(raw[n]["emb"]) for i, n in enumerate(names)])
    local = np.concatenate([np.arange(len(raw[n]["emb"])) for n in names])
    usage = {}
    for p in sorted(Path(fin_dir).glob("*.npz")):
        fz = np.load(p, allow_pickle=True)
        F, ft = fz["emb"].astype(np.float32), fz["t"]
        sims = F @ R.T
        hits = {}
        for fi in range(len(F)):
            tried = set()
            for ri in np.argsort(-sims[fi])[:6]:  # top candidates for this second of the edit
                if sims[fi, ri] < thresh:
                    break
                n = names[owner[ri]]
                if n in tried:
                    continue
                tried.add(n)
                k = inliers(fz["thumbs"][fi], raw[n]["thumbs"][local[ri]])
                if k >= min_inliers:
                    hits.setdefault(n, []).append((float(ft[fi]), k))
                    break
        for n, h in hits.items():
            usage.setdefault(n, []).append({"edit": p.stem, "seconds": len(h),
                                            "at": [round(t) for t, _ in h], "inliers": max(k for _, k in h)})
    print(json.dumps(usage, indent=1))


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
e = sub.add_parser("embed"); e.add_argument("url"); e.add_argument("out")
g = e.add_mutually_exclusive_group(required=True)
g.add_argument("--fps", type=float); g.add_argument("--frames", type=int)
mt = sub.add_parser("match"); mt.add_argument("fin_dir"); mt.add_argument("raw_dir")
mt.add_argument("--thresh", type=float, default=0.72)
mt.add_argument("--min-inliers", type=int, default=25)
a = ap.parse_args()
if a.cmd == "embed":
    embed(a.url, a.out, a.fps, a.frames)
else:
    match(a.fin_dir, a.raw_dir, a.thresh, a.min_inliers)
