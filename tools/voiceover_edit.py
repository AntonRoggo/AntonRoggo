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
                                      # optional per shot: "zoom": 1.2, "y": 0.3 (punch-in, vertical anchor 0-1),
                                      #   "grade": "blue" (overrides the plan's grade for that shot)
  "tail": 7.0,                        # seconds of music-only picture after the voice ends
  "pad_in": 0.15, "pad_out": 0.3,     # optional: speech padding kept at every cut (defaults: edit_video.py)
  "overlap": 0.1,                     # optional: audio crossfade at every join (bigger = snappier joins)
  "max_pause": 0.7,                   # optional: pauses longer than this inside a segment are cut
  "voice_clean": "output/.../vocals.wav",   # optional: same recording with the noise already removed
                                      #   (e.g. demucs --two-stems vocals); used for the sound, while
                                      #   speech detection and timing still come from "voice"
  "detect": "output/.../vocals.wav",  # optional: file to find speech/pauses in (default "voice"); use
                                      #   the cleaned voice when background noise hides the pauses
  "speech_db": 22,                    # optional: speech = within this many dB of his speaking level
                                      #   (default 32, edit_video.py); lower finds shorter pauses
  "gate_db": -30,                     # optional: noise gate after denoising (threshold in dBFS of the
                                      #   -12 LUFS voice); residual noise between words drops ~20 dB
  "denoise": "strong",                # optional: full-strength RNNoise twice + firmer compressor
  "voice_gain": "linear",             # optional: fixed gain + limiter to -12 LUFS instead of loudnorm
                                      #   (which can go dynamic and lift the noise in every pause)
  "headline": "five things no one tells you about oysters",   # optional: title for the whole video,
                                      #   caption style but smaller, max 2 lines, in the upper area
                                      #   ("headline_size" px, default 58; "headline_y" centre, default 350)
  "grade": "natural",                 # optional colour grade after tone mapping (default "natural";
                                      #   "blue" = bluer water, "none" = off); shots can override it
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


def seed_speech_mask(path, speech_db):
    """edit_video.speech_mask with a stricter 'is he talking' threshold (seeds its cache, so
    detect_pauses/trim_to_speech use it). Needed when the pauses aren't quiet enough for the default."""
    import numpy as np
    sr, hop = 16000, 320
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-vn",
                          "-af", f"highpass=f=80,arnndn=m={DENOISE_MODEL}", "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32)
    n = len(a) // hop
    db = 20 * np.log10(np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    ev._speech_cache[path] = (db >= np.percentile(db, 90) - speech_db, hop / sr)


def build_segments(plan, voice):
    """Source ranges of the voice track, trimmed to speech and with long pauses removed.
    Returns [(a, b, hold)] where hold is extra silence after that range."""
    if plan.get("speech_db"):
        seed_speech_mask(voice, plan["speech_db"])
    ev.PAD_IN = plan.get("pad_in", ev.PAD_IN)       # (module globals read by trim_to_speech/cut_pauses)
    ev.PAD_OUT = plan.get("pad_out", ev.PAD_OUT)
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


OVERLAP = ev.AUDIO_OVERLAP     # set from the plan's "overlap" in main()


def offsets(segs, ov=None):
    """Output start time of every segment (crossfaded joins; holds add silence)."""
    ov = OVERLAP if ov is None else ov
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


# "denoise": "strong": RNNoise at full strength, twice, and a firmer compressor (for recordings with
# hiss/rumble left between words after the default PRE chain). Same EQ as boost_audio.PRE.
PRE_STRONG = (f"highpass=f=90,arnndn=m={DENOISE_MODEL}:mix=1,arnndn=m={DENOISE_MODEL}:mix=1,"
              "acompressor=threshold=-24dB:ratio=3:attack=5:release=150:makeup=1:knee=6,"
              "equalizer=f=3000:t=q:w=1.2:g=2,equalizer=f=250:t=q:w=1:g=-1.5")


def render_voice(voice, segs, out_wav, ov=ev.AUDIO_OVERLAP, gate_db=None, denoise=None, linear=False):
    """Denoise the whole recording first (so RNNoise has context), then cut and crossfade.
    gate_db: optional noise gate on the cleaned voice (pulls leftover noise between words down).
    denoise: "strong" uses PRE_STRONG instead of boost_audio.PRE.
    linear: bring the voice to -12 LUFS with one fixed gain + limiter. (loudnorm silently falls back to
    its dynamic mode when the gain would push peaks over 0 dBTP, and that mode lifts the background
    in every pause: heard as static coming in between lines.)"""
    gate = (f",agate=threshold={10 ** (gate_db / 20):.5f}:range={10 ** (-20 / 20):.4f}:ratio=4:attack=3:"
            f"release=120:knee=4" if gate_db is not None else "")
    pre = PRE_STRONG if denoise == "strong" else PRE
    with tempfile.TemporaryDirectory() as tmp:
        clean = Path(tmp) / "clean.wav"
        m = loudnorm_json(voice, pre)
        norm = (f"volume={TARGET_LUFS - float(m['input_i']):.2f}dB,aresample={SR * 4},"
                f"alimiter=limit={LIMIT:.4f}:attack=5:release=50:level=false,aresample={SR}"
                if linear else norm_chain(m))
        run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(voice), "-vn", "-af",
             f"{pre},{norm}{gate},atrim=start=0.015,asetpts=PTS-STARTPTS", "-ac", "1", "-ar", str(SR), str(clean)])
        f = ev.CUT_FADE
        parts = []
        for i, (a, b, hold) in enumerate(segs):
            parts.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={f},"
                         f"afade=t=out:st={b - a - f:.4f}:d={f}" + (f",apad=pad_dur={hold:.3f}" if hold else "") + f"[a{i}];")
        graph = "".join(parts) + ev.audio_join(len(segs), ov)
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


# Colour grades, applied after the HDR->Rec.709 tone mapping (plan "grade", per shot "grade"; "none" = off).
# "natural" (default): a gentle S-curve that keeps pure black/white where they are (no crushed blacks or
# blown highlights), ~1.1x saturation (vibrance first, so already-rich colours and skin aren't overdone),
# a touch of warmth in the mids for healthy skin, slightly richer blues and greener greens.
# "blue": natural plus bluer water/sky (cool shadows and mids, cyan-greens pulled toward blue).
GRADES = {
    "none": "",
    "natural": ("curves=all='0/0 0.25/0.235 0.5/0.5 0.75/0.765 1/1',vibrance=intensity=0.12,eq=saturation=1.06,"
                "colorbalance=rm=0.025:bm=-0.025:rh=0.01:bh=-0.01,huesaturation=colors=c+b:saturation=0.12,"
                "huesaturation=colors=g+y:hue=6:saturation=0.06"),
}
GRADES["blue"] = (GRADES["natural"] + ",colorbalance=rs=-0.03:bs=0.05:rm=-0.04:gm=-0.01:bm=0.06,"
                  "huesaturation=colors=c+g:hue=-12:saturation=0.08,huesaturation=colors=c+b:saturation=0.10")


def grade_filter(name):
    """Filter chain for a grade name (or a raw ffmpeg filter string), wrapped in RGB conversion."""
    chain = GRADES.get(name, name) if name else ""
    return f"format=gbrp,{chain},format=yuv420p," if chain else ""


def picture(shots, total, tmp, grade="natural"):
    """Every shot trimmed to whole frames and concatenated (frame-exact joins), tone-mapped and graded."""
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
              f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*{ya},setsar=1," + grade_filter(s.get("grade", grade)) +
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


HEADLINE_SIZE = 58     # px: smaller than the 70 px captions
HEADLINE_Y = 350       # centre of the headline block (upper area, clear of the IG top bar and the captions)


def add_headline(ass, text, total, size=HEADLINE_SIZE, y=HEADLINE_Y):
    """Put a title on screen for the whole video (list videos: "five things..."), in the caption
    style (lowercase, no punctuation, white with the black stroke), at most 2 balanced lines."""
    words = [w for w in (ev.caption_text(w) for w in text.split()) if w]
    if not words:
        return
    if len(" ".join(words)) > 22 and len(words) > 1:   # wrap into the two most balanced lines
        k = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
        body = " ".join(words[:k]) + r"\N" + " ".join(words[k:])
    else:
        body = " ".join(words)
    line = (f"Dialogue: 1,{ev.ass_time(0)},{ev.ass_time(total)},Default,,0,0,0,,"
            f"{{\\an5\\pos({W // 2},{y})\\fs{size}\\bord{ev.STROKE_PX}}}{body}")
    ass.write_text(ass.read_text(encoding="utf-8").rstrip("\n") + "\n" + line + "\n", encoding="utf-8")


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
    global OVERLAP
    OVERLAP = plan.get("overlap", ev.AUDIO_OVERLAP)
    segs = build_segments(plan, ROOT / plan["detect"] if plan.get("detect") else voice)
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
    if plan.get("headline"):
        add_headline(ass, plan["headline"], total, plan.get("headline_size", HEADLINE_SIZE),
                     plan.get("headline_y", HEADLINE_Y))
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        vwav, mwav, mix = Path(tmp) / "voice.wav", Path(tmp) / "music.wav", Path(tmp) / "mix.wav"
        render_voice(ROOT / plan["voice_clean"] if plan.get("voice_clean") else voice, segs, vwav,
                     OVERLAP, plan.get("gate_db"), plan.get("denoise"), plan.get("voice_gain") == "linear")
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
             (f"volume={TARGET_LUFS - float(m['input_i']):.2f}dB,aresample={SR * 4},alimiter=limit="
              f"{10 ** (-2.2 / 20):.4f}:attack=5:release=50:level=false,aresample={SR}"
              if plan.get("voice_gain") == "linear" else norm_chain(m, final=True)), str(mix)])
        listing = picture(shots, total, tmp, plan.get("grade", "natural"))
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
