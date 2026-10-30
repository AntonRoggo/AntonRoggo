---
name: edit-legend
description: Edit a Lifestyle Legends reel in the split-screen storyteller style (story photos on top with blue pill labels, Anton talking underneath, uppercase captions on the seam, guess-who pixelation, series end card). Use when the user drops footage for a Lifestyle Legends script, asks to "edit the London/Fleming/Chouinard video", or wants a story-about-a-famous-person reel cut from talk clips plus photos.
---

# Edit a Lifestyle Legends reel

These files cover the series:
- **Format and research:** `series/lifestyle-legends/FORMAT.md`
- **Look and reference video:** `series/lifestyle-legends/EDITING_STYLE.md`
- **Scripts:** `series/lifestyle-legends/SCRIPTS.md`, with one plan per script in `series/lifestyle-legends/plans/`

## Steps

1. **Pick the plan** that matches the footage, e.g. `london_b_guess`. For a legend or script that isn't one of the nine, copy the closest plan to a new name and edit its panels to match the new lines.
2. **Check the footage** is in `input/<plan name>/` with the file names the plan uses. The editor lists anything missing. If the user's files are named differently, rename them or change the plan, but ask if it isn't clear which clip or photo is which.
3. **Run a draft:**
   ```bash
   python3 edit_legend.py series/lifestyle-legends/plans/<plan>.json --draft
   ```
4. **Check the draft.**
   - Read the edited transcript and the panel table it prints. Any panel whose word wasn't said is skipped with a warning; fix its `at` (`"surf#2"` means the second "surf", a number means seconds in).
   - Grab frames at a few panel times (`ffmpeg -ss <t> -i output/<plan>.mp4 -frames:v 1 f.png`) and look at them: is the face in the bottom half, is the pixelation over the face, is the pill readable?
   - If the face is cut off, set `"aroll_crop_y"` in the plan (default 0.12; lower shows more headroom).
5. **Render the final** without `--draft`. Use `--model medium` if the transcript had mistakes.
6. **Report** the output path, its length, and anything that was skipped.

Don't publish from here. Publishing goes through the `publish-metricool` skill, and only after the user approves the video.

## Plan reference

```json
{
  "footage": "input/cousteau_b_guess",
  "series_tag": "Lifestyle Legends · Guess who #1",
  "highlight": ["guess", "jail"],
  "title": {"text": "Following Cousteau\nalong the Riviera", "until": "1936"},
  "aroll_crop_y": 0.12,
  "sequence": [{"talk": "01_talk.mp4"}, {"broll": "dive.mp4", "in": 1, "out": 4}],
  "panels": [
    {"at": "guess", "file": "portrait.jpg", "label": "Guess the legend", "censor": [0.25, 0.05, 0.5, 0.5]},
    {"at": "Japan", "file": "sealing_ship.jpg", "label": "Age 17"},
    {"at": "surf", "full": "surf.mp4", "label": "Optional pill"},
    {"at": "got", "full": "talk"}
  ],
  "end_card": {"at": "follow", "title": "Guess the Legend", "sub": "Next: a spy novelist"},
  "music": {"file": "bed.mp3", "volume": 0.12}
}
```

- `file` panels go in the top half. `"full": "<clip or photo>"` fills the whole screen; `"full": "talk"` shows you full screen.
- Photos get a slow zoom automatically. For video panels, `in` sets the start point within the clip.
- `censor` takes `[x, y, w, h]` as fractions of the panel, or a list of those boxes. It pixelates photos only.
- `focus` sets which part of a tall photo stays in the panel: 0 keeps the top (faces in full-length portraits), 0.5 the middle (default), 1 the bottom.
- Captions are uppercase. Numbers and `highlight` words turn yellow.
- `title` is the big opening title used by the In Their Footsteps format. It stays up until the `until` word, or for 5 s if there's no `until`.

## Cutting from one long clip with several takes

When the footage is one long recording with retakes, don't split it into files. Point each `talk` item at the best take with `in`/`out` seconds:

```json
"sequence": [{"talk": "t0010.MP4", "in": 12.9, "out": 15.9}, {"talk": "t0010.MP4", "in": 27.9, "out": 31.2}],
"fix": [["Yvonne", "Yvon"], ["forage", "forge"]],
"captions": {"style": "lower"}
```

- In and out points snap to the nearest pause in the audio (up to 0.6 s away), so they can be rough. Each picked line is transcribed on its own, so a retake next to it can't leak into the captions. Within a picked line only fillers and pauses over 0.7 s are cut. Repeats stay.
- Pick ranges by listening or from a transcript, then check with `--dry-run` before rendering: it prints each line's range, the transcript and the panel table in seconds, and the transcript shows any doubled take ("Then he built one of the biggest... Then he built..."). Move that line's `in` past the false start.
- `fix` corrects misheard words in the captions: `[wrong phrase, right phrase]`, matched case- and punctuation-blind.
- `captions.style` is `legend` (uppercase, on the seam; default) or `lower` (lowercase, smaller, lower third: used for the Do This reels).
- Transcripts are cached in `output/.cache`, so re-cutting the same clip skips transcription.
- Cuts made from real footage live in `series/lifestyle-legends/cuts/` (and `series/do-this/plans/`), not in `plans/`, because the script generator rewrites `plans/`. Image credits for the cuts are in `series/lifestyle-legends/CREDITS.md`.

The style constants (panel sizes, colours, caption size) are at the top of `edit_legend.py`. The scripts and their plans are generated from one source, `series/lifestyle-legends/tools/gen_scripts.py`. To change a line or a panel, edit it there and run `python3 series/lifestyle-legends/tools/gen_scripts.py`. The generator checks every cue word against its line, then rewrites `SCRIPTS.md` and `plans/`. Don't hand-edit the generated files.
