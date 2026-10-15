# Video editing

`edit_video.py` edits talking-head videos to these guidelines:

- **Captions:** Proxima Nova Semibold, 70px, white, 4px black stroke, 3 words on screen at a time, centred in the lower third
- **Cut mistakes:** filler words (um/uh), stutters, and botched takes (when a line is restarted, only the last take is kept)
- **Cut silences** longer than 1 second
- **J-cuts** on every cut: the next clip's audio starts 0.2s before its picture (`J_CUT`)
- **Audio boosted** as loud as possible without clipping (-12 LUFS, peaks capped at -1 dBTP), with a 15ms fade on every cut so there are no pops

## B-roll

The first run writes `output/<name>_edited.timeline.json` (the words with their times after cuts). Pick clips from `broll/catalog.json` / `broll/action.json`, download them to `input/broll/`, write a plan like
`[{"file": "input/broll/oj.mov", "start": 3.2, "end": 5.0, "clip_in": 1.5}]` and run again with `--broll plan.json`. Clips are scaled to fill the frame; captions stay on top.

## Setup

```bash
pip install faster-whisper   # ffmpeg must also be installed
```

Proxima Nova is a licensed font, so it isn't included. Put `ProximaNova-Semibold.otf` (or `.ttf`) in `fonts/`.

## Usage

```bash
python3 edit_video.py input/my_clip.mp4
# -> output/my_clip_edited.mp4  (+ output/my_clip_edited.ass, the editable caption file)
```

Use `--model medium` or `--model large-v3` for more accurate transcription.

## Voiceover over B-roll

`tools/voiceover_edit.py` edits videos with no talking head: a voiceover (Anton reading the
teleprompter, with retakes and pauses) laid over B-roll. Everything comes from a plan JSON
(examples in `edits/voiceover/`):

- `segments`: the source ranges of the voiceover to keep, in order (the best, usually last, take of
  each line; `"hold": 0.4` adds a silent beat for a "..."). Each is trimmed to the speech
  (0.15 s before, 0.3 s after), pauses over 0.7 s inside are cut, joins crossfade over 0.1 s.
- `shots`: B-roll, each running until the next starts. `"at"` is the caption it starts on (frame-exact)
  or a time (`"free": true` for music-only cuts); `"in"` is the clip time; optional `"zoom"`/`"y"` punch-in.
- `fix`: caption text for a word (by its source start time or text), e.g. `{"6.44": "1"}` to show
  numbers, `""` to merge a word into the previous one.
- `music` (song at -8 dB, first beat on frame 1, optional `"after"` level change) and `tail`
  (seconds of music-only picture after the voice).
- `grade`: colour grade applied to every shot after the HDR→Rec.709 tone mapping. On by default
  (`"natural"`); `"none"` turns it off, and a shot can override it (`"grade": "blue"` for water shots).
  `natural` = gentle S-curve that keeps black and white points (no crushed blacks or blown
  highlights), ~1.1x saturation (vibrance first, so skin isn't overdone), a little warmth in the mids
  for healthy skin, slightly richer blues and greener greens. `blue` = natural plus cooler mids and
  shadows and cyan-greens pulled toward blue, so brown-green shallow water reads blue. Presets live
  in `GRADES` in the tool; a raw ffmpeg filter string also works.
- `headline`: title on screen for the whole video (list videos, "five things..."), caption style at
  58 px, max 2 lines, centred at y=350 (`headline_size` / `headline_y` to change).
- Noisy voiceovers (knife sounds, chatter): separate the voice with
  `demucs -n htdemucs --two-stems=vocals`, then point `voice_clean` (the sound) and `detect` (where
  speech and pauses are found) at the vocals file; `speech_db: 22` finds pauses the default misses,
  `gate_db` gates the gaps. Voiceovers run tight: `max_pause` ~0.25 so no pause between lines.
- Hiss or "static" between lines: `"denoise": "strong"` (full-strength RNNoise twice, firmer
  compressor) and `"voice_gain": "linear"` (one fixed gain + limiter to -12 LUFS, for the voice and
  the final mix). Without it, loudnorm drops into its dynamic mode whenever the gain would push peaks
  past 0 dBTP, and that mode lifts the background in every pause. Add `gate_db` (e.g. -34) on top.

```bash
python3 tools/voiceover_edit.py edits/voiceover/2_gatekeep.json --preview   # captions + shot times
python3 tools/voiceover_edit.py edits/voiceover/2_gatekeep.json             # render
```

Transcribe the voiceover first with faster-whisper (word timestamps) per speech chunk; the plan's
`words` points at that JSON. Voice gets RNNoise + -12 LUFS; the final mix is -12 LUFS, -1 dBTP.
Captions use the edit_video.py house style.

## Boost audio only

```bash
python3 boost_audio.py some_video.mp4   # -> some_video_loud.mp4
```

Or ask Claude to "boost the audio" on a file: the `boost-audio` skill in `.claude/skills/` runs this.

## Publishing (Metricool)

Once you approve an edited video, the `publish-metricool` skill schedules it on every platform connected in Metricool. Settings are in `publishing/config.json` and every scheduled post is logged in `publishing/log.md`. This needs the Metricool connector.
