---
name: edit-legend
description: Edit a Lifestyle Legends reel (or any multi-clip reel with b-roll cutaways, screenshot pop-ups or a white title label) in the style of Anton's top-performing reels. Use when the user drops footage for a Lifestyle Legends script, asks to "edit the Fleming/London/Chouinard video", or wants a reel cut from several clips rather than one talking-head take.
---

# Edit a Lifestyle Legends reel

The style guide is `series/lifestyle-legends/EDITING_STYLE.md`, based on the reference reel "It's simple really". The scripts are in `series/lifestyle-legends/SCRIPTS.md`, and each script has a plan in `series/lifestyle-legends/plans/`.

## Steps

1. **Pick the plan.** Match the footage to a script, e.g. `fleming_2_sometimes_life_calls_for`. If the user filmed something that isn't one of the nine scripts, copy the closest plan to a new name and edit it.
2. **Check the footage** is in `input/<plan name>/` with the file names the plan uses. The editor lists any missing files; rename the user's files to match, or change the plan, rather than guessing which clip is which. If it's unclear, ask.
3. **Run a draft first:**
   ```bash
   python3 edit_legend.py series/lifestyle-legends/plans/<plan>.json --draft
   ```
4. **Check the draft.** Read the edited transcript the script prints, plus the cutaway and pop-up times. Grab frames at those times (`ffmpeg -ss <t> -i output/<plan>.mp4 -frames:v 1 frame.png`) and look at them. If a cutaway or pop-up is on the wrong word, fix `at` in the plan: `"swim#2"` means the second "swim", and a number means that many seconds in. Re-run.
5. **Render the final** without `--draft`. Use `--model medium` if the transcript had mistakes.
6. **Report** the output path, its length, and anything that was skipped, such as an anchor word that wasn't found.

Don't publish anything from here. Publishing happens through the `publish-metricool` skill, and only after the user approves the video.

## Plan reference

```json
{
  "footage": "input/fleming_3_please_do_not",
  "label": {"text": "Failed attempt at\nbeing a stockbroker", "until": "please"},
  "keep_case": ["Ian", "Fleming"],
  "sequence": [
    {"talk": "01_coldopen.mp4", "cut": false},
    {"broll": "dive.mp4", "in": 1.0, "out": 3.5, "sound": 1.0, "text": "optional caption"},
    {"talk": "02_talk.mp4"}
  ],
  "cutaways": [{"file": "snorkel.mp4", "at": "swim", "seconds": 1.5, "in": 0, "sound": 0}],
  "popups": [{"file": "fleming.jpg", "at": "Ian", "seconds": 2.5, "width": 0.6, "border": 6,
              "border_color": "black", "y": 0.6, "hide_captions": true}],
  "music": {"file": "track.mp3", "volume": 0.12}
}
```

- `talk` clips are transcribed, then fillers, retakes and silences over 1 s are cut. With `"cut": false` the whole take is kept.
- `broll` clips in the sequence are trimmed and keep their own sound.
- `cutaways` cover the picture while the voice keeps playing. `until` (a word) can replace `seconds`.
- `popups` can be images or videos.
- `keep_case` lists names that shouldn't be lowercased when they start a sentence.

The style constants (caption size and position, label, pop-up defaults) are at the top of `edit_legend.py`.
