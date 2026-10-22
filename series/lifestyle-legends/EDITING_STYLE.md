# Lifestyle Legends: editing style

The look comes from the top story-about-a-famous-person reels on Sandcastles (see [FORMAT.md](FORMAT.md)), not from your own videos. `edit_legend.py` applies it from a plan file.

## Reference video

**Layout:** "Can you guess this footballer from the story of their career?" by @jackgrimse, https://www.instagram.com/reel/DdjfzUURsA3/ (97K views, 12× the channel average).
It's a split screen: the story visual on top with a blue label naming the beat, the storyteller talking to camera underneath, and captions on the seam between them. It's the easiest layout to make and edit week after week, and it suits all three formats.

**Captions and ending:** Lens on Legends, Dua Lipa, https://www.instagram.com/reel/DYul8wohxIL/ (735K views, 259×). Heavy uppercase captions with keywords in colour, the subject's name tagged at the start, and a branded series card at the end.

## What I measured

The full shot-by-shot breakdown of all seven references is in [BREAKDOWNS.md](BREAKDOWNS.md).

I downloaded the references and measured them for cuts, loudness, layout and frame grabs.

| | Guess the footballer | Lens on Legends | Alan Bond (glasshouse) |
|---|---|---|---|
| Length | 62 s | 2 min+ | 2 min 49 s |
| Hard cuts | 11, plus a new top image each sentence (about 2.5 s) | 29, a new image every ~4 s | 1 (motion-graphics dossier) |
| Layout | header strip 5%, top panel 42%, talking head 53% | full-screen illustrated scenes | monochrome cards on black |
| Captions | uppercase, bold, white with black stroke, on the seam | uppercase, heavy, one keyword in green, ~80% down | typewriter text in the frame |
| Labels | blue pill naming the beat, bottom of the top panel | the subject's name tag on the first shot | dates and dollar figures, large |
| Audio | -14 LUFS, LRA 2.0: voice over a music bed | -14 LUFS, LRA 2.6: voice over music | -14 LUFS, LRA 4.2 |
| Ending | the reveal, then "comment when you figured it out" | branded "LENS ON LEGENDS" card | CTA card |

## The Lifestyle Legends look

**The layout (1080×1920)**
- **Header strip** (96 px): paper-coloured, with the series tag "LIFESTYLE LEGENDS · EP 01".
- **Top panel** (806 px): the story visual. It can be an archive photo, a map, a book cover or a clip of you doing the thing. Photos get a slow 8% zoom, alternating in and out, so nothing is ever static.
- **Bottom** (1018 px): you talking to camera. The editor crops your full frame from 12% down, so frame yourself head to chest.
- **Pill label:** white capitals on a blue pill (#3D5AFE) at the bottom of the top panel, naming the beat ("AGE 15", "THE RAZZLE DAZZLE", "1903: THE CALL OF THE WILD").

**Full-screen moments**
- **You, full screen:** the series line, the moral, and any line where your face is the point.
- **B-roll, full screen:** you doing the legend's thing (the swim, the surf), with your voice over it.

**Captions**
- Uppercase and heavy, about 56 px, white with a 5 px black stroke and a soft shadow.
- 2–4 words at a time, broken at natural pauses.
- In the split screen they sit on the seam; when you're full screen they sit 70% down.
- Numbers, years and the plan's `highlight` words turn yellow.

**Guess the Legend**
- `censor` pixelates faces and give-away titles until the reveal, when the same photo is shown unpixelated.

**Pacing**
- A new top panel every sentence or two, roughly every 2.5–5 s.
- Hard cuts only: no transitions, zoom punches or sound effects.

**Ending**
- From "Follow…" to the end, a dark overlay with a series card: **LIFESTYLE LEGENDS** and, in yellow, "NEXT: IAN FLEMING".

**Sound**
- Voice first. Add an optional music bed (cinematic piano or ambient) ducked under the voice.
- The final mix goes to -12 LUFS / -1 dBTP, slightly louder than the references' -14, which Instagram turns down to match anyway.

## How the editor does it

`python3 edit_legend.py series/lifestyle-legends/plans/<plan>.json [--draft]` runs these steps:

1. **Talk clips.** Each one is transcribed. Fillers, stutters, retakes and pauses over 1 s are cut, using the same rules as `edit_video.py`.
2. **Panels.** Each panel starts at its spoken word (`"at": "Klondike"`; `"surf#2"` means the second time "surf" is said) and holds until the next panel. Before the first panel you're full screen.
3. **The picture.** Photos get the zoom and any `censor` pixelation. Clips are trimmed and held to length. The split screen, pills, header tag, captions and end card are composed on top.
4. **Audio.** The music is ducked under your voice, and the mix is boosted to -12 LUFS.
5. **Check.** The editor prints the edited transcript and every panel's start and end time, so you can fix a cue and re-run.

## Shooting checklist

- [ ] Talk takes: vertical, wide lens, head to chest, outdoors, with good light on your face. Keep your head in the top half of the frame, because that's the part that shows in the split screen.
- [ ] Say the hook the instant you hit record.
- [ ] B-roll of you doing the legend's thing, 5–10 s per clip.
- [ ] Gather the images listed under each script. Name the files exactly as the script says and put them in `input/<plan name>/`.
- [ ] Run `--draft` first, check the panel times it prints, then render the final.
