# B-roll catalogue

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

`used_in` lists the posted videos that used the clip, so the same shot isn't repeated in back-to-back reels.
