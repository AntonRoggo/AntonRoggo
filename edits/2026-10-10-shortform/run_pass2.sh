#!/bin/bash
cd /home/user/AntonRoggo
I=input/shortform; O=output/shortform
FISH="Mate, fish and chips on a Friday, cooked in tallow, cheeky pint, pint of Guinness, Bosh."
run(){ name=$1; shift; echo "=== $name"; python3 edit_video.py "$@" -o $O/$name.mp4 2>&1 | grep -v -i "warn\|hf_token"; }
run fish_D_0065_DRAFT $I/lrf/fish_0065.lrf --keep 36.2-38.5
run poolbar_0144 $I/poolbar/0144.mp4 --keep 18.5-25.7
run taco_0175_DRAFT $I/lrf/taco_0175.lrf --drop 0-6.6 --keep 22.3-25.0 --broll $O/taco_broll.json
run uoft_A_0126_DRAFT $I/lrf/uoft_0126.lrf --broll $O/uoft_A_broll.json
run uoft_B_0127_DRAFT $I/lrf/uoft_0127.lrf --broll $O/uoft_B_broll.json
echo ALLDONE
