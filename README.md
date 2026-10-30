# Video editing

`edit_video.py` edits talking-head videos to these guidelines:

- **Captions:** Proxima Nova Semibold, 70px, white, 4px black stroke, 3 words on screen at a time, centred in the lower third
- **Cut mistakes:** filler words (um/uh), stutters, and botched takes (when a line is restarted, only the last take is kept)
- **Cut silences** longer than 1 second
- **Audio boosted** as loud as possible without clipping (-12 LUFS, peaks capped at -1 dBTP), with a 15ms fade on every cut so there are no pops

## Setup

```bash
pip install faster-whisper   # ffmpeg must also be installed
pip install mediapipe        # optional: face tracking for the Legends cuts
curl -L -o models/face_landmarker.task --create-dirs \
  https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
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
python3 edit_legend.py series/lifestyle-legends/plans/cousteau_a_origin.json --draft
# -> output/cousteau_a_origin.mp4  (+ .ass caption file)
```

- Format and research: `series/lifestyle-legends/FORMAT.md`
- Style guide and reference video: `series/lifestyle-legends/EDITING_STYLE.md`
- Scripts: `series/lifestyle-legends/SCRIPTS.md` (Cousteau, Chouinard and Hemingway: Origin Story, a 30 s short cut, Guess the Legend and In Their Footsteps, each built line for line on a winning reel, with three hooks per video)
- Editing breakdown of every reference reel: `series/lifestyle-legends/BREAKDOWNS.md`
- Put each script's footage in `input/<plan name>/`. The `edit-legend` skill runs the whole thing.
- Cuts from the real footage (Cousteau, Chouinard and Hemingway origin stories, filmed Oct 27): `series/lifestyle-legends/cuts/`. Each one picks the best take of every line from one long clip. Image credits to paste into the post caption are in `series/lifestyle-legends/CREDITS.md`.

Which Dropbox file each short clip name in these plans comes from: `series/FOOTAGE.md`.

## What to post (whole account)

`account/STRATEGY.md` covers all 583 reels: topics ranked, what to double down on and stop, and a 12-week plan with no restrictions. The per-reel table, with topic tags, is `account/data/all_reels.csv`.

`account/ADJACENT_IDEAS.md` has 9 next-door formats from Sandcastles 10× outliers (cinematic one-liners, nervous-system explainers, real food vs modern food, country reveals and more), each matched to footage already in Dropbox, with what to make first.

## "Do This" reels (quick format)

The one-line, talk-while-doing-it format behind most of the account's biggest reels:
- `series/do-this/ANALYSIS.md`: every 2025–26 reel transcribed and compared, winners vs losers in the format, outside winners from Sandcastles, and the rules
- `series/do-this/SCRIPTS.md`: 15 talk scripts, 7 text-on-clip posts and 3 oyster ad versions, with a plan to film them all in one morning
- `series/do-this/data/reels_2025_2026.csv`: one row per reel (link, views, outlier, length, format, first line)
- `series/do-this/plans/`: edit plans for the eight Do This reels filmed Oct 29, cut with `python3 edit_legend.py series/do-this/plans/<name>.json` (your take plus Costa Rica B-roll, lowercase captions)

## Publishing (Metricool)

Once you approve an edited video, the `publish-metricool` skill schedules it on every platform connected in Metricool. Settings are in `publishing/config.json` and every scheduled post is logged in `publishing/log.md`. This needs the Metricool connector.
