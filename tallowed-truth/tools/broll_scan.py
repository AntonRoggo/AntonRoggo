#!/usr/bin/env python3
"""Scan Drive folders for B-roll and images: download one file at a time, check whether anyone
talks in it, save thumbnails, delete the file. Resumable (files already in scan.jsonl are skipped).

  python3 tallowed-truth/tools/broll_scan.py sources.json <out_dir>

sources.json: a list of
  {"label": "Assets / MASTER BROLL", "brief": "", "creator": "", "notion": "", "drive_folder": "<folder id>"}
or, for files already listed, {"label": ..., "files": [["<file id>", "<path>"], ...]}.

Writes <out_dir>/scan.jsonl (one line per file) and <out_dir>/thumbs/<file id>_<n>.jpg.
A video counts as B-roll when it has no audio or fewer than 4 words are spoken in it
("talking" otherwise). Images are kept as "image". Needs gdown, faster-whisper, ffmpeg.
"""
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import gdown
import numpy as np
from PIL import Image

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

WORKERS = 4  # files downloaded and checked at once (downloads are the slow part)
_lock = threading.Lock()
VIDEO = {".mov", ".mp4", ".m4v", ".3gp", ".avi", ".webm"}
IMAGE = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
_model = None


def whisper():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("tiny.en", compute_type="int8")
    return _model


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=codec_type,width,height:stream_side_data=rotation",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    info = json.loads(out or "{}")
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    w, h = v.get("width", 0), v.get("height", 0)
    rot = next((abs(int(d.get("rotation", 0))) for d in v.get("side_data_list", []) if "rotation" in d), 0)
    if rot in (90, 270):
        w, h = h, w
    return (float(info.get("format", {}).get("duration", 0) or 0), w, h,
            any(s.get("codec_type") == "audio" for s in streams))


def spoken(path, duration):
    """Words spoken, from the first 60 s (VAD on, so music and room noise don't become words)."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-t", "60", "-i", str(path), "-vn",
                          "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    if len(audio) < 16000 * 0.5 or np.sqrt(np.mean(audio ** 2)) < 1e-4:
        return ""
    with _lock:  # one model, one transcription at a time
        segs, _ = whisper().transcribe(audio, vad_filter=True, language="en")
        return " ".join(s.text.strip() for s in segs).strip()


def video_thumbs(path, duration, fid, thumbs):
    names = []
    for k, frac in enumerate((0.15, 0.5, 0.85)):
        out = thumbs / f"{fid}_{k}.jpg"
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", f"{duration * frac:.2f}",
                        "-i", str(path), "-frames:v", "1", "-vf", "scale=360:-2", "-q:v", "4", str(out)])
        if out.exists():
            names.append(out.name)
    return names


def image_thumb(path, fid, thumbs):
    im = Image.open(path)
    im = im.convert("RGB")
    w, h = im.size
    im.thumbnail((360, 640))
    out = thumbs / f"{fid}_0.jpg"
    im.save(out, quality=80)
    return [out.name], w, h


def list_folder(folder_id):
    for attempt in range(3):
        try:
            files = gdown.download_folder(id=folder_id, skip_download=True, quiet=True) or []
            return [[f.id, f.path] for f in files]
        except Exception as e:  # rate limits, private folders
            print(f"  list failed ({e.__class__.__name__}: {str(e)[:120]}), retry {attempt + 1}", flush=True)
            time.sleep(10 * (attempt + 1))
    return None


def main(sources_path, out_dir):
    out_dir = Path(out_dir)
    thumbs = out_dir / "thumbs"
    thumbs.mkdir(parents=True, exist_ok=True)
    log = out_dir / "scan.jsonl"
    done = set()
    if log.exists():
        done = {json.loads(l)["id"] for l in log.read_text().splitlines() if l.strip()}
    sources = json.loads(Path(sources_path).read_text())
    for src in sources:
        if src.get("dropbox_url"):
            scan_dropbox(src, thumbs, log, done)
            continue
        files = src.get("files")
        if files is None:
            print(f"Listing {src['label']}...", flush=True)
            files = list_folder(src["drive_folder"])
            if files is None:
                with open(out_dir / "errors.jsonl", "a") as f:
                    f.write(json.dumps({"label": src["label"], "error": "could not list folder"}) + "\n")
                continue
        print(f"{src['label']}: {len(files)} files", flush=True)
        todo = [(fid, rel) for fid, rel in files if fid not in done and Path(rel).suffix.lower() in VIDEO | IMAGE]
        with ThreadPoolExecutor(WORKERS) as pool:
            for rec in pool.map(lambda f: scan_file(f[0], f[1], src, thumbs), todo):
                with open(log, "a") as f:
                    f.write(json.dumps(rec) + "\n")
                done.add(rec["id"])
                print(f"  {rec['kind']:8} {rec.get('duration', '')!s:>6} {rec['path']}", flush=True)


def scan_dropbox(src, thumbs, log, done):
    """A public Dropbox shared folder: download it as one zip, scan each file locally."""
    import hashlib
    import zipfile
    url = src["dropbox_url"].replace("dl=0", "dl=1")
    with tempfile.TemporaryDirectory() as tmp:
        z = Path(tmp) / "f.zip"
        print(f"Downloading {src['label']} (Dropbox zip)...", flush=True)
        r = subprocess.run(["curl", "-sSL", "-o", str(z), url], capture_output=True, text=True)
        if r.returncode or not zipfile.is_zipfile(z):
            with open(log.parent / "errors.jsonl", "a") as f:
                f.write(json.dumps({"label": src["label"], "error": "dropbox zip failed"}) + "\n")
            return
        with zipfile.ZipFile(z) as zf:
            names = [n for n in zf.namelist() if Path(n).suffix.lower() in VIDEO | IMAGE]
            print(f"{src['label']}: {len(names)} files", flush=True)
            for n in names:
                fid = "dbx-" + hashlib.md5((src["dropbox_url"] + n).encode()).hexdigest()[:16]
                if fid in done:
                    continue
                local = Path(tmp) / ("x" + Path(n).suffix.lower())
                local.write_bytes(zf.read(n))
                rec = scan_local(local, fid, n, src, thumbs)
                rec["link"] = src["dropbox_url"]
                local.unlink()
                with open(log, "a") as f:
                    f.write(json.dumps(rec) + "\n")
                done.add(fid)
                print(f"  {rec['kind']:8} {rec.get('duration', '')!s:>6} {n}", flush=True)


def scan_local(local, fid, rel, src, thumbs):
    ext = local.suffix.lower()
    rec = {"id": fid, "path": rel, "name": Path(rel).name, "source": src["label"], "brief": src.get("brief", ""),
           "creator": src.get("creator", ""), "notion": src.get("notion", ""), "mb": round(local.stat().st_size / 1e6, 1)}
    try:
        if ext in IMAGE:
            rec["thumbs"], w, h = image_thumb(local, fid, thumbs)
            rec.update(kind="image", width=w, height=h)
        else:
            dur, w, h, has_audio = probe(local)
            words = spoken(local, dur) if has_audio else ""
            n = len(words.split())
            rec.update(kind="broll" if n < 4 else "talking", duration=round(dur, 1), width=w, height=h,
                       has_audio=has_audio, words=words[:300], word_count=n, thumbs=video_thumbs(local, dur, fid, thumbs))
    except Exception as e:
        rec.update(kind="error", error=f"{e.__class__.__name__}: {str(e)[:200]}")
    return rec


def scan_file(fid, rel, src, thumbs):
    ext = Path(rel).suffix.lower()
    rec = {"id": fid, "path": rel, "name": Path(rel).name, "source": src["label"],
           "brief": src.get("brief", ""), "creator": src.get("creator", ""), "notion": src.get("notion", ""),
           "link": f"https://drive.google.com/file/d/{fid}/view"}
    with tempfile.TemporaryDirectory() as tmp:
        local = Path(tmp) / f"f{ext}"
        try:
            gdown.download(id=fid, output=str(local), quiet=True)
            if not local.exists() or local.stat().st_size == 0:
                raise RuntimeError("empty download")
            rec["mb"] = round(local.stat().st_size / 1e6, 1)
            if ext in IMAGE:
                rec["thumbs"], w, h = image_thumb(local, fid, thumbs)
                rec.update(kind="image", width=w, height=h)
            else:
                dur, w, h, has_audio = probe(local)
                words = spoken(local, dur) if has_audio else ""
                n = len(words.split())
                rec.update(kind="broll" if n < 4 else "talking", duration=round(dur, 1), width=w, height=h,
                           has_audio=has_audio, words=words[:300], word_count=n,
                           thumbs=video_thumbs(local, dur, fid, thumbs))
        except Exception as e:
            rec.update(kind="error", error=f"{e.__class__.__name__}: {str(e)[:200]}")
    return rec

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
