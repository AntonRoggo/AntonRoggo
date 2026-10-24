# Lifestyle Legends: scripts

Every script is built **line for line on a winning reel's transcript**. Each table puts the winner's line next to yours, so you can see exactly what each line copies. Each script also has **three hooks**, each copied from a proven hook formula, and you can film any of them. The editing breakdown of each winner is in [BREAKDOWNS.md](BREAKDOWNS.md).

## What the winners actually do

| | Origin Story | Origin Story, short | Guess the Legend | In Their Footsteps |
|---|---|---|---|---|
| **Winner it copies** | [Let's Talk About It](https://www.instagram.com/reel/DaWEza9y-Dg/), 6.0M, 3,241× | [Jon Favreau](https://www.instagram.com/reel/DDSdkJGoVRs/), 5.8M, 556× | [Guess the footballer](https://www.instagram.com/reel/DdjfzUURsA3/), 97K, 12× | [Stevenson Trail](https://www.tiktok.com/@heleneinbetween/video/7646771334520769805), 578K, 65× |
| **Length** | about 2 min | 26 s | 62 s | 99 s |
| **How much story** | One thread: one dream, the thing that killed it, one pivot, proof, the lesson. Five or six facts. | Seven sentences, one setback, one move. | About 12 career steps, one per clause. | Barely any of the legend's life. It's the creator's own experience, with the legend as the reason. |
| **When the name comes** | **First second**: "Jordan Howlett. More popularly known as…" | **First sentence** | **Hidden until 90%**: "By now, you probably know…" | **Named in passing at ~10 s** ("Stevenson's Trail"), paid off at his landmark at ~85 s |

**What changed from the last drafts**
- **Less story.** The old scripts packed 10–14 life events into each video. The winners pick one thread.
- **Name timing.** The Origin Story now says the name in the first line, as the winner does. Hook 2 for each legend keeps the name off the audio, Lens on Legends style; the name tag goes on screen instead. Lens repeats its hook beat later in the story too ("moved back to London alone" at 26–39 s), so the later crash or shell line still works with hook 2.
- **Guess format.** Guess the Legend now copies the winner's actual sentence pattern: present tense, every clause starts with a verb, no ages, then "A ship awaits… This chapter ends when… By now, you probably know…".
- **Footsteps format.** In Their Footsteps is now about *your* experience, copying the Stevenson Trail beats ("No X, no Y, just me…", "Here's how it works", "This is not roughing it", "Standing there, I couldn't believe…", "That's the power of…"). The legend frames it rather than being the story.
- **Short cuts.** A 30-second version of each Origin Story, built on the Favreau winner, for when you want it short. It also works as a text post with no filming.

## How to use this

Each script has a plan in `plans/`, so once you've filmed it the editor can cut it:

```bash
python3 edit_legend.py series/lifestyle-legends/plans/<plan name>.json --draft
```

- Put the footage in `input/<plan name>/`, using the file names under each script.
- The first panel starts at 0 s, so the plan works whichever hook you film.
- In the "On screen" column, **top** is the story panel above you, **full** covers the whole frame, and the bold text is the blue pill label.
- **Lines marked ✎ are personal.** Only say them if they're true for you, or swap in your own version.
- Before posting, check every fact marked ✓. They're from memory and haven't been checked against sources.

**Images.** Hemingway's World War I photos are generally public domain (check each one). Most Cousteau, Chouinard and later Hemingway photos are still under copyright. Use your own footage of places and objects, film yourself holding the book, buy a licence, or use an illustrated scene. Never use a fake photoreal image of a real person.

