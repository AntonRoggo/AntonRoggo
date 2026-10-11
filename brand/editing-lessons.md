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
