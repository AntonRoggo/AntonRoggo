# Skills

Related: [[The Script]] [[Memory Loop]]

Skills are the slash commands that come with this workspace.

Claude Code loads the real instructions from `.claude/skills/`. Obsidian hides folders that start with a dot, so this visible `skills/` folder is your human-readable map.

If you want to use a skill, type the slash command in Claude Code.

If you want to change how a skill works, ask Claude to edit the real skill in `.claude/skills/{skill-name}/SKILL.md`. Editing these visible notes only changes the notes.

## The first ones to try

| Skill | Command | Use it when |
|---|---|---|
| [[vault-setup]] | `/vault-setup` | Set up the workspace for the first time. |
| [[advanced-script-interview]] | `/advanced-script-interview` | Tune the Script after Obsidian and the link map work. |
| [[see-your-setup]] | `/see-your-setup` | Check what is installed and whether the workspace is getting messy. |
| [[reflect]] | `/reflect` | End a session and decide what should become memory. |
| [[remember-this]] | `/remember-this` | Save one lesson while the session is still fresh. |
| [[handoff]] | `/handoff` | Save restart context before sleep, compaction, or switching sessions. |

## Thinking and review

| Skill | Command | Use it when |
|---|---|---|
| [[plan-as-page]] | `/plan-as-page` | Turn a rough idea into a structured plan. |
| [[adversarial-review]] | `/adversarial-review` | Pressure-test an idea, page, prompt, or output. |
| [[convince-me]] | `/convince-me` | Make Claude argue for a recommendation with clearer reasoning. |
| [[security-check]] | `/security-check` | Check installs, backups, public sharing, permissions, and risky file moves before acting. |

## Building the system

| Skill | Command | Use it when |
|---|---|---|
| [[save-as-skill]] | `/save-as-skill` | Turn a repeated workflow into a reusable skill. |
| [[upskill]] | `/upskill` | Improve an existing skill after using it. |
| [[dashboard-setup]] | `/dashboard-setup` | Create or refresh the visual dashboard for the workspace. |
| [[create-workflow-diagram]] | `/create-workflow-diagram` | Turn a process into a diagram. This one may need Node the first time. |

## Production pipelines (make the ads)

These are the heavy systems. The vault skills above run the workspace; these run the work.

| Skill | Command | Use it when |
|---|---|---|
| [[creative-strategy-system]] | `/creative-strategy-system` | Strategy, ideation, hooks, copy, iterations. The default pipeline. |
| [[genesis-ad-system]] | `/genesis-ad-system` | The staged pipeline through trained Genesis server bots. Needs the API key. |
| [[bot-builder]] | `/bot-builder` | Mint a new bot or prompt and install it as a skill. |

Client-specific skills beat these for their own clients: tt-brief-builder, lymphoria-ad-classifier, messaging-extractor.

## The simple model

The skills are not separate apps.

They are instructions Claude can load when you ask for a specific kind of help.

The loop is:

1. Use the skill.
2. Save the work.
3. Promote the lesson if it should help next time.
