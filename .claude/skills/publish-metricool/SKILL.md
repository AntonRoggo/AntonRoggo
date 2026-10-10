---
name: publish-metricool
description: Schedule an approved edited video on every connected social platform through Metricool. Use when the user approves a video ("approved", "post it", "schedule this", "send it out") or asks to publish, schedule, or upload a finished video to Instagram, TikTok, YouTube, Facebook or other platforms via Metricool.
---

# Publish an approved video via Metricool

Only run this for a video the user has explicitly approved in this conversation (e.g. "approve clip_edited.mp4", "this one's good, post it"). Approval of one video never covers another. If it's unclear which file they mean, ask.

## Requirements

- The Metricool connector must be connected. Its tools are `mcp__Metricool_Social_Media_Management__*`: `getBrandSettings`, `getBestTimeToPostByNetwork`, `getScheduledPosts`, `createScheduledPost`, `createScheduledPostForReview`, `updateScheduledPost`. Load them with ToolSearch. If they're missing, stop and tell the user to connect Metricool at https://claude.ai/customize/connectors and start a new session. Never fake a scheduled post.
- Settings are in `publishing/config.json` (brand, platforms, timezone, posting slots, caption style). Read it first.
- Metricool needs the video at a public URL in `info.media`. Google Drive and Dropbox links are uploaded by Metricool automatically (Google Drive must be linked in the user's Metricool account). Follow `config.media_hosting`; if it isn't set up, ask the user.

## Steps

1. **Check the file.** It must be in `output/` and must be an `edit_video.py` output (captions, cuts and audio boost already applied). Check it with `ffprobe`: duration, resolution, and that it's vertical (9:16) when posting Reels/Shorts/TikTok.
2. **Get the brand.** Call `getBrandSettings` and pick the brand whose blogId is `config.blog_id`. Use its timezone unless `config.timezone` is set. Note which networks are actually connected to that brand. Use every network that is both connected and in `config.platforms`, and report any configured platform that isn't connected.
3. **Write the caption.** Base it on the transcript (`output/<name>_edited.ass` holds the caption text) and follow `config.caption`. Make a version per platform where limits differ: YouTube needs a title (≤100 chars) and the "made for kids" setting (`config.youtube.made_for_kids`); TikTok and Instagram captions should keep hashtags at the end.
4. **Pick the time.** If `config.schedule.mode` is `best_time`, call `getBestTimeToPostByNetwork` for each network and take the best slot in the next `config.schedule.within_days` days. If it's `slots`, use the next free slot from `config.schedule.slots` that doesn't already have a post (check `getScheduledPosts`). Always in `config.timezone`, always in the future.
5. **Show the plan and get a final OK.** Before scheduling anything, show the user one table: platform, post type (Reel/Short/TikTok/…), date and time, caption/title. Scheduling posts publishes to their public accounts, so wait for a yes. If `config.confirm_before_scheduling` is `false`, the earlier approval is enough and you skip this step.
6. **Schedule.** Call `createScheduledPost` (or `createScheduledPostForReview` with `config.reviewers` if that list isn't empty). Use one post per platform so each gets its own caption and time. `info` must include `providers`, `publicationDate` {dateTime, timezone}, `text`, `media` [video URL], `autoPublish` (true unless `config.draft`), `draft`, and the network block for that platform:
   - Instagram: `instagramData: {"type": "REEL", "showReelOnFeed": true}`
   - Facebook: `facebookData: {"type": "REEL"}`
   - YouTube: `youtubeData: {"title": ..., "type": "short", "privacy": "public", "madeForKids": config.youtube.made_for_kids}`
   - TikTok: `tiktokData: {"privacyOption": "PUBLIC_TO_EVERYONE"}`
   Set `videoCoverMilliseconds` only when `config.cover_frame_ms` is set; otherwise leave the cover fields out entirely, because if a cover isn't supported for a network Metricool rejects the whole post.
7. **Verify and log.** Call `getScheduledPosts` for the publish dates to confirm each one exists with the right time. Append one line per post to `publishing/log.md` (date scheduled, file, platform, publish time, Metricool post id, uuid, plannerUrl), commit, and push.
8. **Report** the table of what was scheduled, plus anything that failed and why. Never claim a post was scheduled unless step 7 confirmed it.

## Changes after scheduling

To move or cancel a post, use `updateScheduledPost` with the id and uuid from `publishing/log.md`, sending the post's full original content with only the change. Updating gives the post a new id, so update the log. The connector has no delete tool: to cancel a post, send the user the plannerUrl to delete it in Metricool.
