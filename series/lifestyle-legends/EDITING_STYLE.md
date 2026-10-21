# Lifestyle Legends: editing style

Every Lifestyle Legends reel is cut to match your own best-performing reels. `edit_legend.py` applies this style automatically from a plan file.

## Reference video

**"It's simple really"**: https://www.instagram.com/reel/DZF3QURNzQw/
1.18M views, 51× your average. A 9-second day in the life: hook on the sea wall, the dive, the swim, then "sit at the cafe and do absolutely nothing."

Each format also has a reference for the parts it adds:

| Format | Reference | Views / outlier | What it adds |
|---|---|---|---|
| A. Day in the life | It's simple really ([reel](https://www.instagram.com/reel/DZF3QURNzQw/)) | 1.18M / 51× | the base style |
|  | Sunday night lights ([reel](https://www.instagram.com/reel/DdiCL9OgLst/)) | 50K / 21× | a fast list of actions, one shot per action |
| B. Sometimes life calls for… | 48 oysters ([reel](https://www.instagram.com/reel/DcG_wOLABVr/)) | 180K / 69×, 9% engagement | screenshot "evidence" pop-ups over a seated take |
| C. Please do not… | Please do not spike my cortisol ([reel](https://www.instagram.com/reel/DZF3HAYtJ63/)) | 124K / 5.5× | skit cold open under a white label |

## What the reference reels have in common

I measured these from the downloaded reels (cut detection, transcripts, loudness, frame grabs).

**Camera**
- Ultra-wide action-cam or 0.5× look, held at arm's length or propped at waist height and slightly low.
- You're in frame from the head to the knees, with the location filling the rest of the frame.
- Golden-hour light, sea or a café behind you, linen or swim shorts.
- Vertical 9:16. The originals are 1440×2560; the editor delivers 1080×1920.

**Pacing**
- The first word lands at 0.0 s: no intro, no logo, no establishing shot.
- Speech runs at 2.4–3.8 words per second. The 48 oysters skit runs at about 1.7 because the deadpan beats are left in. Pauses under 1 s stay; anything longer is cut.
- Length depends on the format:
  - Day in the life: 9–20 s
  - Please do not: 12–20 s
  - Sometimes life calls for: 35–45 s

**Cuts**
- Only 1–4 cuts per video. Most of it is one continuous take.
- Cut only when the action or place changes (the dive, the café). Use hard cuts only: no transitions, zooms, shakes or effects.
- B-roll runs full screen for 1.5–3 s while your voice continues over it.

**Captions**
- Semibold sans (Proxima Nova Semibold), about 66 px on a 1080-wide frame ("and go for a swim" spans about half the width). That's small, like Instagram's native captions, not the big bouncing style.
- White fill, a thin black stroke (4 px) and a soft shadow.
- Centred mid-frame, at about 50% of the height, roughly at chest level.
- One short phrase on screen at a time, 2–4 words, broken where you'd naturally pause.
- Written lowercase as spoken ("wake up", "and go for a swim"). Full stops and commas are dropped; "why???" keeps its question marks.
- Captions stay on over b-roll and disappear while a pop-up card is on screen.

**Label** (format C only)
- A white box with black capital letters, two lines, above the captions: "FAILED ATTEMPT AT NOT SPIKING CORTISOL".
- It stays on through the cold open and disappears when the real talk starts.

**Pop-ups** (format B)
- A screenshot (study headline, chart, photo or book cover) shown as a card at 55–85% of the frame width, just below the middle of the frame.
- It stays 2–3 s, cutting in and out with no animation. A thin border is optional.

**Sound**
- Your voice with natural ambience (sea, café). The reels have no silent gaps, so there's always a bed of room or outdoor sound.
- The references sit at about -14 LUFS with peaks around -1 dBFS. The house pipeline goes to -12 LUFS / -1 dBTP, which is slightly louder and still clean.
- Music is optional and off unless the plan adds it. If you add a track, it's ducked under your voice.

## How the editor does it

`edit_legend.py` reads a plan from `series/lifestyle-legends/plans/` and runs these steps:

1. **Talk clips.** Each one is transcribed. Fillers, stutters, retakes and silences over 1 s are cut, using the same rules as `edit_video.py`. A clip marked `"cut": false` is kept whole, which is used for skit cold opens.
2. **B-roll clips** in the sequence are trimmed (`in`/`out`) and joined in order. Their natural sound is kept.
3. **Cutaways** are laid full screen over the talk, starting at a spoken word (`"at": "swim"`). Your voice keeps playing underneath.
4. **Pop-ups** are placed as cards at a spoken word, and captions are hidden while each one is up.
5. **The label** shows from the start until a word (`"until": "please"`) or a time.
6. **Captions** are added in the style above. The `.ass` caption file is kept next to the video so wording can be fixed by hand.
7. **Audio** goes through `boost_audio.py`: -12 LUFS, -1 dBTP, a 15 ms fade on every cut.

After every run, the editor prints the edited transcript with timestamps. If a cutaway lands in the wrong place, change its `at` word, using `swim#2` for the second time "swim" is said, or set `at` to a number of seconds.

## Shooting checklist

- [ ] Film on the wide lens, vertical, with the camera at chest to waist height.
- [ ] Start talking the instant you hit record, and say the hook first.
- [ ] Film each action (dive, surf, shucking oysters, typing) as its own 3–5 s clip. These become the cutaways.
- [ ] Get pop-up images as screenshots or photos you're allowed to use. Public-domain archive photos on Wikimedia Commons are fine; check the licence on each. For book covers, film yourself holding the book.
- [ ] Name the files as the script says and put them in `input/<plan name>/`.
