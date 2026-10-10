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

## Boost audio only

```bash
python3 boost_audio.py some_video.mp4   # -> some_video_loud.mp4
```

Or ask Claude to "boost the audio" on a file: the `boost-audio` skill in `.claude/skills/` runs this.

## Publishing (Metricool)

Once you approve an edited video, the `publish-metricool` skill schedules it on every platform connected in Metricool. Settings are in `publishing/config.json` and every scheduled post is logged in `publishing/log.md`. This needs the Metricool connector.
