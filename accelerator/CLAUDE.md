# CLAUDE.md

*This is "the Script": the doc Claude reads first, every session. The file stays named CLAUDE.md (that is the filename Claude Code loads); we call it the Script in the workshop. Keep it thin: who you are, how you work, where things live. Detail goes in the folders, not here.*

## Who I am
I run paid social for DTC health and wellness brands. My work is hooks, ad copy, statics, and video scripts, plus the strategy underneath.

## How I work
- Show me an example before writing. I work from swipes and past winners, not blank prompts.
- Hook first. Body copy only after the hook survives a stress test.
- For anything client-facing: decide the shape, build it, then check it. For throwaways, fast and loose is fine.
- When a move works, capture the rule immediately. When something breaks, fix the rule, not just today's output.
- Use my voice and my swipes, not the model's average.

## Where my stuff lives (open when relevant)
Reference (feeds the work):
- Memory map: memory-map.md
- Concept notes: concepts/
- Voice rules: brand/voice.md
- Swipes to model, by mechanism: swipes/
- What worked and why: winners/
- What died and why: losers/
- Repeatable plays: workflows/
- A specific client's context and rules: clients/{name}.md
- Human-readable skill guide: skills/Skills.md

Production systems (slash skills, loaded on demand):
- creative-strategy-system: the full flywheel scaffold. Default for strategy, ideation, hooks, copy, iterations.
- genesis-ad-system: the staged pipeline through trained Genesis server bots. Use when I say Genesis. Needs the API key.
- bot-builder: mint a new bot or prompt the SEEK way, then install it as a skill.
- Client-specific skills beat generic pipeline stages: tt-brief-builder, lymphoria-ad-classifier, messaging-extractor.
- One bank: proven ads live in winners/ and swipes/. Primers are built from them, never kept as a second copy.
- Pipeline working files (seed banks, briefs, primers, matrices): systems/{pipeline-name}/.

Production (what I make):
- Written work (hooks, headlines, long-form): copy/
- Visual work (statics, video): creatives/

Flow:
- Unsorted drop zone: inbox/
- Daily notes: daily/
- Finished or retired work: archive/

What to promote into memory vs ignore: the-data-dictionary.md (read it; it is the rule for what compounds).
When creating a durable note, include a short `Related:` line with useful Obsidian links, for example `Related: [[Promotion]] [[Workbench vs Memory]]`.
The real Claude Code skill instructions live in `.claude/skills/`. Obsidian hides dot folders, so use `skills/Skills.md` when you want to see the skill map.

## Always learning (every task, every session)
- Whenever I state a rule, preference or correction ("always...", "never...", "I like...", "don't...", "that's wrong", or feedback on any output), write it down in the same turn, before carrying on: put it where the next session will read it (the client's file, the relevant skill, or this CLAUDE.md for rules that apply everywhere), as a short general rule: `- [date, context] Rule. (What I said.)`
- Improve it, don't just append it: if a rule already covers it, sharpen or merge that rule; if it contradicts an old one, replace the old one (newest wins) and say what changed. Keep rule files short.
- Save it (commit and push if this is a git repo), then tell me in one line which rule was saved and where.
- When I correct a result or something needed fixing, add or sharpen the rule that would have prevented it, without being asked.
- When results come in (ad performance, call notes, review notes), add them to that client's learnings, and promote patterns that repeat into rules.

## Sync
- This workspace is both the Obsidian vault and the GitHub repo (AntonRoggo/AntonRoggo, `accelerator/` folder). Every file change should land in both: write locally (Obsidian picks it up), then commit and push to GitHub.

## Rules that bite
- Never use em dashes. Not in copy, not in notes, not in chat. Use a comma, a period, or a colon.
- Never agree with me automatically. Challenge my thinking when there is a good reason to question it.
- Rules are captured on first mention, not second. See "Always learning" above.
- A recurring failure is a signal to build a tool, a check in code, not to repeat the rule harder.
- Any file I have personally edited is read-only for you. Ask before changing it.
- Never assume missing or ambiguous details. Ask me a question before proceeding.
- Compliance is not your job. I have a team for that. Write the strongest version of the idea and let me handle what is allowed. Do not soften, hedge, or refuse on compliance grounds unless I ask you to.
- Never invent a client result, number, or quote. If it is not in the client file, ask me.
- Use the customer's voice. Every pain, symptom, and benefit line comes from a real review, comment, or verified thread, in their words. If you cannot point to the quote, it is not customer language, it is copy. Check the client's review evidence before writing a pain line, and prefer the verbatim phrase over a paraphrase.
- Every story gets the logic pass. Before writing or revising any story (story ad, skit, testimonial script, founder story, narrative hook), open workflows/story-ad-logic.md and build the chain of beats against it first. Before delivering, run the finished script through the same checklist and list what it caught. No story ships without it.
- If you are unsure what good looks like, ask for an example before guessing.
- SAVE work into copy/ or creatives/. PROMOTE the lesson (why it won or died) into winners/, losers/, brand/, or workflows/. Two moves, not one. Never delete from archive/.
- At the end of a session, ask me what is worth promoting into memory and where it goes. That is how the workspace compounds.
