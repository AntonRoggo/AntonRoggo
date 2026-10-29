---
name: tt-ad-edit
description: Edit a talking-head ad for The Tallowed Truth (F-Balm) in the house style of our best ad, the "come clean" founder confession. Use when a creator or Ben's raw footage needs cutting into a 9:16 Meta ad with TTT captions, a hook banner, customer pop-ups and a review scroll; when asked to "cut this", "edit this ad", "make it look like the founder confession", or to check an edit against the TTT style.
---

# TTT ad edit (v1)

Built from a frame-by-frame breakdown of the founder confession ad (FBA1400B, CA$36 per purchase on CA$44K, the
account's #1 ad). The full breakdown, shot by shot, is in `reference/founder-confession.md`; read it before
your first edit.

## What you need

- The raw talking takes (9:16, the script filmed separately from any B-roll).
- The script or brief, so you know which take of each line is the keeper.
- Pop-up material for the proof moments: customer photos or clips, review screenshots or a screen recording of
  the reviews page. Find them with the brain: `testimonials/README.md`, `reviews/`, and
  `tools/review_card.py` for a review that has no screenshot yet.
- Fonts: Proxima Nova Semibold (captions), Proxima Nova Extrabold and Bold (banner).

## How to run an edit (creator footage in, edit out)

The editor is `tallowed-truth/tools/tt_edit.py` (it uses `edit_video.py` at the repo root for the cutting
engine). Needs ffmpeg and `pip install faster-whisper`.

1. **Get the footage.** Creators upload to the TTT BRAIN Drive folder `01 Creator Footage (upload here)`, one
   folder per creator per brief. Download the talking take(s) into `input/`. If the script was filmed in
   several files, join them in script order first.
2. **Plan pass** (no render): `python3 tallowed-truth/tools/tt_edit.py input/<take>.mp4 -o output/<name>/<name>.mp4 --plan-only`.
   It prints what it cut ("Cut words: ...") and writes `<name>.timeline.json`, the transcript on the edited
   timeline.
   - Read the cut words. The engine treats any immediate repeat as a stutter, so a deliberate repeat
     ("bang, bang, bang", "really, really") gets cut: put it back with `--keep START-END` (source seconds).
   - Fix misheard brand words with `--fix 'START-END=tallow balm'`.
   - Cut an outtake or aside the engine kept with `--drop START-END`.
3. **Pick the pop-ups.** Find the brief's proof moments in the timeline and write `popups.json` with the exact
   words they go under (see the format at the top of `tt_edit.py`): customer pairs, a review screenshot from
   `testimonials/`, or a review card by id. The tool snaps each one to the nearest cut.
4. **Render:** same command without `--plan-only`, plus `--headline "LINE ONE|line two"` and
   `--popups popups.json`. About 2 minutes for a 60 s video.
5. **Check it** against the checklist below: grab frames at the banner, every pop-up, and a few captions.
6. **Deliver.** Upload the MP4 with `python3 tools/dropbox_upload.py "/TTT Edits/<creator>" output/<name>/<name>.mp4`
   and send the link back with a one-line summary (length, cuts, pop-ups used).

Without Proxima Nova files in `fonts/` the tool falls back to Inter so a preview still renders; final edits
need the Proxima Nova files.

## The style in one paragraph

One person talking straight to camera the whole time, moving through real places with the real product or
ingredient in hand. Hard cuts every 3-6 s on sentence breaks, no transitions, no pauses. Small white
2-word captions locked to one spot. A white "news" banner for the first 3 s. Proof pops up exactly where the
captions are, at the moment the words claim it, and the captions step aside while it's up. Ends on money back
plus "link below" with a point down.

## Cutting

1. **Pick takes.** Keep the last clean take of each line. Cut stumbles, restarts, "um"s and dead air.
2. **First word on frame 1.** No lead-in, no breath, no logo. Last word ends 0.2 s before the video ends.
3. **Pauses.** Inside a shot, trim pauses to 0.25 s or less. Allow up to 0.5 s only while a pop-up is on and
   the speaker is listing things.
4. **Hard cuts only**, every one on a sentence or clause break. Jump cuts between takes in the same spot are
   fine (the ad has five). Never cut mid-word. Keep each cut tight to the speech, as in our other edits
   (`AUDIO_OVERLAP` 0.1 s, `J_CUT` 0.1 s).
5. **Shot length.** Aim for 3-6 s; 1-2 s for a short punch line ("Premium ingredients, premium results.").
   One long take (up to ~14 s) is fine only when the speaker is walking from one place or prop to the next:
   the movement does the work of a cut.
6. **New idea, new shot.** Change place, prop or framing when the script moves to the next point (each
   ingredient in the founder ad has its own stop).
7. **No B-roll cutaways.** Show things inside the talking shot (holding the tallow, standing over the honey).
   Cover the speaker only with pop-ups.
8. **Length.** 45-65 s. The founder ad is 64 s at 3.9 words a second.

## Captions

- Proxima Nova Semibold, 70 px at 1080x1920, white (#FFFFFF), 4 px black outline, plus a soft black drop
  shadow about 3 px down-right at ~60% opacity.
- All lowercase. Keep apostrophes ("i'll", "you've", "doesn't"); drop all other punctuation.
- 2 words per caption. One word if it's long ("antimicrobial"); 3 only if it fits easily. Never across a
  sentence or phrase break. Each caption is on screen exactly while its words are spoken.
- Centred, baseline at 68% of the height (y 1305). It never moves, whatever's behind it.
- **No captions while a pop-up is on screen.**
- Fix misheard words before burning in (brand words: "tallow", "The Tallowed Truth", "F-Balm", "tallow balm").

ASS style (`PlayResX: 1080`, `PlayResY: 1920`):

```
Style: TT,Proxima Nova Semibold,70,&H00FFFFFF,&H000000FF,&H00000000,&H66000000,0,0,0,0,100,100,0,0,1,4,3,2,40,40,600,1
```

Alignment 2 (bottom centre) with MarginV 600 puts the baseline at about y 1305 (MarginV measures to the bottom
of the line box, which sits about 15 px below the baseline at 70 px). Check it on the first render and adjust.

## Hook banner (first ~3 s)

- Flat white box, square corners, centred, 77% of the width (x 123-954), y 1107-1232, ~12 px padding.
- Line 1: the claim in caps, black Proxima Nova Extrabold ~70 px ("OFFICIAL STATEMENT").
- Line 2: who's speaking, black Proxima Nova Bold ~50 px ("from The Tallowed Truth Founder").
- On from frame 1 until the first pop-up (or ~3 s). Captions run directly underneath it.
- Swap the words to fit the speaker and the angle, keeping the same shape. For example, "HONEST REVIEW / from
  a 64-year-old nurse".

## Pop-ups

- **Timing:** each pop-up starts on a cut (or within 0.1 s of it), fades in over 0.3 s (a slight blur on the way
  in is fine) and ends with a hard cut. Length 2-8 s.
- **Place:** centred on the caption zone (y about 1050-1400), so the viewer's eye doesn't move.
- **Content matches the words.** When the speaker says people get results, show real people; when they say
  "the reviews say...", scroll the real reviews while they read them out.
- **Kinds used in the winner:**
  1. Two customer clips or photos side by side, each ~35% wide, thin dark border (at 3 s, for proof up top).
  2. A slow screen recording of the Judge.me reviews page in a white panel ~80% wide (late, for social proof).
     Leave in a 3-4 star review; it reads as real.
- Review cards (`tools/review_card.py`) and before/afters from `testimonials/` follow the same rules.
- Quote reviews word for word, and only show a customer's photo with their own review.

ffmpeg overlay for one pop-up (S = start, E = end, in seconds):

```
[1:v]scale=864:-1,format=rgba,setpts=PTS-STARTPTS+S/TB,fade=in:st=S:d=0.3:alpha=1[p];
[0:v][p]overlay=x=(W-w)/2:y=1230-h/2:enable='between(t,S,E)'
```

## Audio

- Voice only. Pull background noise down (RNNoise), then -12 LUFS, peaks at -1 dBTP. The founder ad delivered at
  -14 LUFS / -0.7 dBFS. No music.

## Script shape (the winner's order)

1. Hook that sounds like news or a confession (0-3 s), with the banner.
2. Proof flash: a real customer pop-up while the benefit is said (3-5 s).
3. Open loop: "Give me 60 seconds, I'll show you..." (5-9 s).
4. The body, one point per shot, each shown in hand and given a "not" (not bleached, not synthetic...).
5. "The truth is..." quality claim.
6. Social proof: review scroll while the speaker reads what reviews say.
7. Who it's for ("if you've tried a cheap tallow balm or a serum...").
8. Money-back guarantee, "click the link below", point down.

## Check before showing the edit

- [ ] First word on frame 1; no pause over 0.25 s (0.5 s under a pop-up); ends 0.2 s after the last word.
- [ ] Every cut on a sentence/clause break; no shot over 6 s unless the speaker is walking.
- [ ] Captions: Proxima Nova Semibold 70 px, white, 4 px outline + shadow, lowercase, apostrophes only,
      1-3 words, same spot all the way through, none under pop-ups, brand words spelled right.
- [ ] Banner on for the first ~3 s, captions directly under it.
- [ ] Every pop-up starts on a cut, fades in 0.3 s, ends on a cut, sits on the caption zone, and shows what's
      being said at that moment. Reviews word for word, photo matches the review.
- [ ] Product visible in most shots; held to the lens for the offer.
- [ ] Ends on money back + link below + point down.
- [ ] Audio -12 LUFS, peaks -1 dBTP, no music, no hiss.

## Lessons

- **Pick takes per script line** (from the founder ad's raw footage): for each line of the script, use the last
  complete, clean delivery, wherever it sits. Creators film many files (the founder ad: 8 hook takes, then one
  file per section, some with long botched attempts before the good one). The tool only catches short restarts
  on its own; a long failed attempt before a clean redo must be removed with `--drop`, or trim the file to the
  good take first. Read the transcript of every file before choosing.

- An immediate repeat isn't always a stutter. Read the cut-words list on every edit and restore deliberate
  repeats.

## Not known yet (v1)

The rules above come from the delivered ad only. These are guesses until confirmed: whether there's a quiet
music bed; the banner font weights; the exact shadow settings; how much raw footage was cut. See the questions
in the brain's `skills/README.md`.
