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
- Fonts: Proxima Nova Semibold (captions), Proxima Nova Extrabold and Bold (banner). The Semibold is in
  Dropbox `/[04] Video Editing Resources/fonts/`; put it in `fonts/` at the repo root (git-ignored).

## How to run an edit (creator footage in, edit out)

The editor is `tallowed-truth/tools/tt_edit.py` (it uses `edit_video.py` at the repo root for the cutting
engine). Needs ffmpeg and `pip install faster-whisper`.

1. **Get the footage.** Creators upload to the TTT BRAIN Drive folder `01 Creator Footage (upload here)`, one
   folder per creator per brief. Download the talking take(s) into `input/`. If the script was filmed in
   several files, join them in script order first.
2. **Check the story against the real review** if it's a customer story (see Lessons).
3. **Plan pass** (no render): `python3 tallowed-truth/tools/tt_edit.py input/<take>.mp4 -o output/<name>/<name>.mp4 --plan-only`.
   It writes `<name>.sentences.txt`, every sentence numbered with its source time, and marks likely false starts
   and fillers (`<- repeat/filler?`): suggestions only, nothing is cut automatically.
   - Read every sentence against the script and decide keep or drop (see Cutting). Drop with
     `--drop-sentence 0,3,23-24`. Fix misheard brand words with `--fix 'START-END=tallow balm'`.
   - Run the plan again: it prints every cut with the words either side of it.
4. **Send the sentence cut list to Anton before the first render** (which sentences go and why, every cut).
5. **Pick the pop-ups.** Write `popups.json` with the exact words they go under (format at the top of
   `tt_edit.py`). See Pop-ups and B-roll below.
6. **Render:** same command without `--plan-only`, plus `--hook "<text-on-screen hook>"` and
   `--popups popups.json`.
7. **Check it** against the checklist below, including playing 1 s either side of every cut.
8. **Deliver.** Upload the MP4 with `python3 tools/dropbox_upload.py "/TTT Edits/<creator>" output/<name>/<name>.mp4`
   and send the link back with a one-line summary (length, cuts, pop-ups used).

Without Proxima Nova files in `fonts/` the tool falls back to Inter so a preview still renders; final edits
need the Proxima Nova files.

## The style in one paragraph

One person talking straight to camera the whole time, moving through real places with the real product or
ingredient in hand. Hard cuts only between whole sentences, no transitions, no dead air. White 3-4 word
captions locked to one spot. A short text-on-screen hook above his head for the first 4 s. Proof pops up exactly where the
captions are, at the moment the words claim it, and the captions step aside while it's up. Ends on money back
plus "link below" with a point down.

## Cutting

Approved by Anton after Pat's esthetician edit (Oct 30 2026), where the automatic cutter made 23 cuts, most of
them mid-sentence, on breaths, or removing nothing.

1. **The sentence is the unit.** Cuts go between whole sentences, never inside one. Every kept sentence is
   finished; we never cut while he's speaking.
2. **Choose sentences, don't trim words.** Go through the sentence list against the script: keep or drop each
   one, with a reason (the best take, a false start, an aside, a wrong fact). When he messes up a sentence and
   says it again, drop the messed-up one and keep his redo. With no clean redo, keep it, or flag a reshoot. A
   sentence with a wrong fact comes out whole or stays; never splice around the fact.
3. **Pauses inside a sentence stay**, and so do pauses up to 0.7 s between sentences. Only silence over 0.7 s
   between two kept sentences is cut.
4. **A shot never opens on a breath.** It starts on the first word's sound (measured from the audio, not the
   transcript) and never reaches back into the word before it.
5. **No pointless cuts.** No cut that removes under 0.3 s, no shot under 1.5 s. A good continuous take stays
   continuous.
6. **Nothing is cut automatically.** The repeat/filler detector only suggests; check each one against the
   script. A repeat is often deliberate.
7. **Hard cuts only**, with the usual J-cut (`AUDIO_OVERLAP` 0.1 s, `J_CUT` 0.1 s). First word on frame 1, the
   video ends 0.2 s after the last word.
8. **Product in shot.** The tin in hand for most of it, held to the lens for the offer (that's filming; flag it
   to the creator if it's missing).
9. **Length.** Whatever the kept sentences make. The founder ad is 64 s; a told story runs longer. Shorten by
   dropping whole sentences, never by trimming inside them.

## Captions

- Proxima Nova Semibold, 70 px at 1080x1920, white (#FFFFFF), 4 px black outline, plus a soft black drop
  shadow about 3 px down-right at ~60% opacity.
- All lowercase. Keep apostrophes ("i'll", "you've", "doesn't"); drop all other punctuation.
- 3-4 words per caption (fewer if the sentence or phrase is shorter). A new caption starts at each new
  sentence or after a long pause. Never across a sentence or phrase break.
- **Timed to his voice:** each caption goes up as he starts the first word (measured from the audio; the
  transcript's word times are off by -0.1 to +0.3 s) and stays at least 0.4 s. Late captions read as lag.
- Centred, baseline at 68% of the height (y 1305). It never moves, whatever's behind it.
- **No captions while a pop-up is on screen.**
- Fix misheard words before burning in (brand words: "tallow", "The Tallowed Truth", "F-Balm", "tallow balm").

ASS style (`PlayResX: 1080`, `PlayResY: 1920`):

```
Style: TT,Proxima Nova Semibold,70,&H00FFFFFF,&H000000FF,&H00000000,&H66000000,0,0,0,0,100,100,0,0,1,4,3,2,40,40,600,1
```

Alignment 2 (bottom centre) with MarginV 600 puts the baseline at about y 1305 (MarginV measures to the bottom
of the line box, which sits about 15 px below the baseline at 70 px). Check it on the first render and adjust.

## Text-on-screen hook (first 4 s)

- **The words follow `rules/tos-hook-rules.md`:** 3-7 words, under 35 characters, a third party plus an exact
  age or number, ending in a colon for a story ("Esthetician shocked by 64 year old's skin:"). It must not
  repeat what the speaker says. Never a generic label ("REAL CUSTOMER STORY") and never the "OFFICIAL
  STATEMENT / from The Tallowed Truth Founder" shape (the us-vs-them pattern, highest CPAs) for a story ad.
- **Above his head**, around the forehead, so it never covers his face or the captions: black Proxima Nova
  Semibold on a white rounded box, one line (two if it must wrap). The tool finds the face and places it.
- On from frame 1 for 4 s. **No pop-up starts before it ends.**

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
- **A review pops up only when he says it's a review or message** ("she sent us this message", "we got a
  review"), as proof of what he's telling. Keep his words as he said them around it.
- **Show only the main point of the review, highlighted:** a sentence or two (`"from"` + `"max_chars"`) with
  the key words marked (`"highlight": "has never seen skin like mine"`). Nobody reads a paragraph in 3 s.
- **B-roll pop-ups, by what he's saying:**
  - Any time he describes F-Balm: the golden balm texture in warm or sunny light (open tin in sunlight on
    marble, fingertip scoop by a window).
  - "Cheap tallow" / "bleaching it": Michał's most-used clip of the white tallow being poured into a bucket
    (location to be added to the catalogue).
  - Quality, "we make it ourselves", premium ingredients: the open golden tins laid out in the factory
    (Anton's favourite).
  - Never the nozzle filling a tin.
  - All B-roll pop-ups the same size and shape: square crops of the subject at `"width": 0.6`.
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

- [ ] Play 1 s either side of every cut: each is between whole sentences, no breath at the start of a shot,
      no half word, nothing cut that removes under 0.3 s, no shot under 1.5 s.
- [ ] Every dropped sentence has a reason in the cut list sent to Anton.
- [ ] Captions: Proxima Nova Semibold 70 px, white, 4 px outline + shadow, lowercase, apostrophes only,
      3-4 words, new caption per sentence, up as he starts the word, none under pop-ups, brand words right.
- [ ] Text-on-screen hook passes `rules/tos-hook-rules.md`, sits above his head, up for 4 s, not cut off.
- [ ] Every pop-up fades in 0.3 s, sits on the caption zone, shows what's being said at that moment, and
      matches the B-roll list above. The review pops up only on "review"/"message", main point highlighted.
- [ ] Product visible in most shots; held to the lens for the offer.
- [ ] Ends on money back + link below + point down.
- [ ] Audio -12 LUFS, peaks -1 dBTP, no music, no hiss.

## Lessons

- **Pick takes per script line** (from the founder ad's raw footage): for each line of the script, use the last
  complete, clean delivery, wherever it sits. Creators film many files (the founder ad: 8 hook takes, then one
  file per section, some with long botched attempts before the good one). The tool only catches short restarts
  on its own; a long failed attempt before a clean redo must be removed with `--drop`, or trim the file to the
  good take first. Read the transcript of every file before choosing.

- **Check a story video against the real review before cutting it** (Pat's four authority stories, Oct 2026).
  Creators retell customer stories from memory and drift: a wrong name ("Jill" for Shari W.), a made-up
  timeline ("three months, every day" for "a month"), lines the customer never wrote, or two reviews merged
  into one. Find the review in `reviews/reviews.csv` (or `reviews/stories/`). Drop a sentence that's invented
  if the story still holds without it; otherwise keep what he says (Anton: the review on screen is the proof).
  Never splice inside a sentence to remove a detail. If too much is invented, ask for a reshoot.

- **Crop tall B-roll to the subject before using it as a pop-up.** A vertical clip shrunk into the caption
  zone is mostly background (the tin ends up at the bottom of a strip of curtain). Cut a short square crop
  around the subject with ffmpeg first, then use it at `"width": 0.6`.

## Not known yet (v1)

The rules above come from the delivered ad only. These are guesses until confirmed: whether there's a quiet
music bed; the banner font weights; the exact shadow settings; how much raw footage was cut. See the questions
in the brain's `skills/README.md`.
