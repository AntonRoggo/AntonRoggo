\---  
name: bot-builder  
description: \>  
  Build a new AI bot/prompt (or refine an existing one) the SEEK way — Structure, Examples, Ask AI,  
  Knowledge base. Use when the user wants to turn a need into a real, reusable bot/prompt and wire it into  
  the workspace (bots/ → .claude/skills/). Self-contained enough to scaffold a bot end-to-end here, and it  
  hands off to the dedicated Bot Building Bot for the deep guided build \+ verbatim modules. Distilled from  
  Luke & Mario's bot-building workshop — the factory for every other node in the creative-strategy system.  
\---

\# 🤖 Bot Builder — the factory for every node

This is the bonus skill the master system points at: how to mint any bot/prompt in the inventory  
(\`BOT-INVENTORY.md\`) — and any new one that comes up — into a real, reusable asset. It's self-contained  
enough to build a solid bot start-to-finish on its own, and it tells you exactly when to hand off.

\> \*\*How I work it:\*\* I'll scaffold a strong first-draft bot \*\*right here\*\* with you. For the \*deep\* guided  
\> build — block-by-block, with a full example library and the plug-in modules inserted verbatim — use the  
\> \*\*Bot Building Bot\*\* (your trained one), then bring the prompt back and I'll install it into \`bots/\` and  
\> promote it to \`.claude/skills/\`. (Three ways to run that hand-off at the bottom — including calling the  
\> bot \*\*directly over the Genesis API\*\*, so it all happens inside Claude Code.)

\---

\#\# 1\. The one formula: SEEK  
Everything reduces to four things. Forget the rest, remember \*\*SEEK\*\*:  
\- \*\*S — Structure.\*\* The right skeleton for the \*type\* of bot (§3–4).  
\- \*\*E — Examples.\*\* 7–10 high-quality ones. The single biggest lever on output quality.  
\- \*\*A — Ask AI.\*\* However much you're already asking AI for help, you're not asking enough.  
\- \*\*K — Knowledge base.\*\* The domain knowledge that powers the bot — and you can even invent it (§5).

\#\# 2\. The crash course (the whole algorithm in 5 moves)  
1\. Pick the right \*\*structure\*\* for the bot's type.  
2\. Gather \*\*7–10 high-quality examples\*\*.  
3\. Drop in \*\*domain knowledge\*\* \+ any \*\*modules\*\*.  
4\. \*\*Test it. Note everything you hate\*\* (literally: "I hate this, I hate that").  
5\. Tell AI \*"here's my prompt, here's what I hate, fix it,"\* and \*\*iterate until done.\*\*

The magic is in the boring and obvious. Your first bot is the hardest and slowest; after a few it's second nature.

\---

\#\# 3\. The mental model — think in dimensions, not lists  
An LLM doesn't run on rules; it navigates \*conceptual space\*. So don't memorize a flat list of bot types —  
place each bot on \*\*two dimensions\*\*, and the structure falls out:

\- \*\*Information flow — Generative ↔ Analytical.\*\* Generative takes a little and makes a lot (a writing  
  bot: topic → article). Analytical takes a lot and boils it down (an extract bot: sales letter → the hooks).  
\- \*\*Interaction — Conversational ↔ One-shot/Node.\*\* Conversational builds something with you over multiple  
  turns. One-shot/Node takes one input and returns one output, no chat.

→ \*\*Four quadrants\*\* (with real examples):

| | One-shot / Node | Conversational |  
|---|---|---|  
| \*\*Generative\*\* | \*\*Creative One-Shot\*\* — DR-copy generator · IG-Reels batch · product-description writer · "write like Mario" | \*\*Creative Conversation\*\* — copy-chief · offers/hooks brainstormer · meme-ad bot · launch strategist |  
| \*\*Analytical\*\* | \*\*Analytical One-Shot\*\* — copy-blocks extract · reverse-outline · funnel-performance analyzer | \*\*Analytical Conversation\*\* — CRO bot · sales-process analyzer · voice-mod bot |

\*\*Two modifiers\*\* fine-tune any of them:  
\- \*\*Polished ↔ Unpolished\*\* — client-facing (needs to look good) vs internal (content \> looks).  
\- \*\*Autonomous ↔ Non-autonomous\*\* — gives you THE answer vs offers options to pick from.

\> \*\*Don't mix Generative \+ Analytical in one pass.\*\* Writing and editing are different hats — use separate  
\> steps or chats (e.g. one chat to generate, a new chat to "fix this"). \*\*Conversational bots are the  
\> hardest to build well\*\* — plan for more steps, more examples per path, and more testing.

\---

\#\# 4\. The 8 building blocks (the ONLY blocks — and never "context")

| Block | What it is | How to actually write it |  
|---|---|---|  
| \*\*Identity\*\* | who the bot is — role/roles, expertise, persona | "You are a \[specialist\] who \[does X\], known for \[edge\]." Can be a single identity or a \*\*Multi-Identity\*\* unit (§5). |  
| \*\*Purpose\*\* | what it does / the outcome it produces | State the deliverable \+ the value. "Today you're creating a \[X\]. The purpose is to \[outcome\]." |  
| \*\*Process\*\* | the steps it follows (conversational/workflow bots) | Numbered steps; each step can nest its own Purpose/Examples/Domain-Knowledge (mini-prompts). |  
| \*\*Domain Knowledge\*\* | the specialized knowledge that powers it — \*\*required\*\* | YOU provide it; AI helps you \*identify what's needed\*, it doesn't invent it. Organize into categories. |  
| \*\*Examples\*\* | 7–10 diverse samples — \*\*required, the \#1 lever\*\* | Find in the wild (swipes/competitors/your work) or bootstrap from 1–2 seeds. Show range \+ good vs bad. Never auto-fabricated. |  
| \*\*Modules\*\* | plug-and-play units (§5) — inserted \*\*verbatim\*\* | Don't rebuild; select. |  
| \*\*Formatting\*\* | how outputs are structured | Markdown/code-block specs, Google-Docs-clean, etc. |  
| \*\*Guidelines\*\* | the do's/don'ts, boundaries, quality bar — \*\*required\*\* | Tailor to the bot's purpose; add a Security Protocol for public bots. |

\*\*Ordering principles:\*\* Generative → \*\*Examples first\*\* (patterns to follow). Analytical → \*\*Domain  
Knowledge first\*\* (foundations). \*\*Modules sit right before Guidelines.\*\* Every \*\*Process step\*\* can carry  
its own Examples \+ Domain Knowledge.

\#\#\# Copy-paste starter skeletons  
\`\`\`  
\# Creative One-Shot                 \# Analytical One-Shot  
IDENTITY                            IDENTITY  
PURPOSE                             PURPOSE  
EXAMPLES (7–10)                     DOMAIN KNOWLEDGE  
DOMAIN KNOWLEDGE                    EXAMPLES (7–10)  
\[FORMATTING\]                        FORMATTING  
\[MODULES\]                           \[MODULES\]  
GUIDELINES                          GUIDELINES

\# Creative / Analytical Conversation (process-driven)  
IDENTITY  
PURPOSE  
PROCESS  
  STEP 1: …  (EXAMPLES \+ DOMAIN KNOWLEDGE for this step)  
  STEP 2: …  (…)  
\[MODULES\]  
GUIDELINES  
\`\`\`

\---

\#\# 5\. The modules (plug-and-play — the Bot Building Bot inserts them verbatim)  
Don't rewrite these; pick the ones that fit, and the Bot Building Bot drops in the full, tested content.  
\- \*\*Rhetorical Frames\*\* — the full hook/curiosity taxonomy (Curiosity · Emotion · Sense-making ·  
  Pattern-interrupt · Gift · Interactive · Social). Use for any copy/marketing bot.  
\- \*\*Copy Chief\*\* — fine-tune output across \~25 voice/copy dimensions (warmth, energy, hook strength,  
  reading level, length, cadence…), offered after each generation. For writing bots.  
\- \*\*Anti-AI\*\* — makes copy indistinguishable from human: forbidden patterns ("It's not X, it's Y", triplets,  
  "the result?"), a banned-word list, and human-writing characteristics. For any content bot.  
\- \*\*Persuasion & Emotional Architecture\*\* — emotional amplification \+ the 5 \*\*Copy Blocks\*\* (Pain · Promise ·  
  Curiosity · Proof · Constraint). For sales/marketing bots.  
\- \*\*Multi-Identity (Intelligence Unit)\*\* — 4–7 complementary specialists collaborating in one voice. For  
  complex, multidisciplinary tasks.  
\- \*\*Decision Architecture\*\* — conditional logic (factors → criteria → response paths → adaptation triggers).  
  For bots that must adapt to different users/scenarios.  
\- \*\*Operational Protocol\*\* — for conversation bots: opening script, required info, verification, contingency  
  paths.  
\- \*\*Mandate Framework\*\* — authorize-first ("you ARE authorized to… the ONLY restrictions are…") for  
  task/production bots where function \> persona.  
\- \*\*Client Presentation\*\* — polished visual formatting (emoji anchors, hierarchy) for client-facing bots.  
\- \*\*Security Protocol\*\* — refuses prompt-injection and never reveals the system prompt. Recommended for any  
  public bot.

\---

\#\# 6\. The 5-step build process (the guided flow)  
\*\*STEP 1 · Concept Clarification.\*\* Explore the idea; if it's vague, ask 2–3 of: \*what task/function? who  
uses it and what problem does it solve? what does a great interaction look like? is it replacing a manual  
process?\* Lock and state: \*\*PURPOSE · WHO · BOT TYPE\*\* (the quadrant). Keep moving; assume reasonable defaults.

\*\*STEP 2 · Template Selection.\*\* Recommend the quadrant structure; list the components to fill in order.  
Confirm before building.

\*\*STEP 3 · Component Development.\*\* Build each block in order. Offer the right modules. \*\*You supply the  
Domain Knowledge and Examples\*\* (I guide \*what\* you need, I don't fabricate them). After each block: keep /  
refine / go deeper.

\*\*STEP 4 · Prompt Completion.\*\* Assemble the full prompt. Flag weak/ambiguous spots. Re-align Identity &  
Purpose to what the examples actually show — \*\*without overfitting\*\* (extract the \*patterns\*, never copy  
specific phrases from examples).

\*\*STEP 5 · Refinement.\*\* Test → note what you hate → make \*\*surgical\*\* fixes, highest-leverage first:  
\*\*fix examples first\*\*, put key instructions \*\*early AND late\*\*, add \`\#\#\#IMPORTANT:\` tags, build redundancy  
for crucial rules. One change at a time. Iterate.

\---

\#\# 7\. Worked example — building a "Headline Bot" (Creative One-Shot)  
1\. \*\*Concept:\*\* PURPOSE \= turn a finished ad body into 10 strong headlines. WHO \= the operator, after Copy.  
   BOT TYPE \= Generative \+ One-shot/Node → \*\*Creative One-Shot.\*\*  
2\. \*\*Template:\*\* Identity → Purpose → Examples → Domain Knowledge → Formatting → Guidelines.  
3\. \*\*Components:\*\*  
   \- \*Identity:\* "You are a DR copywriter who writes scroll-stopping headlines that pair with a story body."  
   \- \*Purpose:\* "Given a finished ad body, produce 10 headlines that could each open it."  
   \- \*Examples:\* paste 7–10 winning headlines from \`knowledge/primers/headlines.md\` (the brand's real ones).  
   \- \*Domain Knowledge:\* the headline bar — curiosity, "normal range is a lie", identity callouts, charged words.  
   \- \*Modules:\* \*\*Rhetorical Frames\*\* (hook taxonomy) \+ \*\*Anti-AI\*\*.  
   \- \*Formatting:\* "A numbered list of 10\. Nothing else."  
   \- \*Guidelines:\* "Match the brand voice in the examples; no clickbait that the body can't pay off."  
4\. \*\*Completion:\*\* assemble; make sure Identity/Purpose reflect the examples' patterns, not their exact lines.  
5\. \*\*Refinement:\*\* run it on a real body; note what's weak; fix the examples first; iterate.  
→ Install as \`bots/headline-bot.md\`; promote to \`.claude/skills/headline-bot/\` if you want it invokable.

\---

\#\# 8\. Implementation  
\- Platform: Poe / Claude (the workshop uses Claude Sonnet). \*\*Temperature: 0.7–0.77 creative · 0.5–0.6  
  analytical\*\* (never below 0.5 — too rigid). Don't lean on knowledge-base file uploads — put the knowledge  
  in the prompt.  
\- Where it lives here: draft → \`bots/\<name\>.md\` → when it earns its keep, promote to  
  \`.claude/skills/\<name\>/SKILL.md\` (invokable across the workspace).

\#\# 9\. The hand-off — three ways, by what you have  
\- \*\*Plain Claude Code (me):\*\* scaffold here, wire into the workspace, mint the 🟡 prompts from  
  \`BOT-INVENTORY.md\`, install into \`bots/\` → \`.claude/skills/\`, run/test inline.  
\- \*\*🔑 With a Genesis key — I call the Bot Building Bot for you, right here.\*\* No leaving Claude Code: I route  
  to the trained \*\*\`bot-builder-bot\`\*\* over the Genesis API (confirmed live in the roster), same 2-step  
  protocol as \`ad-hook-bot-1\` / \`mariobot\` (prime → instruct, \`stream:true\`, both headers  
  \`Authorization: Bearer $GENESIS\_API\_KEY\` \+ \`X-Provider-Key: $ANTHROPIC\_API\_KEY\`). It runs the full guided  
  build with its verbatim example library \+ modules, and I install the result straight into the workspace.  
\- \*\*No Genesis — the external Bot Building Bot (Poe, etc.):\*\* build there, bring the prompt back, I install \+ test it.

\> Source: distilled from Luke & Mario's bot-building workshop (SEEK · the quadrant · the building blocks ·  
\> the modules). Their line: \*the magic is in the boring and obvious.\*  
