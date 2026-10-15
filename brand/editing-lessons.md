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
- [2026-10-11, taco feedback] Never reveal a punchline in the captions before he says it. A silent beat mid-sentence (chewing, thinking about the score) shows "..." until he speaks ("this is like a" / "..." / "9 out of 10 taco"). Word end times from the speech model are capped at a natural length, because it stretches words over pauses.
- [2026-10-11, UofT feedback] The closing line can go back on his face ("don't let your life get boring"). Cut back exactly where the take of him saying that line starts, never on the tail of the previous take. The end stretch only has to be 1s (`MIN_END_FACE`), not 1.5s.
- [2026-10-12, giveaway feedback] Captions stay at ONE height for the whole video, never jumping up and down between captions. Use the lowest position any caption needs to clear his face (centre if his face is never in the way).
- [2026-10-12, giveaway feedback] When a clip is added onto a finished edit that has music (e.g. a giveaway CTA), the music keeps playing under the new clip at the same level, then fades out at the very end. If it's "charmed - stella", continue the song from the exact spot; otherwise separate the music from the voice and continue it with a seamless loop.
- [2026-10-13, download happiness feedback] Never cut the hook. Before dropping the start of a take, watch it: the hook is usually the first strong line + reaction ("Downloading happiness" with the oyster held up), not the first line of the script that follows. If a later line repeats the hook ("How do you download happiness?"), keep both: hook first.
- [2026-10-13, download happiness feedback] Talking must sound finished and natural: never clip the ends (or soft starts) of words. Keep ~0.15 s before and ~0.3 s after speech at every cut; the J-cut crossfade must fall in that padding, not on the word.

- (2026-10-15) Voiceover scripts for Anton come as a clean teleprompter first: only the words he reads, one sentence per line, no clip names or visual direction. Put the shot list (which clip goes under each line) in a separate "Editor notes" section below.
- [2026-10-15, "where your oysters come from" feedback] Give viewers context, not tight close-ups of the item. Prefer wide or medium shots of people doing the thing (lifting cages, the crane hauling a cage out of the water, eating an oyster out on the water) over tight shots of hands or cages. Each shot should show where we are and what is happening.
- [2026-10-15, same] Open a location with an establishing shot of us in it (for the farm: us out on the water / on the boat), not a detail shot.
- [2026-10-15, same] Match the shot to the words literally: "we take them out with the crane" shows the crane lifting a cage out of the water; "eating" shows us eating there, in that place.
- [2026-10-15, same] Pick clean-looking shots: skip overexposed or washed-out clips (or fix their exposure and colour), and frame away from mud and mess. Choose the wider, cleaner angle when one exists.
- [2026-10-15, "five things" feedback] Phone footage is often HDR (HLG/PQ, BT.2020). Always tone-map it to Rec.709 before editing, or it looks washed out and overexposed. Both `edit_video.py` (B-roll) and `tools/voiceover_edit.py` now do this automatically; check any new pipeline for it.
- [2026-10-15, same] Voiceover edits run tight: no pauses between lines (unlike talking-head edits, where short pauses stay). Lines butt up against each other with J-cut-style overlaps, keeping only the ~0.15 s / 0.3 s padding so no word is clipped.
- [2026-10-15, same] Master voiceover audio properly: remove background noise (knife/cutting sounds, chatter, room tone) so only his voice remains, then -12 LUFS / -1 dBTP. Listen to the whole track for leftover noise before showing it.
- [2026-10-15, same] List videos ("5 things...") get a headline on screen for the whole video at the top: the title in the caption style, e.g. "five things no one tells you about oysters".
- [2026-10-15, "bar vs 60 oysters" feedback] Don't limit B-roll to one shoot. Pull from the whole library (`broll/catalog.json`, `broll/action.json`, `broll/raw/*.json`, ANTON MASTER BROLL) when a line is about his lifestyle. A run of lines about eating oysters becomes a montage of him eating oysters in different places (Toronto, Spain, France, Brazil, the farm).
- [2026-10-15, same] Shots must literally match the setting in the words: "at the bar" opens on him at a bar; "dinner" shows dinner; health or testosterone lines show him training or doing something physical.
- [2026-10-15, same] Choose calm, steady shots over shaky or whip-pan ones (e.g. "us on the boat": a steady shot of us sitting on the boat).
- [2026-10-15, gatekeep feedback] Shots move the story forward step by step: on the boat, then walking out into the water to the cages, then the work, then eating. Every new shot is the next step in the story, so it's clear where we are (an oyster farm).
- [2026-10-15, same] Voiceovers are very snappy: no dead space between words or sentences, anywhere. This includes long music-only stretches, which feel like dead space; don't end a voiceover video on a silent montage.
- [2026-10-15, same] Use everything he recorded for the script. Don't drop lines or the CTA to make it shorter or to copy another creator's format; if it seems too long, ask first.
- [2026-10-15, booked-out feedback] When he mispronounces a word on purpose or by accident (e.g. "oysters"), the caption puts that word in quotation marks. This is the one exception to the no-punctuation rule.
- [2026-10-15, same] A long pause before the CTA ("if you want to win...") gets J-cut out like any other pause; the CTA follows straight on.
- [2026-10-15, Terry Black's feedback] End on the natural sign-off ("cheers") plus about 1 s, and cut filler outros like "that's today's video". Check unclear words by ear (he said "boy"); don't trust the transcript when it sounds odd.
- [2026-10-15, day-in-the-life feedback] Colour grade every edit for a healthy, natural look: water slightly bluer, greens a little greener, skin not pale. Use one consistent grade across the video, applied after the HDR→Rec.709 tone mapping.
- [2026-10-15, same] Prefer steady, well-framed shots. Skip clips where the camera walks in so close the framing is lost.
- [2026-10-15, same] Scene-setting lines ("sunrise") can use pure scenery B-roll with nobody in it. Pick the most beautiful one.
- [2026-10-15, Terry Black's feedback] Captions must match what he actually says. In noisy places the speech model invents words ("let me tell you" / "I'm a dog" where he says "I'm a boy"): re-listen to any short or low-confidence stretch and correct it with `--fix START-END=TEXT` (source times), never ship a guessed caption.
- [2026-10-15, Terry Black's feedback] End on the last real line (e.g. "cheers"), about 1 s after it, and cut sign-offs like "all right, that's today's video" (`--end SEC`, source time).
- [2026-10-15, "bar vs 60 oysters" v2] Noisy voiceover recordings: separate the voice with demucs (`--two-stems vocals`) and use that stem as the plan's voice, so speech detection trims tight and only his voice is left (RNNoise + `gate_db` on top). Then voiceover lines butt together: ~0.12 s before / 0.2 s after speech, 0.1 s overlap, no audible gap.
- [2026-10-15, same] Check every DJI clip for flat log footage (D-Log / D-Log M: grey, low contrast) before using it, and convert it to Rec.709 if so; phone HDR (HLG/PQ) is tone-mapped. Look at the contact sheet: nothing washed out.
- [2026-10-15, Anton's rule] VOICEOVERS: zero space between sentences. J-cut everything so each sentence starts the moment the last one ends (overlap the joins). Talking-head videos can keep short natural pauses, but voiceover cuts are always super tight.
- [2026-10-15, Anton's rule] Avoid shots that are cropped in so far they're hard to read (e.g. a heavy punch-in on a selfie to isolate something). If a clip needs a big crop to work, use a different clip. Show it plainly and wide enough to understand at a glance.
