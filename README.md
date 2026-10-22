# Video editing

`edit_video.py` edits talking-head videos to these guidelines:

- **Captions:** Proxima Nova Semibold, 70px, white, 4px black stroke, 3 words on screen at a time, centred in the lower third
- **Cut mistakes:** filler words (um/uh), stutters, and botched takes (when a line is restarted, only the last take is kept)
- **Cut silences** longer than 1 second
- **Audio boosted** as loud as possible without clipping (-12 LUFS, peaks capped at -1 dBTP), with a 15ms fade on every cut so there are no pops

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

## Lifestyle Legends reels (multi-clip)

`edit_legend.py` cuts a split-screen storyteller reel, a format based on the top "story about a famous person" reels on Sandcastles:
- story photos and clips on top, with a blue pill label naming each beat
- you talking to camera underneath
- uppercase captions on the seam
- full-screen moments, guess-who pixelation, and a series end card

Each edit is driven by a plan file, and every panel starts on a spoken word:

```bash
python3 edit_legend.py series/lifestyle-legends/plans/london_a_origin.json --draft
# -> output/london_a_origin.mp4  (+ .ass caption file)
```

- Format and research: `series/lifestyle-legends/FORMAT.md`
- Style guide and reference video: `series/lifestyle-legends/EDITING_STYLE.md`
- Scripts: `series/lifestyle-legends/SCRIPTS.md` (Origin Story, Guess the Legend and In Their Footsteps for Cousteau and Chouinard, plus five options for legend 3; London and Fleming are already scripted)
- Editing breakdown of every reference reel: `series/lifestyle-legends/BREAKDOWNS.md`
- Put each script's footage in `input/<plan name>/`. The `edit-legend` skill runs the whole thing.

## Publishing (Metricool)

Once you approve an edited video, the `publish-metricool` skill schedules it on every platform connected in Metricool. Settings are in `publishing/config.json` and every scheduled post is logged in `publishing/log.md`. This needs the Metricool connector.
