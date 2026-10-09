---
name: boost-audio
description: Boost a video's or audio file's volume as loud as possible without clipping while keeping it natural (no jumps in volume, no pops at cuts). Use when the user asks to boost, normalize, raise, or max out audio gain, make a video louder, or fix quiet audio.
---

# Boost audio

Run the repo script on each file the user names:

```bash
python3 boost_audio.py <input> [-o <output>]
```

Default output is `<name>_loud.<ext>` next to the input. The video stream is copied, only audio is re-encoded.

What it does:
- High-pass at 80 Hz, a slow leveller that evens out quiet and loud sections over ~15 s windows, then a gentle 3:1 compressor that tames individual loud words.
- Two-pass `loudnorm` in linear mode to -12 LUFS: one steady gain change, so there's no pumping.
- True-peak limiter with a -1 dBTP ceiling. That's as close to 0 as is safe: AAC/MP3 encoding pushes peaks up slightly, so a 0 dB ceiling would clip after export.

`edit_video.py` already runs this on every edited video, and fades each cut by 15 ms so cuts don't pop. Only use this skill directly for videos that don't go through `edit_video.py`.

After running, report the before/after loudness the script prints. If the user wants it louder or quieter, change `TARGET_LUFS` in `boost_audio.py` (-14 is the YouTube/Spotify level, -10 is very loud and starts to sound squashed). Never raise `TRUE_PEAK` above -1.
