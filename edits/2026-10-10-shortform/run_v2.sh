#!/bin/bash
cd /home/user/AntonRoggo
I=input/shortform; O=output/shortform
FISH="Mate, fish and chips on a Friday, cooked in tallow, cheeky pint, pint of Guinness, Bosh."
run(){ name=$1; shift; echo "=== $name"; python3 edit_video.py "$@" -o $O/$name.mp4 2>&1 | grep -v -i "warn\|hf_token"; }
run fish_A_0064 $I/fish/0064.mp4 --hint "$FISH" --drop 9.2-11.2
run fish_B_0066 $I/fish/0066.mp4 --hint "$FISH"
run fish_C_0068 $I/fish/0068.mp4 --hint "$FISH" --keep 10.3-12.8 --drop 17.0-18.3
run fish_D_0065_DRAFT $I/lrf/fish_0065.lrf --hint "$FISH Balance. Locking in. You're basically cooking yourself mentally. Go all in." --keep 36.2-38.5
run poolbar_0144 $I/poolbar/0144.mp4 --hint "In Texas, the 80s, pool hall." --keep 18.5-25.7
run freddy_0139 $I/freddy/0139.mp4 --drop 8.75-9.8
run uoft_A_0126_DRAFT $I/lrf/uoft_0126.lrf --hint "Be a tourist in your own city." --broll $O/uoft_A_broll.json
run uoft_B_0127_DRAFT $I/lrf/uoft_0127.lrf --hint "Be a tourist in your own city." --broll $O/uoft_B_broll.json
echo ALLDONE
