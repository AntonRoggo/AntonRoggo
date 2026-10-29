# Fully AI videos for Seed Oil Scout: plan

Source: Owen (StefanBrain team), "How I use Grokbot computer use to one-shot video generation with StefanBrain", X, 2026-10-27, 13.5 min.
https://x.com/ostentatiousHQ/status/2115103866869952669
Full transcript: `notes/refs/2026-10-27-owen-grokbot-stefanbrain-transcript.txt` (auto-transcribed, so names like "Grokbot" are sometimes heard as "grog bot"/"crockpot").

## What he built

Grokbot is the orchestrator ("command center"). It controls a logged-in browser on his Mac (computer use) and runs a "group chat" of agents that talk to each other:

| Bot | Job |
|---|---|
| Operations | Lead agent. Routes work between the bots and to Owen. |
| VG Prompting | Writes the generate package (product refs, notes, aspect/duration/style, scene prompt + script). Uploads every reference (character images, voice/audio, guidance) so clips stay consistent. Learns from QA. |
| VG QA | Watches each video and grades it: DR principles, pronunciation, visual inconsistencies. |
| VG Editor | Fixes problems with SB's own editor (regenerate a line, swap hooks, B-roll), or its own editor for cuts and stitching. |
| VG Gate | Final ship/kill call after QA scores (Grokbot suggested adding it, so QA critiques and Gate decides). |

Setup steps he showed:
1. Pasted the setup prompt (below) into Grokbot. Asked "do you recommend any other bots?" and it added the Gate bot.
2. Signed Grokbot into stefanbrain.com. It went through every video he'd ever made (~176) and their prompts, plus docs.stefanbrain.com, and wrote a `sb-video-prompting` skill file of lessons. He only used videos made since 5 September (VidGen 2.0).
3. Had the Editor bot learn the SB editor from the KB tutorial (docs.stefanbrain.com/knowledge-base/video/edit-video-dialogue-and-captions) and by trying it out.
4. Agreed the workflow (below), then ran two tests:
   - **Song ad** for Grüns, GLP-1 digestion angle: angle explored in SB chat for a hook and chorus, then VidGen made a ~2 min claymation song ad with lots of B-roll and 2 alternative hooks in the SB editor.
   - **4 × 15s clips** of an animated gummy bear, made separately and then stitched together outside SB. To keep them consistent it locked one character image, made 4 pose stills from it (wave, walk, dance, cheer), and animated each still using the locked image as reference (same set, same character, same props).

His takeaways:
- QA was too strict at first and failed everything over tiny glitches. Loosen it.
- Too much B-roll was added because he asked for it.
- The stitched video lost SB's caption style. Make captions a standing rule in the editor.
- Comment or RT the tweet and he'll DM you his full setup prompt. The version below was read off the screen.

### Setup prompt (as shown on screen)

> Set up a Video Generation Groupchat. Goal here is autonomous video generation and editing. We need a QA Bot (to watch and judge videos based on specific skills and DR principles, pronunciation, and visual inconsistencies), a Prompting bot (to learn from QA, past prompts, and future prompts, upload all visual references, guidances, audio tracks, etc.), a Video Editor bot, to use SB's native regeneration and editing platform to fix any inconsistencies. It will also use your own native video editor when needed to perform additional edits and cuts.
>
> Additionally, use computer use, and analyze every video I ever generated with StefanBrain. Examine the prompts, and where the video went wrong. Use those findings to create a video prompting skill, so that we can ensure the highest quality results, every time. Use docs.stefanbrain.com to also look at what the team suggests for prompting video gen. Then, let's align before you generate a video, because i want to QA your prompts and understand your reasoning. We will work towards this being fully autonomous. You will generate skill files as we go for each bot so that we follow a process that is repeatable and improves over time, resulting in this: as you generate more videos, learn from mistakes to continually improve and get better.
>
> We need to setup a system here. Do you recommend we add any other bots into this groupchat before we proceed with full setup here?

### Workflow it settled on

- **Mode A (while calibrating):** Owen gives a one-line idea + product → Prompting drafts the generate package → Owen approves the package (nothing generates without his OK) → generate → QA watches → Editor makes the smallest fix → QA again → Gate ships or kills → Owen watches and approves.
- **Mode B (scaling):** same pipeline, but step 1 becomes a weekly concept board. The bot pulls angles from SB products, past winners and losers, ad-spy references and Slack, then sends 5-10 one-line concepts (hook, product, format, why it might work). Owen approves, kills or tweaks each one. Once the skill is trusted, routine packages skip prompt review and Owen only sees Gate's finals.

## How we'd do it here, with Claude Code as the harness

Same roles, mapped onto the tools this repo already has:

| Role | Here |
|---|---|
| Operations | This Claude Code session |
| Angles, hooks, scripts | StefanBrain (`ask_stefanbrain`) |
| Prompting, QA, Gate | Claude subagents. Their skill files live in this repo (like `brand/editing-lessons.md`) and get updated from each round of feedback. |
| Video, image and voice generation | **Option 1:** HiggsField (connected; image → image-to-video, voice, music). Works from the cloud right now. **Option 2:** StefanBrain VidGen. Not exposed through the StefanBrain connector, so it needs computer use on Anton's Mac (logged into stefanbrain.com), the same way Grokbot does it. |
| QA "watching" | Frames + Whisper transcript (the same way this video was analysed): check the words match the script and pronunciation is right, and that characters and props stay consistent from shot to shot. |
| Editing and stitching | ffmpeg + `edit_video.py` (our caption style, J-cuts, music, loudness), which avoids the caption problem Owen hit. |
| Posting | `publish-metricool`, only after Anton approves that specific video. |

Accounts as of 2026-10-28: StefanBrain CA Pro (MCP usage unlimited, no brands set up yet). HiggsField Ultra with ~201 credits, which is enough for a short test but not many clips.

## Open questions before the test

- What Seed Oil Scout is: product/app link, audience, offer, and which accounts the videos post to (and whether those accounts are in Metricool).
- Generation path for the first test: HiggsField from here, or SB VidGen by connecting Anton's computer.
- First format: e.g. a recurring animated mascot (the locked-character trick) doing 15s spoken or song clips, or a faceless B-roll + voiceover explainer.

## Tonight's test (Mode A, one video)

1. Create a "Seed Oil Scout" brand + product in StefanBrain, then get 3 angles and one 15-30s script from it.
2. Lock the character/set: one reference image, then pose stills from it.
3. Anton approves the generate package (prompts, script, voice) before any credits are spent.
4. Generate the clips → QA → fix → stitch and caption → Anton reviews.
5. Write what went wrong into a `seed-oil-scout` prompting skill file so the next video is better.
