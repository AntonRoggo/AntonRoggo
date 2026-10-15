#!/usr/bin/env python3
"""Edit a voiceover-over-B-roll video (no talking head) from a plan JSON.

  python3 tools/voiceover_edit.py plan.json [--preview]

Plan (times are seconds; "src" times are in the voiceover file):
{
  "voice": "input/voiceovers/2_gatekeep.m4a",
  "words": "output/voiceover/work/2_gatekeep.words.json",   # faster-whisper words (cached)
  "out": "output/voiceover/2_gatekeep.mp4",
  "segments": [                       # the voice track, in order: the best take of each line
    {"src": [12.3, 15.9], "hold": 0.4, "note": "line 2, take 3"},   # hold = extra silent beat after it ("...")
    ...
  ],
  "fix": {"9": "nine"},               # optional caption text for words (by start time, see below)
  "shots": [                          # picture: each shot runs until the next one starts
    {"file": "input/vo_broll/px/a0743_34.mp4", "at": 0, "in": 0.0},
    {"file": "...", "at": "so i flew", "in": 2.1},       # "at" = caption that starts with these words,
    {"file": "...", "at": 12.4, "in": 0.5}               #   or an output time (snapped to a caption start
  ],                                                    #   unless "free": true, e.g. music-only cuts)
                                      # optional per shot: "zoom": 1.2, "y": 0.3 (punch-in, vertical anchor 0-1)
  "tail": 7.0,                        # seconds of music-only picture after the voice ends
  "music": {"file": "input/shortform/music/charmed - stella.mp3", "db": -8,
            "after": {"at": 14.2, "db": -1}}   # optional: music level change (e.g. music carries the end)
}

The voice is cut tight with the edit_video.py rules: every segment is trimmed to where speech
starts/stops (PAD_IN before, PAD_OUT after), pauses longer than "max_pause" (default 0.7 s)
inside a segment are cut, and joins crossfade over AUDIO_OVERLAP. Noise is pulled down with
RNNoise and the voice brought to -12 LUFS (boost_audio.py); music goes under it at -8 dB with
its first beat on the first frame; the final mix is -12 LUFS with peaks under -1 dBTP.
Captions use the house style (edit_video.py: lowercase, no punctuation, <=3 words, never across
a phrase, centred at one height, "..." during silent beats).

"fix" maps a word's source start time (rounded to 2 decimals, as a string) or its text (lowercase,
no punctuation) to the caption text, e.g. {"one": "1"} to show numbers.
Writes <out>, <out>.ass, <out>.shots.json (final shot list) and, with --preview, nothing else.
"""
import argparse
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import edit_video as ev  # noqa: E402
from boost_audio import DENOISE_MODEL, LIMIT, PRE, TARGET_LUFS  # noqa: E402

FPS = 30
W, H = 1080, 1920
SR = 48000


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def loudnorm_json(path, af=""):
    err = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-vn", "-af",
                          (af + "," if af else "") + f"loudnorm=I={TARGET_LUFS}:TP=0:LRA=20:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err).group(0))


def norm_chain(m, final=False):
    """Linear gain to -12 LUFS, then a limiter. The final mix is limited at 4x oversampling with a
    lower ceiling, so true peaks stay under -1 dBTP after AAC encoding."""
    lim = (f"aresample={SR * 4},alimiter=limit={10 ** (-2.2 / 20):.4f}:attack=5:release=50:level=false,"
           f"aresample={SR}") if final else f"aresample={SR},alimiter=limit={LIMIT:.4f}:attack=5:release=50:level=false"
    return (f"loudnorm=I={TARGET_LUFS}:TP=0:LRA=20:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
            f"linear=true,{lim}")


def build_segments(plan, voice):
    """Source ranges of the voice track, trimmed to speech and with long pauses removed.
    Returns [(a, b, hold)] where hold is extra silence after that range."""
    max_pause = plan.get("max_pause", ev.MAX_PAUSE)
    pauses = ev.detect_pauses(voice, max_pause)
    out = []
    for seg in plan["segments"]:
        a, b = seg["src"]
        pieces = ev.trim_to_speech(ev.cut_pauses([(a, b)], pauses), voice)
        if not pieces:
            raise SystemExit(f"segment {seg} has no speech")
        if seg.get("keep_start"):        # don't let speech trimming move the start (soft first sound)
            pieces[0] = (min(pieces[0][0], a), pieces[0][1])
        for k, (s, e) in enumerate(pieces):
            out.append((s, e, seg.get("hold", 0.0) if k == len(pieces) - 1 else 0.0))
    return out


def offsets(segs, ov=ev.AUDIO_OVERLAP):
    """Output start time of every segment (crossfaded joins; holds add silence)."""
    t, offs = 0.0, []
    for a, b, hold in segs:
        offs.append(t)
        t += (b - a) + hold - ov
    return offs, t + ov


def map_words(words, segs, fix):
    """Words inside the kept ranges, on the output timeline: [{text,start,end}]."""
    offs, _ = offsets(segs)
    out = []
    for w in words:
        # the segment that holds most of the word (whisper often starts a word early, so its
        # middle can fall just before a segment that starts at the speech)
        ov = [min(b, w["end"]) - max(a, w["start"]) for a, b, _ in segs]
        best = max(range(len(segs)), key=lambda i: ov[i])
        if ov[best] < min(0.03, w["end"] - w["start"]) - 1e-6:   # (zero-length words count if inside)
            continue
        for k, ((a, b, _), o) in enumerate(zip(segs, offs)):
            if k == best:
                text = w["text"]
                key_t, key_w = f"{w['start']:.2f}", ev.caption_text(text)
                new = fix.get(key_t, fix.get(key_w))
                if new == "":            # word merged into the previous caption word ("gate" "keep")
                    if out and text[-1:] in ".,?!:;":
                        out[-1]["text"] += text[-1]
                    break
                if new is not None:
                    text = new + (text[-1] if text[-1:] in ".,?!" else "")
                # the speech model often starts the first word after a silence a few tenths
                # early; never before the speech itself (the kept range starts PAD_IN before it)
                start = max(w["start"], a + ev.PAD_IN * 0.8)
                out.append({"text": text, "start": o + start - a,
                            "end": o + max(start + 0.05, min(b, w["end"])) - a})
                break
    return out


def render_voice(voice, segs, out_wav):
    """Denoise the whole recording first (so RNNoise has context), then cut and crossfade."""
    with tempfile.TemporaryDirectory() as tmp:
        clean = Path(tmp) / "clean.wav"
        m = loudnorm_json(voice, PRE)
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(voice), "-vn", "-af",
             f"{PRE},{norm_chain(m)},atrim=start=0.015,asetpts=PTS-STARTPTS", "-ac", "1", "-ar", str(SR), str(clean)])
        f = ev.CUT_FADE
        parts = []
        for i, (a, b, hold) in enumerate(segs):
            parts.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={f},"
                         f"afade=t=out:st={b - a - f:.4f}:d={f}" + (f",apad=pad_dur={hold:.3f}" if hold else "") + f"[a{i}];")
        graph = "".join(parts) + ev.audio_join(len(segs))
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(clean), "-filter_complex", graph,
             "-map", "[ac]", "-ar", str(SR), str(out_wav)])


def snap_shots(plan, captions, total):
    starts = [t for t, _ in captions]

    def resolve(at):
        if isinstance(at, str):
            p = ev.caption_text(at)
            hits = [t for t, txt in captions if txt.startswith(p)]
            if not hits:
                raise SystemExit(f"shot anchor not found in captions: {at!r}")
            return hits[0]
        return at

    shots = []
    for s in plan["shots"]:
        t = resolve(s["at"])
        if not s.get("free") and not isinstance(s["at"], str) and t > 0:
            t = min(starts, key=lambda c: abs(c - t)) if t <= starts[-1] + 1 else t
        shots.append(dict(s, start=t))
    shots.sort(key=lambda s: s["start"])
    shots[0]["start"] = 0.0
    for i, s in enumerate(shots):
        s["end"] = shots[i + 1]["start"] if i + 1 < len(shots) else total
    return shots


def hdr_to_sdr(path):
    """iPhone/DJI HDR clips (HLG or PQ, BT.2020) look washed out and overexposed if they're
    just rescaled: tone-map them to Rec.709 first. Returns a filter prefix ('' for SDR)."""
    trc = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer",
               "-of", "csv=p=0", str(path)]).stdout.strip()
    if trc not in ("arib-std-b67", "smpte2084"):
        return ""
    return (f"zscale=tin={trc}:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
            "tonemap=hable:desat=0:peak=4,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")


def picture(shots, total, tmp):
    """Every shot trimmed to whole frames and concatenated (frame-exact joins)."""
    frame = lambda t: int(math.ceil(t * FPS - 1e-6))
    total_f = int(round(total * FPS))
    listing = []
    for i, s in enumerate(shots):
        f0, f1 = frame(s["start"]), min(frame(s["end"]), total_f) if i + 1 < len(shots) else total_f
        n = f1 - f0
        if n <= 0:
            continue
        length = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            s["file"]]).stdout)
        if s.get("in", 0) + n / FPS > length + 1e-3:
            print(f"WARNING: {s['file']} runs out ({s.get('in', 0):.2f}+{n / FPS:.2f} > {length:.2f}); last frame held",
                  file=sys.stderr)
        p = Path(tmp) / f"shot{i:02d}.mp4"
        z, ya = s.get("zoom", 1.0), s.get("y", 0.5)   # punch-in (e.g. to crop a finger off the edge)
        zw, zh = int(round(W * z / 2) * 2), int(round(H * z / 2) * 2)
        vf = (hdr_to_sdr(s["file"]) + f"fps={FPS},scale={zw}:{zh}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*{ya},setsar=1,"
              f"tpad=stop_mode=clone:stop_duration=3,trim=end_frame={n},setpts=PTS-STARTPTS")
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", f"{s.get('in', 0):.4f}", "-i", s["file"],
             "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", str(p)])
        listing.append(f"file '{p.name}'")
        s["frames"] = [f0, f0 + n]
    (Path(tmp) / "list.txt").write_text("\n".join(listing) + "\n")
    return Path(tmp) / "list.txt"


def music_track(music, total, voice_end, out_wav):
    gain = music.get("db", ev.MUSIC_DB)
    beat = ev.first_beat(music["file"])
    start = music.get("start", 0.0)        # output time of the first beat
    place = (f"adelay={int(round((start - beat) * 1000))}:all=1" if start >= beat
             else f"atrim=start={beat - start:.3f},asetpts=PTS-STARTPTS")
    vol = f"volume={gain}dB"
    if music.get("after"):
        t0, g1, ramp = music["after"]["at"], music["after"]["db"], music["after"].get("ramp", 0.3)
        a0, a1 = 10 ** (gain / 20), 10 ** (g1 / 20)
        vol = f"volume='if(lt(t,{t0}),{a0},if(lt(t,{t0 + ramp}),{a0}+({a1}-{a0})*(t-{t0})/{ramp},{a1}))':eval=frame"
    fade = music.get("fade", 0.5)
    run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", music["file"], "-af",
         f"aresample={SR},{place},{vol},apad,atrim=end={total:.3f},afade=t=out:st={total - fade:.3f}:d={fade}",
         "-ac", "2", str(out_wav)])
    return beat


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", type=Path)
    ap.add_argument("--preview", action="store_true", help="print segments, captions and shots; don't render")
    a = ap.parse_args()
    plan = json.loads(a.plan.read_text())
    voice = ROOT / plan["voice"]
    out = ROOT / plan["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    words = json.loads((ROOT / plan["words"]).read_text())
    segs = build_segments(plan, voice)
    _, voice_len = offsets(segs)
    total = round((voice_len + plan.get("tail", 0.0)) * FPS) / FPS
    timed = map_words(words, segs, plan.get("fix", {}))
    kept, keep = timed, [(0.0, total)]
    chunks = ev.caption_chunks(ev.timed_words(kept, keep))
    captions = [(round(c[0][0], 3), " ".join(t for t in (ev.caption_text(w) for _, _, w in c) if t)) for c in chunks]
    print(f"voice {voice_len:.2f}s, total {total:.2f}s, {len(segs)} audio pieces")
    for (s, e, h) in segs:
        print(f"  src {s:7.2f}-{e:7.2f}" + (f" +{h}s beat" if h else ""))
    for t, txt in captions:
        print(f"  {t:6.2f}  {txt}")
    shots = snap_shots(plan, captions, total)
    for s in shots:
        print(f"  shot {s['start']:6.2f}-{s['end']:6.2f}  {Path(s['file']).name} in={s.get('in', 0)}")
    if a.preview:
        return
    ass = out.with_suffix(".ass")
    ev.write_captions(kept, keep, W, H, ass)
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        vwav, mwav, mix = Path(tmp) / "voice.wav", Path(tmp) / "music.wav", Path(tmp) / "mix.wav"
        render_voice(voice, segs, vwav)
        graph = f"[0:a]aresample={SR},apad,atrim=end={total:.4f}[v];"
        inputs = ["-i", str(vwav)]
        if plan.get("music"):
            music_track(plan["music"], total, voice_len, mwav)
            inputs += ["-i", str(mwav)]
            graph += "[1:a]anull[m];[v][m]amix=inputs=2:normalize=0:duration=first[x]"
        else:
            graph += "[v]anull[x]"
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *inputs, "-filter_complex", graph, "-map", "[x]",
             "-ac", "2", str(Path(tmp) / "raw_mix.wav")])
        m = loudnorm_json(Path(tmp) / "raw_mix.wav")
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(Path(tmp) / "raw_mix.wav"), "-af",
             norm_chain(m, final=True), str(mix)])
        listing = picture(shots, total, tmp)
        assf = str(ass).replace("\\", "/").replace(":", r"\:")
        fonts = str(ev.FONTS_DIR).replace(":", r"\:")
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
             "-i", str(mix), "-filter_complex", f"[0:v]ass='{assf}':fontsdir='{fonts}'[vo]", "-map", "[vo]",
             "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
             "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.4f}", "-movflags", "+faststart", str(out)])
    out.with_suffix(".shots.json").write_text(json.dumps(
        [{k: s[k] for k in ("file", "start", "end", "in", "frames") if k in s} for s in shots], indent=1))
    print(f"Done: {out}")


if __name__ == "__main__":
    main()
