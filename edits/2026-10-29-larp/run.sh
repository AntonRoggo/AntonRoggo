#!/bin/bash
# "Do This" LARP batch (Dropbox: Short Form/Larp Clips Oct 29). Usage: run.sh [--plan-only] [name...]
cd /home/user/AntonRoggo
I=input/larp/raw; O=output/larp; B=edits/2026-10-29-larp
MUSIC="input/larp/music/charmed - stella.mp3"
EXTRA=(); [ "$1" = "--plan-only" ] && { EXTRA=(--plan-only); shift; }
ONLY=" $* "
run(){ name=$1; shift; [ "$ONLY" != "  " ] && [[ "$ONLY" != *" $name "* ]] && return
  echo "=== $name"; mb=(); [ -f $B/$name.broll.json ] && mb=(--broll $B/$name.broll.json --music "$MUSIC")
  python3 edit_video.py "$@" "${mb[@]}" "${EXTRA[@]}" -o $O/$name.mp4 2>&1 | grep -v -i "warn\|hf_token"; }
GRANDPA="The goal this winter is to be as close to a retired Italian grandpa as possible. Affogatos for breakfast. Two-hour lunch with the boys. Shopping at the farmers market. Evening walk with your hands behind your back. In bed by ten."
LETS="Let's all keep watching reels in bed with the brightness on max. Let's hit snooze four times because it's too cold to see the sunrise. Let's all eat lunch at our desk and be exhausted. Who's with me?"
run 03_italian_grandpa_A_0011 input/larp/clean/0011.mp4 --hint "$GRANDPA" --drop 13.9-16.3 --drop 24.0-27.0 --fix "5.6-6.8=possible@5.70-6.24"
run 03_italian_grandpa_B_0016 $I/0016.mp4 --hint "$GRANDPA" --fix "0-6.5=The@5.68-6.20 goal@6.20-6.46" --drop 27.4-29.9
run 04_lets_all_A_0012 $I/0012.mp4 --hint "$LETS" --fix "0-0.9=Let's@0.46-0.72 all@0.74-0.9" --cut 0-0.28
run 04_lets_all_B_0014 $I/0014.mp4 --hint "$LETS" --drop 0-34.0 --drop 41.0-42.6 --end 45.2
run 04_lets_all_C_0015 $I/0015.mp4 --hint "$LETS"
run 05_holiday_habit_0017 $I/0017.mp4 --hint "You don't need a holiday to feel like you're on holiday. Sit down for breakfast. Go for a swim in the lake at lunch. Take the scenic way. Be a tourist in your own city." --fix "20.6-21.9=sit@21.28-21.84" --cut 20.6-21.2
run 06_cortisol_supplement_0018 $I/0018.mp4 --hint "My favorite cortisol supplement is a dozen oysters, some orange juice on the beach, and a couple friends who don't check their phones. Follow this protocol daily. Side effects might include being a little too jolly." --fix "0-12.7=My@0.0-0.64 favorite@0.64-1.0 cortisol@1.0-1.48 supplement@1.48-2.06 is@2.06-2.3 a@2.3-2.56 dozen@2.56-2.8 oysters@2.8-3.4 some@11.0-11.24 orange@11.24-11.6 juice@11.6-11.86 on@11.86-12.12 the@12.12-12.28 beach@12.28-12.62" --drop 29.0-32.0
run 07_nobodys_watching_0019 $I/0019.mp4 --hint "I'm eating a dozen oysters on a bench at 10am. Nobody's watching you. Nobody cares. Swim in September. Dance terribly in front of everyone. Talk to the stranger at the bar." --cut 2.3-3.33 --fix "2.6-3.55=I'm@3.40-3.58"
run 08_old_people_right_2_0020 $I/0020.mp4 --hint "Old people were right again. Soup fixes most things. Evening walk after dinner. Call your mama on a Sunday. Go to bed when it gets dark, not when your phone dies."
run 11_waste_a_winter_0021 $I/0021.mp4 --hint "Five ways to waste your winter. Hibernate in bed all day. Scroll in bed until 1am. Skip the sauna. Eat lunch at your desk. Wait till spring to start living. We ain't doing that."
run 14_the_trade_0022 $I/0022.mp4 --hint "Bro, that watch costs more than my whole year. My whole year is just swimming with my boys, orange juice on the beach, cheeky oysters on a Friday, and friends who actually show up." --drop 0-22.0
echo ALLDONE
