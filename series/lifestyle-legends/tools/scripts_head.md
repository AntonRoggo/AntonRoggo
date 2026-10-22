# Lifestyle Legends: scripts

There are three legends, each with one script per format. How each format is edited is broken down in [BREAKDOWNS.md](BREAKDOWNS.md).

- **Legend 1: Jacques Cousteau.** The Riviera is his home water.
- **Legend 2: Yvon Chouinard.**
- **Legend 3: Ernest Hemingway.** He lived it, then wrote it.
- **The bench**, for Ep 04 and beyond, is at the end. Jack London and Ian Fleming already have scripts.

The three formats:
- **A. The Origin Story**
- **B. Guess the Legend**
- **C. In Their Footsteps**

Each script has a plan in `plans/`, so once you've filmed it the editor can cut it:

```bash
python3 edit_legend.py series/lifestyle-legends/plans/<plan name>.json --draft
```

Put the footage for each script in `input/<plan name>/`, using the file names below. In the "On screen" column:

- **top** is the story panel above you.
- **full screen** covers the whole frame.
- **pill** is the blue label naming the beat.

Each panel starts on the first word of its line and stays up until the next one.

Before posting, check every fact marked ✓. They're from memory and haven't been checked against sources.

**Images.** Archive photos from before 1931 are generally public domain in the US; use Wikimedia Commons or the Library of Congress, and check each licence. Hemingway's WWI-era photos are generally public domain; check each one. For Cousteau, Chouinard, Fleming and later Hemingway photos, most are still under copyright. Use your own footage of places and objects, film yourself holding the book, buy a licence, or use an illustrated scene (that's what Lens on Legends does). Never use a fake photoreal image of a real person.

