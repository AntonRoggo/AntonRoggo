"""Continue a finished edit's background music past its end, for clips appended after it.

  python3 tools/music_bed.py <music_stem.wav> <cut_seconds> <length_seconds> <out.wav> [--song song.mp3]

<music_stem.wav> is the edit's music on its own (from demucs: `--two-stems=vocals`, the
no_vocals file). The bed starts exactly at <cut_seconds> of the edit's timeline and lasts
<length_seconds>, at the same level the music had in the edit.

--song: the original track (e.g. "charmed - stella"). If the stem matches it, the song is
continued from the exact sample. Otherwise (or without --song) the stem is continued with a
loop splice: jump back to the earlier moment whose preceding 3 s sound most like the 3 s
before the cut, so the music carries on seamlessly. Prints the method used, or "no music"
(and writes silence) if the stem is essentially empty.
"""
import argparse, subprocess, sys
import numpy as np

SR = 44100


def load(path):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(path), "-ac", "2",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def chroma(mono, hop=441, n=4096):
    """12-bin chroma per 10 ms frame, unit-normalised."""
    frames = np.lib.stride_tricks.sliding_window_view(np.pad(mono, (0, n)), n)[::hop]
    spec = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1))
    f = np.fft.rfftfreq(n, 1 / SR)
    band = (f > 60) & (f < 4000)
    pc = (np.round(12 * np.log2(f[band] / 440)) % 12).astype(int)
    c = np.stack([spec[:, band][:, pc == k].sum(1) for k in range(12)], 1)
    c = np.log1p(c)
    c -= c.mean(1, keepdims=True)
    return c / (np.linalg.norm(c, axis=1, keepdims=True) + 1e-9)


def rms(x):
    return float(np.sqrt((x ** 2).mean()) + 1e-12)


def song_offset(stem, song, cut):
    """Seconds into the song that play at time 0 of the edit, judged on the 8 s before the
    cut; None if the stem isn't this song."""
    a, b = max(0, cut - 8), cut
    seg = chroma(stem[int(a * SR):int(b * SR)].mean(1))
    full = chroma(song.mean(1))
    w = len(seg)
    scores = np.array([(full[o:o + w] * seg).sum() / w for o in range(0, len(full) - w)])
    o = int(scores.argmax())
    if scores.max() < 0.55:
        return None
    # refine to the sample with waveform cross-correlation (+-15 ms)
    coarse = o * 441 - int(a * SR)                       # song sample at edit sample 0
    x = stem[int(a * SR):int(b * SR)].mean(1)
    best, lag = -1, coarse
    for d in range(-660, 661, 2):
        s0 = int(a * SR) + coarse + d
        if s0 < 0 or s0 + len(x) > len(song):
            continue
        y = song[s0:s0 + len(x)].mean(1)
        c = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9))
        if c > best:
            best, lag = c, coarse + d
    return lag / SR


def splice_point(stem, cut, ctx=3.0):
    """Earlier time t whose preceding ctx seconds best match the ctx seconds before the cut."""
    c = chroma(stem[:int(cut * SR)].mean(1))
    w = int(ctx * 100)
    ref = c[-w:]
    best, t = -1, None
    for e in range(w, len(c) - w - 100):                 # leave >=1 s before the cut
        s = (c[e - w:e] * ref).sum() / w
        if s > best:
            best, t = s, e / 100
    return t, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("cut", type=float); ap.add_argument("length", type=float)
    ap.add_argument("out"); ap.add_argument("--song")
    a = ap.parse_args()
    stem = load(a.stem)
    n = int(a.length * SR)
    tail = stem[max(0, int((a.cut - 5) * SR)):int(a.cut * SR)]
    if rms(tail) < 10 ** (-45 / 20):
        bed, how = np.zeros((n, 2)), "no music"
    else:
        bed, how = None, None
        if a.song:
            song = load(a.song)
            off = song_offset(stem, song, a.cut)
            if off is not None:
                s0 = int((a.cut + off) * SR)
                ref = song[s0 - len(tail):s0]
                gain = rms(tail) / rms(ref)
                bed = song[s0:s0 + n] * gain
                if len(bed) < n:
                    bed = np.pad(bed, ((0, n - len(bed)), (0, 0)))
                how = f"song continued from {a.cut + off:.2f}s, gain {20 * np.log10(gain):+.1f} dB"
        if bed is None:
            t, score = splice_point(stem, a.cut)
            src = stem[int(t * SR):]
            reps = int(np.ceil(n / max(1, len(src))))
            bed = np.concatenate([src] * max(1, reps))[:n] if len(src) else np.zeros((n, 2))
            how = f"loop splice from {t:.2f}s (match {score:.2f})"
    fade = int(0.6 * SR)
    bed[-fade:] *= np.linspace(1, 0, fade)[:, None]
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2",
                    "-i", "-", a.out], input=bed.astype(np.float32).tobytes(), check=True)
    print(how)


if __name__ == "__main__":
    main()
