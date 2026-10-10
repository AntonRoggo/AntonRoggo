# AntonRoggo brand brain

This repo is the source of truth for Anton's personal-brand content: how videos are edited, what the brand sounds like, what B-roll exists, and what has been posted. Media lives in Dropbox; only text lives here.

## Where things are

| What | Where |
|---|---|
| Edit a talking-head video (captions, mistake/silence cuts, audio boost) | `edit_video.py` (see README) |
| Boost audio only | `boost_audio.py`, skill `boost-audio` |
| Schedule an approved video on every platform | skill `publish-metricool`, settings in `publishing/config.json`, history in `publishing/log.md` |
| Brand voice, audience, content pillars, visual style | `brand/` |
| Lessons from Anton's feedback on past edits (read before every edit) | `brand/editing-lessons.md` |
| Activity clips (Anton/friends doing things) | `broll/action.json` |
| B-roll catalogue (best clips only, tagged) | `broll/catalog.json` |
| Raw footage and B-roll | Dropbox: `/[01] Clients/[03] Anton/ANTON MASTER BROLL` |

## Rules

- Edit style: Proxima Nova Semibold 70px, white with 4px black stroke, 3 words on screen, centred in the lower third. Cut mistakes and silences over 1s. Audio at -12 LUFS, peaks at -1 dBTP.
- Footage kinds: `broll` = scenery and small everyday moments used as overlays (only quality 4-5 make the catalogue). `action` = Anton or friends doing an activity (kitesurfing, surfing, hiking, climbing...), used to show what he's describing; judged on whether the activity is clear, not on beauty. `talking` = takes to camera.
- When picking clips, prefer the ones Anton already reuses most in finished edits (`used_count` in the catalogue, from `tools/clip_embed.py`), even if they aren't the prettiest. Example: the Montenegro clip of him sipping orange juice on a sunbed is one of his most used.
- Never post without Anton's explicit approval of that specific video. Posts go out 10 minutes after approval, Eastern time.
- Read files from Dropbox with the Dropbox connector (`download_link` gives a temporary URL). Never move, rename or delete Dropbox files without asking.
- Don't commit videos, fonts or other large media. Put working files in `input/` and `output/` (git-ignored).
- Before every edit, read `brand/editing-lessons.md` and follow every rule in it. After the edit, check the video against each rule before showing it.
- When Anton gives feedback on an edit, turn each point into a short, general rule in `brand/editing-lessons.md` (not just a fix for that one video), commit it, then fix the video.
- When Anton states a new preference ("always...", "never...", "I like..."), record it in the right file here and commit it, so future sessions know it.
