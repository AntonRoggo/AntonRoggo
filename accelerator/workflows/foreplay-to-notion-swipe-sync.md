# Foreplay to Notion Swipe Library sync (manual, 2026-09-24)

Where Foreplay saves go: the Swipe Library database in Creative OS (collection 22a7413e-78d6-4143-a7f4-bb3ed9ebab5b), not the Creatives Tracker. The Tracker links to Swipe Library rows through its Swipe Source relation. The Creative OS page says the same: "the sync worker pulls every new Foreplay save via the API into a row."

How the pull works:
- Foreplay MCP: get_swipefile_ads returns only the 10 newest saves. get_board_ads(board_id, cursor) pages 10 at a time, newest first; the cursor is the saved-at timestamp in ms of the last item. Boards: #client-thetallowedtruth zpZ3KZOmXhswbxky6Kra, #all bCMNQeCjyRmA99PlVBka, #client-lymphoria Tn9pC1J1eqayRomNq5FM.
- Every page overflows the tool result; parse the saved file with Python, never read it.
- "New" = Foreplay ID not already in the Swipe Library (query it first; the sync worker last ran 2026-07-30).
- Page shape that works: notion-create-pages with parent {data_source_id} and pages [{properties, content}]. Properties: Name ("Brand: descriptor", colon not dash), Foreplay ID, Link, Hook (first two transcript sentences), Transcript (1,900-char cap), Source Foreplay, Status Transcribed or New, Still Running, Brand Fit (TT client page 39aae2bae08e817bbcfbdc7753959a04 when the ad is on the TT board). Body: video URL, boards, headline, primary text, timestamped transcript.
- notion-update-page takes page_id, command update_properties, properties at top level.

State after 2026-09-24: 25 videos saved after Aug 15 imported (IDs in scratchpad foreplay_new.json). 17 image/DCO saves from the same window not imported. The Aug 14 bulk-save day (Dr. Squatch, HIKE, Hollow Socks, beam, SmoothSpine, dozens of pages on both boards) not imported; ask before backfilling.

Related: [[Creative OS]] [[the-tallowed-truth]]
