# Your Workspace

This is your workspace: a folder of plain markdown that Claude Code reads and you view in Obsidian. Claude reads the Script (CLAUDE.md) first, every session, so it shows up already knowing who you are and how you work.

## Your first session
Run /vault-setup first. It does steps 1 to 3 for you (personalize the Script, make your client file, start today's note). Then do steps 4 and 5. If /vault-setup is not installed yet, do all five by hand:
1. Personalize the Script: edit the "Who I am" line in CLAUDE.md to your niche and role.
2. Make your client file: copy clients/_client-template.md to clients/{yourclient}.md and fill it in. Do this before writing client work, so claims have a source.
3. Start today's daily note: create daily/YYYY-MM-DD.md for what you work on and decide. Add `Related: [[Memory Loop]] [[The Script]]` under the title.
4. Work: SAVE it into copy/ or creatives/. Name every file YYYY-MM-DD-slug.md.
5. Promote at the end: ask Claude "what from this session is worth promoting into memory, and where does it go." Approve, and it files the lessons into winners/, brand/, and the rest.

Read the-data-dictionary.md once, to learn what is worth promoting vs ignoring.

Open `memory-map.md` in Obsidian when you want to see the links between the pieces.

Open `skills/Skills.md` in Obsidian when you want to see the slash-command skills. The actual Claude Code instructions live in `.claude/skills/`, but Obsidian hides folders that start with a dot.

## Why the Obsidian links exist

The `[[links]]` are there for two jobs:

- Obsidian shows backlinks, so you can see what keeps connecting.
- Claude can read those links as routing hints when it opens the files.

This does not mean every word should become a link. Add a short `Related:` line to durable notes:

```md
Related: [[Memory Loop]] [[Workbench vs Memory]]
```

Good links point to a concept, client, workflow, winner, loser, or swipe that explains the note. Skip decorative links.

Folders: see the Script's "where my stuff lives" map.
