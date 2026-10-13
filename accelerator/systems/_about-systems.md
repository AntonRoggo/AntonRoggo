# Systems

Working stores for the production pipelines. Each pipeline gets one folder here for the files the vault has no other home for: seed banks, briefs, matrix files, primer cuts, bots, data.

- systems/genesis-ad-system/{client}/ (plus config/.env for API keys and context/ for gallery code)
- systems/creative-strategy-system/{brand}/
- systems/bot-builder/ for standalone bot drafts
- systems/copy-lint/ holds lint_copy.py, the guard that checks everything written to copy/ against the voice rubric (em dashes block, triplets and vague pronouns warn). Wired as a PostToolUse hook in .claude/settings.json.

Rules: this is a workbench, not memory. Proven ads live in winners/ and swipes/, finished work in copy/ or creatives/. Nothing here is the record.

Related: [[The Script]] [[Workbench vs Memory]]
