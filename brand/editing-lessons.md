# Editing lessons

Every piece of feedback Anton gives on an edit becomes a rule here. Read this before every edit and check the finished video against it before showing it to him.

Format: `- [date, video] Rule. (What went wrong / what he said.)`

## Rules

- [2026-10-10, setup] Activity footage (kitesurfing, hiking, climbing, surfing...) is "action", not B-roll; use it when he describes doing that thing. Don't judge it on beauty.
- [2026-10-10, setup] Prefer clips he already reuses in finished edits (e.g. Montenegro orange-juice-on-sunbed) over prettier unused ones.
- [2026-10-10, setup] "Vibing" moments (lawn chairs, dancing, fire pits, hangouts) are wanted B-roll, even without him in shot.
- [2026-10-10, setup] Every cut is a J-cut: audio of the next clip leads its picture slightly (0.2s), so cuts feel smooth instead of choppy.
- [2026-10-10, Short Form batch] Several takes of the same script in a folder = an A/B test: edit every take as its own version (name them A, B, C...), don't merge them.
- [2026-10-10, Short Form batch] When he talks about doing something (e.g. "shoot some guns"), cut to footage of HIM doing it. Identify him by what he's wearing in the talking take (taco/gun day: light sage-green linen shirt), not by guesses.
- [2026-10-10, Short Form batch] Never cut the payoff even if it's silent: the pool shot after "watch this", the bite in a taste test. Use `--keep` for those moments; trim the dead walking/chewing around them.
- [2026-10-10, Short Form batch] Cut on-camera asides and outtakes ("I shouldn't have said that", "am I in the frame?") with `--drop` when the automatic mistake detection misses them.
- [2026-10-11, Short Form feedback] Captions follow sentence flow first: never put the first word of the next sentence on the current caption ("life's not that complicated" / "eat some tacos", not "...complicated eat"). 3 words is a maximum, not a target.
- [2026-10-11, Short Form feedback] Captions centred on screen, not in the lower third. If centred would cover his face, place them just below his chin.
- [2026-10-11, Short Form feedback] Captions are all lowercase with no punctuation.
- [2026-10-11, Short Form feedback] Mix the audio so background noise is low and his voice is clear (denoise before loudness; never use processing that lifts the background in pauses).
- [2026-10-11, Short Form feedback] J-cuts must have NO pause at the cut: trim tight to the words and overlap the audio (next clip's sound crossfades in over the last ~0.1s of the previous one), then the picture follows.
- [2026-10-11, Short Form feedback] No split-second flashes back to camera between B-roll shots. B-roll starts and ends exactly when a caption starts (cut on words); any gap under 1.5s between B-roll shots (or before the end) gets filled by the previous shot.
- [2026-10-11, UofT feedback] No B-roll in the first ~3 seconds: the hook stays on his face, not overlaid.
- [2026-10-11, UofT feedback] No long pauses between sentences: any pause over ~0.35s is cut with a J-cut. Detect pauses from the audio, not word timestamps (the speech model stretches words over the silence after them).
- [2026-10-11, B-roll feedback] B-roll must cover every frame of its slot: joins between B-roll shots and back to camera must be frame-exact (build the picture from whole-frame pieces, not overlay windows).
- [2026-10-11, UofT feedback] Never show a silent shot of his face (e.g. after "don't let your life get boring"). Clips are trimmed to where his voice actually starts/stops; if there must be a silent moment, extend the B-roll over it instead.
- [2026-10-11, UofT feedback] Watch the exact seconds of every B-roll clip you use, not just the clip's opening frames. Never use a shot of the floor/path; "introduce some variety" got kitesurfing instead.
- [2026-10-11, UofT feedback] "Try the good food" type lines: a clip of HIM eating (alone), not just food or a group.
- [2026-10-11, fish feedback] Talking pieces are conversational: only cut pauses longer than ~0.7s, unless B-roll covers the cut (then cut tighter / J-cut heavily). Too many cuts feel choppy.
- [2026-10-11, UofT feedback] The 3-second no-B-roll hook rule can be overridden when Anton asks for a specific clip there (plan entry "in_hook": true).
- [2026-10-11, UofT feedback] Never use clips in `broll/banned.json` (e.g. the UofT library interior shot, the bike-path/floor shot). Pick aesthetic shots for "beautiful spots" lines (e.g. Lake Ontario pebble beach, red autumn tree).
- [2026-10-11, music] Videos with B-roll get music: "charmed - stella" (Dropbox `[04] Video Editing Resources/audio/songs/`), at -8 dB, with the song's first beat landing exactly on the first B-roll frame (`--music`).
- [2026-10-11, UofT feedback] No ~1s breakaways to camera next to B-roll. When a B-roll shot ends on a new line, the J-cut means the old clip (e.g. him smiling after "picnic in the park") would still show for a split second before the jump cut. So B-roll runs on until the jump cut (or starts at it). Any camera piece under 1.5s next to B-roll gets swallowed by the B-roll (automatic in `snap_plan`).
- [2026-10-11, taco feedback] Music is the default for B-roll edits, not a must: some videos get no song (the Texas taco video has no music). Ask or follow his note per video.
