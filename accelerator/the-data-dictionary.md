# The Data Dictionary

The most important file in the workspace. It answers the question that decides whether your setup gets smarter or just gets bigger: what is worth promoting into memory, and what is noise.

Two moves, kept separate:
- SAVE = put your work in the workbench (copy/, creatives/).
- PROMOTE = put the lesson into memory (winners/, losers/, brand/, workflows/).
This file is about PROMOTE.

## The rule of the second time
This rule is about PATTERNS, not individual wins. Promote a clear win or loss into memory as it happens (a hook that won -> winners/, an ad that died -> losers/). The second time the same pattern holds, promote it again into a reusable rule or play. Once is a data point. Twice is a pattern worth systematizing. Three times it should already be a play in workflows/. You are not promoting everything, you are systematizing what repeats.

File naming: name every file `YYYY-MM-DD-slug.md` (for example `2026-05-29-hidden-fee-hook.md`). One convention everywhere, so you never have to stop and decide.

Linking: every promoted note should include one short `Related:` line near the top. Use two or three useful Obsidian links, not a wall of links.

```md
Related: [[Promotion]] [[Workbench vs Memory]]
```

The links are not decoration. They help Obsidian show backlinks and help Claude follow the memory trail next time.

## Worth promoting vs not

| Worth promoting | Not worth promoting |
|---|---|
| A hook structure that won twice | A one-off line for today's ad |
| A voice rule you corrected after a miss | A single-use prompt for one task |
| A swipe that matches a mechanism you keep using | A swipe you kept because it looked cool |
| An ad that died, and the reason it died | Exploratory junk from a thinking session |
| A client rule that bit you once | A just-in-case note that never fires |
| A play you ran three times this month | A workflow you will never repeat |

## The data points worth promoting
Each lands in a specific place. Write it in your own words, short.

1. Winning hooks, with WHY. -> winners/. The mechanism, the audience, the brand. Not just the line.
2. Voice rules, especially corrected ones. -> brand/voice.md. The ones born from a miss are the gold.
3. Swipes by mechanism. -> swipes/. Organize by the mechanism the ad uses, not by brand.
4. Losers, with WHY. -> losers/. Stops you and the model re-running a dead angle.
5. Client rules that bit you. -> clients/{name}.md. The one thing you will forget and regret.
6. Plays you repeat. -> workflows/. Any sequence you have run three times, written as steps.
7. Verification gates that caught a real failure. -> the workflow file or the Script. A specific testable gate, not "make it good."

## Workbench vs memory
copy/ and creatives/ are your workbench: where you make hooks, headlines, long-form, statics, video. This file governs what gets PROMOTED from the workbench into memory. When a piece of copy or a creative wins, promote its lesson to winners/ with the reason it worked. The workbench holds the work; winners/ holds why it worked.

## How to promote without breaking flow
Do not stop mid-task to write a perfect note. At the end of a session, ask Claude: "what from this session is worth promoting into memory, and where does it go." It proposes, you approve. Two minutes, and it is how the setup gets smarter from your own work.
