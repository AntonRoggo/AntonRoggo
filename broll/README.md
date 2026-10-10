# B-roll catalogue

**Status (Oct 2026):** 2,492 videos from the 12 ANTON MASTER BROLL folders created since July 2025 were viewed and logged in `raw/` (every clip, any kind: broll, talking, other). `catalog.json` holds the 249 best B-roll clips (quality 4-5, duplicates removed). Not yet covered: `toronto summer 2025`, `ALL BROLL`, and older folders. Skipped as too large: `brazil 2025/day 6/finished/dec 5.mov` (a finished edit).

`action.json` holds clips of Anton or friends doing an activity (kitesurfing, hiking, snowboarding, climbing...), rated on `action_quality` (how clearly the activity shows), with `activity` and `who` fields. Clips rated 1 (barely visible) are left out.

Use `raw/` to find talking takes or lower-rated clips; use `catalog.json` when picking B-roll for an edit.

`catalog.json` lists only the best clips from the Dropbox B-roll library, one entry per clip:

```json
{
  "dropbox_id": "id:...",
  "path": "/[01] Clients/[03] Anton/ANTON MASTER BROLL/...",
  "shot": "sipping coffee",
  "tags": ["morning", "cafe", "warm", "close-up"],
  "location": "Florence",
  "orientation": "vertical",
  "duration": 6.2,
  "usable": [[0.5, 5.0]],
  "quality": 5,
  "used_in": []
}
```

Shot types so far: shuffling leaves, fizzing milk, sipping coffee, licking bottle, sipping green tea, stacking. Add new ones as they come up.

Tag `vibing` = Anton or friends chilling or dancing: lawn/lounge chairs, sunbeds, lying in the grass or on rocks, dancing. Search tags for it.

`used_in` lists the posted videos that used the clip, so the same shot isn't repeated in back-to-back reels.
