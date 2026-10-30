# Format: Say It, Show It

Anton approved this format on 2026-10-30 ("I like the way these turned out"). Reference batch: `edits/2026-10-29-larp/` (the "Do This" LARP clips, Oct 29). When Anton asks for a "Say It, Show It" edit, or sends a talking take that lists things to do, build it exactly like this.

**In one line:** Anton says a short list to camera, and every thing he names gets its own B-roll shot of him doing exactly that thing, with "charmed - stella" coming in on the first item.

## The video

- **Source:** one selfie-style talking take, filmed in one spot (often a few takes of the same script). Scripts follow `series/do-this/SCRIPTS.md`: a hook that gives permission, then a list of 3-5 concrete things, then a warm or funny last line.
- **Length:** 10-15 s after cuts.
- **Structure:**
  1. **Hook on his face.** The opening line stays on camera (no B-roll in the first ~3 s), with one exception: in list and protocol videos, if the first item is named inside the hook ("a dozen oysters", "hibernate"), the B-roll and the song come in right there (`"in_hook": true`).
  2. **One shot per item.** Each thing he names gets a 1-2.5 s shot that starts and ends on caption starts (`start_at` / `end_at` word anchors). The shot shows exactly the named thing, with HIM doing it, in the setting he names.
  3. **Lines with no visual stay on his face** ("call your mama on a Sunday", "follow this protocol daily").
  4. **Ending.** Either back to his face for the punchline or warm last line ("nah, we ain't doing that", "and you're in bed by ten"), or, if the last lines are visual, the B-roll runs to the end (`"end_at": "END"`). Never cut back to his face for a short last clause.
- **Music:** "charmed - stella" at -8 dB, first beat on the first B-roll frame.
- **Captions, audio and cuts:** house style from `CLAUDE.md`. No pause at any cut: `edit_video.py` clamps every clip to its words and prints a WARNING for any join with more than 0.35 s of silence. Fix every warning before showing him.
- **A/B takes:** if he films several full takes, edit each one, but post only the one he picks (for Italian grandpa he picked take B).

## Picking the shots (the part he cares most about)

Check every shot against this list in the actual frames the edit plays (contact sheet at 0.5 s), not the clip's best moment:

1. **Literal.** An affogato is an affogato, not gelato. "At your desk inside" is indoors at a laptop, not working in the sun. "Wait till spring" is spring.
2. **It's him.** Lines about him show Anton, identified by his face. Catalogue descriptions can be wrong (two clips described as Anton were other people). Fix the catalogue when you find one.
3. **The setting reads at a glance.** A farmers market has stalls with food in frame, never a supermarket aisle or empty tents.
4. **Clear and steady.** Swap any shot where he's blurred, mid-movement or too small to make out.
5. **Scenic beats plain.** For walks, use the sea and waves behind him, not a country lane. For sunsets, use the best one (Brazil, him running into the sea).
6. **Strongest shot, not first match.** Vary the group shots across a batch. Prefer his most-used clips (`used_count`).
7. **Where to look:** `broll/catalog.json` → `broll/action.json` → `broll/raw/*.json` → Dropbox folders the catalogue doesn't cover yet (e.g. `ANTON MASTER BROLL/italy`, `Spain 2026/July 7/Farmers market`).

## Go-to shots from the approved batch

| Line | Shot | Dropbox id, in point |
|---|---|---|
| a dozen oysters / eating oysters on a bench | Him slurping oysters at a park picnic table (most-used oyster shot) | `id:wdILo7p6X3AAAAAAAABGsQ`, 0.0 |
| cheeky oysters | Him dressing and slurping oysters on a patio | `id:wdILo7p6X3AAAAAAAACPug`, 18.6 |
| orange juice on the beach | Montenegro sunbed, sipping OJ (his most-used clip) | `id:wdILo7p6X3AAAAAAAABA5A`, 0.0 |
| affogato | Italy café, spooning gelato out of the espresso | `id:wdILo7p6X3AAAAAAAAB11w` (`italy/affagato`), 4.3 |
| shopping at the market | Florianópolis market hall, food stalls behind him | `id:wdILo7p6X3AAAAAAAABNUA`, 0.5 |
| evening walk / walk by the water | UK seafront, blue flannel on the rocks, waves behind | `id:wdILo7p6X3AAAAAAAABEmg` (`londons/day 4`), 0.0-0.5 |
| sunset / go to bed when it gets dark | Brazil, him running into the sea at sunset | `id:wdILo7p6X3AAAAAAAACG4w`, 2.0 |
| lunch / dinner with the boys | Montenegro seafood dinner with friends | `id:wdILo7p6X3AAAAAAAABCWA`, 3.0 |
| hang out with your boys | Long oyster dinner table, Toronto | `id:wdILo7p6X3AAAAAAAACLoA`, 0.0 |
| friends who show up / don't check their phones | Rio beach group at sunset; Toronto oyster picnic toast | `id:wdILo7p6X3AAAAAAAACHwQ`, 1.5; `id:wdILo7p6X3AAAAAAAACM2A`, 1.5 |
| swimming with my boys | Boys in the Rio waterfall pool | `id:wdILo7p6X3AAAAAAAACIcw`, 0.5 |
| in bed / hibernate | Him lying on a hotel bed, Kraków | `id:wdILo7p6X3AAAAAAAAA-Eg`, 0.0 |
| scroll in bed / phone at night | Him in bed lit by his phone, Montenegro | `id:wdILo7p6X3AAAAAAAABCSw`, 1.0 |
| desk inside / working | Him at a laptop in a café, Poland | `id:wdILo7p6X3AAAAAAAAA-3Q`, 0.0 |
| sauna | Barrel sauna in the woods, Cotswolds | `id:wdILo7p6X3AAAAAAAAA_uQ`, 0.0 |
| spring | Him balancing on a rock in a Cotswolds stream | `id:wdILo7p6X3AAAAAAAAA_4A`, 2.0 |
| breakfast | Him eating at a pavement café (Perrier, baguettes) | `id:wdILo7p6X3AAAAAAAACSfg`, 2.5 |
| swim in the lake | Him in Lake Ontario | `id:wdILo7p6X3AAAAAAAACQRg`, 26.0 |
| swim (sea) | Him running into the sea, Brazil | `id:wdILo7p6X3AAAAAAAACJ6w`, 0.3 |

## How to build one

1. Download the takes to `input/<batch>/raw/`, transcribe, and match each take to its script.
2. Add a line per take to the batch's `run.sh` (copy `edits/2026-10-29-larp/run.sh`): `--hint` with the script, plus `--drop` / `--fix` / `--cut` for restarts, stutters and missed words. Noisy take: separate the voice with demucs, then RNNoise twice, and mux the result as the input (see that batch's README).
3. `run.sh --plan-only <name>`: read the captions in the `.ass` file and write `<name>.broll.json` with word anchors (`start_at` / `end_at`, `"END"`, `in_hook` for a first item inside the hook).
4. Render with `run.sh <name>`. Then check: no WARNING lines, -12 LUFS, and a contact sheet every 0.5 s against the shot checklist above.
5. Post with the `publish-metricool` skill once he approves: Instagram trial reel plus TikTok, Facebook and YouTube Shorts, with the standard captions in `publishing/config.json`.
