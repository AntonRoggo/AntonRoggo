# Video description scale: how much a pasted story has to lose before it becomes a video script

Filed 2026-10-01 after the Maui anniversary script, where the operator had to delete scenery and blocking line by line. Measured, not guessed: ten Lymphoria winners against nine long stories the operator pasted and six drafts Claude returned. Checker: `python3 tools/description_meter.py <file> --target song|vo|drama|bof`.

Related: [[story-ad-logic]] [[story-completion]] [[_story-library]] [[mechanism-and-product-core]] [[feedback-no-bloat]]

## The core difference
A pasted story is written to be read. The reader has no picture, so the words build the room, the clothes, the light, the faces. A winning video script is written to be heard over a picture. The camera already shows the room, so the words only carry what the picture cannot: numbers, the body, what people say, and the one object that comes back later.

## What the numbers show (spoken words only)

| Measure | Winners | Stories sent | Claude's drafts |
|---|---|---|---|
| Spoken words | 1,124 average (375 to 2,064) | 2,024 average (up to 3,333) | 1,726 |
| Words per sentence or line | 5.6 | 8.8 | 7.3 |
| Lines of 4 words or fewer | 46% | 27% | 40% |
| Adverbs and intensifiers per 1,000 words | 1.5 | 5.6 | 1.6 |
| Place phrases ("overlooking," "across the") per 1,000 | 1.5 | 2.3 | 3.4 |
| Numbers (ages, pounds, weeks) per 1,000 | 51 | 56 | 63 |
| Body and symptom words per 1,000 | 10.8 | 14.5 | 10.6 |

Reading it: the winners are not description-free. They spend description in different places. The stories sent run long, use long sentences and lean on adverbs ("completely," "literally," "truly"). Claude's drafts fixed the adverbs but kept the stories' length and scenery, and added place phrases of their own.

## What winners describe (keep in the spoken words)
1. **Numbers.** Ages, pounds, months, weeks, the time on the clock. The densest category in every winner. "She was 28. He was 54." "35 pounds in 18 months."
2. **The body, in fixed places and plain words.** Belly, face, jaw, ring, jeans, "tight and pushed out," "soft or hard." Description that sells the mechanism or proves the change.
3. **One prop that comes back.** The dress, the ring, the pin, the bottle. Named by what it means, not what it looks like: "the dress I bought and never wore," not "the navy silk wrap."
4. **Evidence in a catch, in four words or fewer each.** "Grey Camry." "Kitchen light still on." "Bedroom door was cracked." Every detail is a clue, never decoration.
5. **The stare, in three short beats.** "Mouth slightly open. Like he'd seen a ghost." One simile, at the peak, nowhere else.
6. **What people say.** Short, verbatim, tagged.

## What winners leave to the camera (cut or move to a visual note)
1. **Scenery, light and weather.** Sunrise turning the water gold, torches, ocean breeze, golden hour.
2. **Other people's appearance.** Blonde highlights, glossy lips, backless dress, tight sundress. Give an age; casting does the rest.
3. **Clothing color and fabric,** unless it is the payoff prop.
4. **Furniture and materials.** Mahogany bar, quartz counter, wicker couch, coat rack.
5. **Blocking.** Stepped back beside me, half-step toward her, cut me off by the coat rack, turned his head.
6. **Face narration in a drama.** "His face went red," "his jaw dropped." The actor shows it. In a song, one short line at most.
7. **Interior monologue.** At most one thought line per act ("I almost believed him"). No paragraphs of feeling.
8. **Adverbs and intensifiers.** Completely, literally, truly, immediately, quietly.
9. **Throat-clearing.** "Let me back up," "Here is the biggest thing I took away," "I want to be honest."
10. **Process the montage shows.** Airport lines, shuttles, packing, arriving, sitting down. Cut to the next thing that changes the story.

## The scale

| Level | What it is | Spoken words | Words per line | What stays in the words | Example |
|---|---|---|---|---|---|
| 5 | Read story (Reddit post, advertorial, long VSL) | 2,000 to 3,300 | 8 to 10 | Everything: rooms, clothes, light, feelings | What gets pasted in |
| 4 | Narrated VO over B-roll | 1,200 to 2,100 | 5.5 to 7 | Numbers, body, evidence clues, dialogue; terse scene clues allowed | Story 006 |
| 3 | Song or verse | 900 to 1,700 | 4.5 to 6 | Numbers, body, the prop, dialogue as "she said"; no scenery | Stories 001, 002, 004 |
| 2 | Realistic AI drama or two-hander | 400 to 1,600 | 5 to 7.5 | Dialogue only; all description lives in the visual and acting notes | Locker room, tailgate |
| 1 | BOF offer ad | 20 to 200 | short | The offer and one reason | Rosabella, Smooche |

Every pasted story starts at level 5. Pick the target level from the format, then move down.

## The procedure, every time a story is pasted
1. Name the target level from the format (song = 3, VO = 4, realistic AI drama = 2, BOF = 1).
2. Run the meter on the pasted story: `python3 tools/description_meter.py <file> --target <song|vo|drama|bof>`.
3. Cut to the word range by removing whole beats that do not change the story (process, transitions, repeated proof) before trimming sentences.
4. Move every flagged scenery, appearance, blocking and face-narration line into a "(Visual: ...)" note; keep the clue words only when they are evidence.
5. Keep the numbers, the body words, the payoff prop and the dialogue.
6. Re-run the meter on the draft; it should pass at least 5 of the 6 checks, like the winners.
