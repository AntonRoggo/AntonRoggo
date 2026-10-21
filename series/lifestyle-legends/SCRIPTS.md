# Lifestyle Legends: 9 scripts

There are three formats, each copied from one of your outliers, written for each of three legends: Yvon Chouinard, Ian Fleming and Jack London. Each script has a matching plan in `plans/`, so once you've filmed it the editor can cut it:

```bash
python3 edit_legend.py series/lifestyle-legends/plans/<plan name>.json
```

Put the footage for each script in `input/<plan name>/`, using the file names given in the script. The edit rules are in [EDITING_STYLE.md](EDITING_STYLE.md).

Before posting, check every fact marked ✓. They're from memory and haven't been checked against sources.

## The three formats

| | Format | Copied from | Length | Shape |
|---|---|---|---|---|
| **A** | "A day in the life if you're [legend]" | It's simple really (1.18M, 51×), Sunday night lights (21×) | 12–20 s | Hook on camera, then 4–6 quick actions, each shown as it's said, ending on one contrarian line |
| **B** | "Sometimes life calls for [absurd thing]" | 48 oysters (180K, 69×, 9% engagement) | 35–45 s | One seated take with an absurd prop. Then "Why???", the NPC problem, "How do you break free?", the legend's story as the "science" with screenshot pop-ups, "So what's the takeaway here?" and "Namaste." |
| **C** | "Please do not [X]" | Please do not spike my cortisol (124K, 5.5×) | 12–20 s | A 2 s skit cold open under a white "FAILED ATTEMPT AT…" label, then you in paradise telling the legend's story as an exasperated aside, ending on the day of the week |

Deliver all three formats deadpan. You believe every word.

---

## Yvon Chouinard

### A. Day in the life (`chouinard_1_day_in_the_life`)

| File | Say | On screen |
|---|---|---|
| `01_hook.mp4`: selfie at a beach or crag at sunrise, board or rope on your shoulder | "A day in the life if you're Yvon Chouinard." | caption |
| | "Wake up in the dirt." | cutaway `sleep.mp4`: you crawling out of a sleeping bag or van |
| | "Climb all morning." | cutaway `climb.mp4`: bouldering or a ridge scramble |
| | "Surf when the swell shows up." | cutaway `surf.mp4`: paddling out or catching a wave |
| | "Make your own gear and sell it out of your car." | cutaway `trunk.mp4`: opening a car boot full of gear |
| `02_close.mp4`: sitting on the sand or at a café, wet hair | "Accidentally build Patagonia. Let your people go surfing." | caption |

✓ Verify: lived out of his car; forged and sold his own climbing gear (pitons) out of it.

### B. Sometimes life calls for (`chouinard_2_sometimes_life_calls_for`)

`01_talk.mp4`: one seated take at a camp table, fleece on, with a can of cat food and a camping stove in front of you.

| Say | On screen |
|---|---|
| "Sometimes life calls for cat food." | caption |
| "Why???" | |
| "Rent is due. I have a LinkedIn. I'm an NPC." | |
| "How do you break free?" | |
| "Okay. Yvon Chouinard. The sixties, living in Yosemite on like a dollar a day." | pop-up `yosemite.jpg`: an archive photo of Camp 4 or El Capitan |
| "He ate cat food so he could keep climbing." | |
| "Taught himself blacksmithing, sold climbing gear out of the back of his car." | pop-up `gear.jpg`: old pitons or a forge |
| "That turned into Patagonia." | pop-up `patagonia.jpg`: the logo or a shopfront |
| "Then in 2022 he gave the whole company away. Earth is now the only shareholder." | pop-up `headline.png`: a screenshot of the news headline |
| "So what's the takeaway here?" | |
| "Eat the cat food. Climb the rock. The billion-dollar company shows up later." | |
| "Don't actually eat the cat food." | |
| "Namaste." | |

✓ Verify: the cat-food story; living on about $1 a day; Patagonia given away in 2022 ("Earth is now our only shareholder").

### C. Please do not (`chouinard_3_please_do_not`)

| File | Say | On screen |
|---|---|---|
| `01_coldopen.mp4`: laptop open on a bench by the surf; you look at the screen, then at the waves | "Alright, let's answer some emails." | label: **FAILED ATTEMPT AT NOT GOING SURFING** |
| `02_talk.mp4`: sitting on the sand after a surf, board beside you | "Please do not ask me to come into the office." | the label disappears here |
| | "The founder of Patagonia literally wrote a book called Let My People Go Surfing." | pop-up `book.jpg`: you holding the book |
| | "Surf's up, you go surfing. That's company policy." | |
| | "I'm just following the policy, man." | |
| | "It's a Tuesday." | |

✓ Verify: Patagonia's "let my people go surfing" flexible-time policy.

---

## Ian Fleming

### A. Day in the life (`fleming_1_day_in_the_life`)

| File | Say | On screen |
|---|---|---|
| `01_hook.mp4`: selfie on a sea wall or terrace, mask on your forehead | "A day in the life if you're Ian Fleming." | caption |
| | "Wake up on the water. Swim the reef." | cutaway `snorkel.mp4`: underwater or snorkel shot |
| | "Spear a fish." | cutaway `spear.mp4`: a speargun, or a fish at the market |
| | "Write two thousand words." | cutaway `write.mp4`: a typewriter or notebook on a terrace |
| | "Lunch." | cutaway `lunch.mp4`: a plate and a view |
| | "Nap." | cutaway `nap.mp4`: hammock or sunbed |
| `02_close.mp4`: linen shirt, martini or espresso, straight to camera | "Invent James Bond." | caption |

✓ Verify: his Jamaica routine of swimming, then about 2,000 words a morning; spearfishing at Goldeneye.

### B. Sometimes life calls for (`fleming_2_sometimes_life_calls_for`)

`01_talk.mp4`: one seated take at a desk or café table, laptop open, snorkel mask on your face.

| Say | On screen |
|---|---|
| "Sometimes life calls for a snorkel at your desk." | caption |
| "Why???" | |
| "It's Monday. Forty-seven tabs open. I'm an NPC." | |
| "How do you break free?" | |
| "Okay. Ian Fleming." | pop-up `fleming.jpg`: portrait |
| "Dropped out of military academy. Failed the Foreign Office exam." | |
| "Became a stockbroker. Called himself the worst stockbroker in the world." | |
| "Then he moved to Jamaica and built a house on the water called Goldeneye." | pop-up `goldeneye.jpg` |
| "Every morning: swim the reef, write two thousand words, nap." | |
| "Wrote Casino Royale at forty-three." | pop-up `casino_royale.jpg`: you holding a copy |
| "Look at the chart. One of the biggest film franchises of all time." | pop-up `chart.png`: a real box-office chart screenshot |
| "So what's the takeaway here?" | |
| "Swim first. Write later. Be a terrible stockbroker." | |
| "Namaste." | |

✓ Verify: left Sandhurst early; failed the Foreign Office exam; the "worst stockbroker" quote; *Casino Royale* written at Goldeneye in early 1952, when he was 43; use a real source for the chart.

### C. Please do not (`fleming_3_please_do_not`)

| File | Say | On screen |
|---|---|---|
| `01_coldopen.mp4`: collared shirt, a stock app on your phone; you stare at it, then at the sea | "Alright, let's check the markets." | label: **FAILED ATTEMPT AT BEING A STOCKBROKER** |
| `02_talk.mp4`: on the rocks after a swim, dripping | "Please do not make me check the markets." | the label disappears here |
| | "I just went for a swim in the sea." | |
| | "Ian Fleming was the worst stockbroker in London." | pop-up `fleming.jpg` |
| | "He quit, moved to Jamaica, and wrote James Bond in a beach house." | |
| | "I'm just following the process, man." | |
| | "It's a Sunday." | |

---

## Jack London

### A. Day in the life (`london_1_day_in_the_life`)

| File | Say | On screen |
|---|---|---|
| `01_hook.mp4`: selfie on a dock or harbour wall | "A day in the life if you're Jack London." | caption |
| | "Age fifteen. Borrow three hundred bucks. Buy a boat." | cutaway `boat.mp4`: a small sailboat or dinghy |
| | "Steal oysters at midnight." | cutaway `oysters.mp4`: shucking oysters at night by torchlight |
| | "Sail to Japan." | cutaway `sail.mp4`: sailing or open water |
| | "Go to the gold rush. Find no gold. Get scurvy." | cutaway `cold.mp4`: grey, cold, miserable water or a mountain |
| | "Come home broke. Write The Call of the Wild." | cutaway `write.mp4`: notebook or typewriter |
| `02_close.mp4`: board under your arm, just out of the surf | "Then learn to surf." | caption |

✓ Verify: the $300 loan at 15; sealing voyage to Japan at 17; Klondike gold rush and scurvy; *The Call of the Wild* in 1903; learned to surf at Waikiki in 1907.

### B. Sometimes life calls for (`london_2_sometimes_life_calls_for`)

`01_talk.mp4`: one seated take at the same kind of oyster bar as your 69× video, with a mountain of oysters on the table. This is the sequel.

| Say | On screen |
|---|---|
| "Sometimes life calls for 48 oysters. Again." | caption |
| "Why???" | |
| "It's raining. I doomscrolled. I'm an NPC again." | |
| "How do you break free?" | |
| "Piracy." | |
| "Okay. Jack London. Age fifteen." | pop-up `london.jpg`: young Jack London (old photos are generally public domain; check) |
| "Borrowed three hundred dollars, bought a boat called the Razzle Dazzle." | pop-up `sloop.jpg`: an old oyster sloop photo or illustration |
| "Raided oyster beds in San Francisco Bay at night." | |
| "They called him the Prince of the Oyster Pirates." | |
| "Then he wrote The Call of the Wild. One of the most famous writers in the world." | pop-up `call_of_the_wild.jpg`: the 1903 cover |
| "So what's the takeaway here?" | |
| "Eat 48 oysters. Become a pirate. Write it down later." | |
| "Namaste." | |

✓ Verify: the *Razzle Dazzle* name and the "Prince of the Oyster Pirates" nickname.

### C. Please do not (`london_3_please_do_not`)

| File | Say | On screen |
|---|---|---|
| `01_coldopen.mp4`: collared shirt and a coffee, walking toward a building | "Alright, off to the office." | label: **FAILED ATTEMPT AT GETTING A REAL JOB** |
| `02_talk.mp4`: sitting on the beach, surfboard beside you | "Please do not tell me to get a real job." | the label disappears here |
| | "Jack London was an oyster pirate, a sailor, a hobo, and a gold miner before he wrote a single book." | pop-up `london.jpg` |
| | "Then he went to Hawaii and learned to surf." | |
| | "I'm still in the research phase, man." | |
| | "It's a Wednesday." | |

---

## Captions to post with them

- **A:** "A day in the life if you're [legend] 🌊 Lifestyle Legends. Who's next? 👇"
- **B:** "Sometimes life calls for [prop]. The science is clear. Namaste 🙏 (Lifestyle Legends)"
- **C:** "Failed attempt at [X]. [Legend] would understand. (Lifestyle Legends)"

Every caption should end by pointing to the newsletter: "Full story in the newsletter, link in bio."
