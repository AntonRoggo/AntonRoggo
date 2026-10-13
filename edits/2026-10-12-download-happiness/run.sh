#!/bin/sh
# Download happiness (oyster giveaway), v2. Source take: Dropbox
#   /[01] Clients/[03] Anton/Short Form/Oyster Give Away/DJI_20260903022524_0071_D.MP4  (id:wdILo7p6X3AAAAAAAACZEg)
# downloaded to input/giveaway/0071.mp4. Source times below are in that file.
#   43.7  hook: "Downloading happiness." (oysters held up)
#   45.0-49.2 dropped: "Wait." + "Everybody put cuteness overload in the comments" aside
#   49.3-57.95 kept whole: "How do you download happiness? Forty-eight oysters and a chicken lollipop. Taste test." (flowing table talk, no pause cuts)
#   57.95-59.3 cut: camera gets bumped
#   59.3-68.4 kept whole: the bite, "Mmm." ... "Yum." (both reactions with the beat between)
#   69.1-69.85 dropped: "Again," (nothing came before it in this edit)
#   up to "Namaste." at 82.7; "Here we go" dropped
# v1 (scheduled 2026-10-13 10:52 ET) was edited before the review tool; no recipe exists for it.
cd "$(dirname "$0")/../.."
python3 edit_video.py input/giveaway/0071.mp4 \
  --hint "Downloading happiness. How do you download happiness? Forty-eight oysters and a chicken lollipop. Taste test. Mmm. Yum. If you want to win 75 oysters, I'm going to ship them straight to your door. Comment oysters below so you can download happiness. Namaste." \
  --drop 0-43.5 --drop 45.0-49.2 --drop 69.1-69.85 --drop 83.2-84 \
  --keep 49.3-57.95 --keep 59.3-68.4 \
  -o output/giveaway/2026-10-12-download-happiness_v2.mp4
