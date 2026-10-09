---
name: publish-metricool
description: Schedule an approved edited video on every connected social platform through Metricool. Use when the user approves a video ("approved", "post it", "schedule this", "send it out") or asks to publish, schedule, or upload a finished video to Instagram, TikTok, YouTube, Facebook or other platforms via Metricool.
---

# Publish an approved video via Metricool

Only run this for a video the user has explicitly approved in this conversation (e.g. "approve clip_edited.mp4", "this one's good, post it"). Approval of one video never covers another. If it's unclear which file they mean, ask.

## Requirements

- The Metricool connector (Metricool's MCP server) must be connected. Search for its tools with ToolSearch (`metricool`, `schedule post`, `brands`). If none are found, stop and tell the user to connect Metricool at https://claude.ai/customize/connectors and start a new session. Never fake a scheduled post.
- Settings are in `publishing/config.json` (brand, platforms, timezone, posting slots, caption style). Read it first.
- Metricool needs the video at a public URL. Get one as `config.json` → `media_hosting` says. If it isn't set up, ask the user.

## Steps

1. **Check the file.** It must be in `output/` and must be an `edit_video.py` output (captions, cuts and audio boost already applied). Check it with `ffprobe`: duration, resolution, and that it's vertical (9:16) when posting Reels/Shorts/TikTok.
2. **Get the brand.** Call the connector's list-brands tool and pick the brand named in `config.json`. Note which networks are actually connected to that brand. Use every network that is both connected and in `config.platforms`, and report any configured platform that isn't connected.
3. **Write the caption.** Base it on the transcript (`output/<name>_edited.ass` holds the caption text) and follow `config.caption`. Make a version per platform where limits differ: YouTube needs a title (≤100 chars) and the "made for kids" setting (`config.youtube.made_for_kids`); TikTok and Instagram captions should keep hashtags at the end.
4. **Pick the time.** If `config.schedule.mode` is `best_time`, call the connector's best-time-to-post tool for each network and take the best slot in the next `config.schedule.within_days` days. If it's `slots`, use the next free slot from `config.schedule.slots` that doesn't already have a post (check the connector's list-scheduled-posts tool). Always in `config.timezone`, always in the future.
5. **Show the plan and get a final OK.** Before scheduling anything, show the user one table: platform, post type (Reel/Short/TikTok/…), date and time, caption/title. Scheduling posts publishes to their public accounts, so wait for a yes. If `config.confirm_before_scheduling` is `false`, the earlier approval is enough and you skip this step.
6. **Schedule.** Read the schedule-post tool's input schema and fill it from the plan. Use one post with several providers when every platform shares the time and caption, otherwise one post per platform. Set auto-publish on (not draft) unless `config.draft` is true. Video post types: Instagram Reel, Facebook Reel, YouTube Short, TikTok video.
7. **Verify and log.** List the scheduled posts to confirm each one exists with the right time. Append one line per post to `publishing/log.md` (date scheduled, file, platform, publish time, Metricool post id), commit, and push.
8. **Report** the table of what was scheduled, plus anything that failed and why. Never claim a post was scheduled unless step 7 confirmed it.

## Changes after scheduling

To move or cancel a post, use the connector's update/delete tools by the id in `publishing/log.md`, then update the log.
