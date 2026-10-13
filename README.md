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

## Review tool

Every edit lands in the review tool, a private page on claude.ai (link in `review/config.json`). Watch a cut, press **N** to drop a note at that exact moment, then **Apply notes**: Claude starts a session, re-edits, and uploads the next version next to the old one, with a reply on each note. **Compare** plays two versions side by side. **Approve vN** tells Claude to post that exact version.

Each note becomes a rule in `brand/editing-lessons.md`, and every review is mirrored to `reviews/<video>.md`, so the feedback history lives in git. How Claude runs the loop is in `.claude/skills/review/SKILL.md`; the page source is `review/index.html`.

- `tools/review_proxy.py` makes the review copy of an edit (under the 15 MB upload limit).
- `tools/review_sync.py` writes the database dump to `reviews/`.
- `tools/dropbox_api.py` uploads full-quality masters and finals to the Dropbox app folder and makes public links.

## Publishing (Metricool)

Once you approve an edited video, the `publish-metricool` skill schedules it on every platform connected in Metricool. Settings are in `publishing/config.json` and every scheduled post is logged in `publishing/log.md`. This needs the Metricool connector.
