# AntonRoggo brand brain

This repo is the source of truth for Anton's personal-brand content: how videos are edited, what the brand sounds like, what B-roll exists, and what has been posted. Media lives in Dropbox; only text lives here.

## Where things are

| What | Where |
|---|---|
| Edit a talking-head video (captions, mistake/silence cuts, audio boost) | `edit_video.py` (see README) |
| Boost audio only | `boost_audio.py`, skill `boost-audio` |
| Review loop: upload edits, read Anton's timestamped notes, apply them, handle approvals | skill `review`, review tool page `review/index.html` (URL in `review/config.json`), history in `reviews/` |
| Schedule an approved video on every platform | skill `publish-metricool`, settings in `publishing/config.json`, history in `publishing/log.md` |
| GoatBar.co (Anton's protein bar brand): design language, references, product, site, Instagram | `goatbar/CLAUDE.md` (start there) |
| Brand voice, audience, content pillars, visual style | `brand/` |
| Lessons from Anton's feedback on past edits (read before every edit) | `brand/editing-lessons.md` |
| Activity clips (Anton/friends doing things) | `broll/action.json` |
| B-roll catalogue (best clips only, tagged) | `broll/catalog.json` |
| Raw footage and B-roll | Dropbox: `/[01] Clients/[03] Anton/ANTON MASTER BROLL` |

## Rules

- Edit style: Proxima Nova Semibold 70px, white with 4px black stroke, all lowercase with no punctuation. Up to 3 words on screen, but a caption never crosses a sentence or phrase boundary (sentence flow beats the 3-word count). Captions are centred on screen; if that would cover his face they sit just below his chin. Cut mistakes and pauses over ~0.7s (detected from the audio); shorter pauses stay so it feels conversational. Clips are trimmed to where his voice starts/stops: never a silent shot of his face. Every cut is a J-cut with no pause: clips are trimmed tight to the words, the next clip's audio overlaps the previous one by 0.1s (`AUDIO_OVERLAP`) and the picture follows 0.1s later (`J_CUT`). B-roll starts/ends exactly on caption starts, frame-exact, never leaving less than 1.5s of camera between shots or next to a jump cut (B-roll runs on to the cut instead), and never in the first ~3s (the hook stays on his face). Audio: background noise pulled down (RNNoise) so his voice is clear, then -12 LUFS, peaks at -1 dBTP. Edits with B-roll get music by default (unless Anton says no song for that video): "charmed - stella" at -8 dB, first beat exactly on the first B-roll frame. Never use clips listed in `broll/banned.json`.
- Footage kinds: `broll` = scenery and small everyday moments used as overlays (only quality 4-5 make the catalogue). `action` = Anton or friends doing an activity (kitesurfing, surfing, hiking, climbing...), used to show what he's describing; judged on whether the activity is clear, not on beauty. `talking` = takes to camera.
- When picking clips, prefer the ones Anton already reuses most in finished edits (`used_count` in the catalogue, from `tools/clip_embed.py`), even if they aren't the prettiest. Example: the Montenegro clip of him sipping orange juice on a sunbed is one of his most used.
- Every finished edit goes into the review tool (skill `review`) as a new cut or version, with its recipe committed in `edits/` so any later session can rebuild it. Anton's notes there are feedback like any other: each becomes a rule in `brand/editing-lessons.md`.
- Never post without Anton's explicit approval of that specific video (saying so in chat, or pressing Approve on that version in the review tool). Posts go out 10 minutes after approval, Eastern time.
- Read files from Dropbox with the Dropbox connector (`download_link` gives a temporary URL). Never move, rename or delete Dropbox files without asking.
- Don't commit videos, fonts or other large media. Put working files in `input/` and `output/` (git-ignored).
- Before every edit, read `brand/editing-lessons.md` and follow every rule in it. After the edit, check the video against each rule before showing it.
- When Anton gives feedback on an edit, turn each point into a short, general rule in `brand/editing-lessons.md` (not just a fix for that one video), commit it, then fix the video.

## Always learning (every task, every session)

This repo is the brain. It only gets smarter if every rule Anton gives is written down and kept sharp.

- **Write every rule down, straight away.** Whenever Anton states a rule, preference or correction ("always…", "never…", "I like…", "don't…", "that's wrong", feedback on any output), record it in the same turn, before carrying on with the task:
  - Put it where the next session will read it: video editing → `brand/editing-lessons.md`; one client → that client's `clients/<client>/client.md` (Voice and rules) or `learnings.md`; one workflow → that skill's `SKILL.md`; how Claude works across everything → this file.
  - Write it as a short general rule, not a one-off fix: `- [date, context] Rule. (What he said.)`
- **Improve it, don't just append it.** If a rule already covers it, sharpen or merge that rule. If the new rule contradicts an old one, replace the old one (the newest instruction wins) and say what changed. Keep rule files short enough to read before every task.
- **Commit and push it**, then tell Anton in one line which rule was saved and where.
- **Learn from mistakes without being told.** When Anton corrects a result, or a task needed a fix, add or sharpen the rule that would have prevented it.
- **Learn from results.** When ad performance, review notes or call notes come in, add them to that client's `learnings.md`. When the same pattern shows up more than once, promote it to a rule.
