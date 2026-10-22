# Lifestyle Legends: scripts

There are three legends, each with one script per format. How each format is edited is broken down in [BREAKDOWNS.md](BREAKDOWNS.md).

- **Legend 1: Jacques Cousteau.** The Riviera is his home water.
- **Legend 2: Yvon Chouinard.**
- **Legend 3: pick one of five.** The options are below. Jack London and Ian Fleming already have scripts.

The three formats:
- **A. The Origin Story**
- **B. Guess the Legend**
- **C. In Their Footsteps**

Each script has a plan in `plans/`, so once you've filmed it the editor can cut it:

```bash
python3 edit_legend.py series/lifestyle-legends/plans/<plan name>.json --draft
```

Put the footage for each script in `input/<plan name>/`, using the file names below. In the "On screen" column:

- **top** is the story panel above you.
- **full screen** covers the whole frame.
- **pill** is the blue label naming the beat.

Each panel starts on the first word of its line and stays up until the next one.

Before posting, check every fact marked ✓. They're from memory and haven't been checked against sources.

**Images.** Archive photos from before 1931 are generally public domain in the US; use Wikimedia Commons or the Library of Congress, and check each licence. For Cousteau, Fleming and Chouinard, most photos are still under copyright. Use your own footage of places and objects, film yourself holding the book, buy a licence, or use an illustrated scene (that's what Lens on Legends does). Never use a fake photoreal image of a real person.


## Legend 1: Jacques Cousteau

### A. The Origin Story: `cousteau_a_origin`

**Length:** about 95 s (284 words). **Film:** One take to camera on the rocks above the sea, slow and serious. Plus two clips of you: swimming in the Med, and an underwater POV with goggles or a mask.

**Built on:** Lens on Legends, Dua Lipa: one bold fact first, short declarative sentences, a payoff flurry, the detail nobody tells, and a callback to the hook. See [BREAKDOWNS.md](BREAKDOWNS.md).

| Say | On screen |
|---|---|
| At twenty-six, Jacques Cousteau crashed his car, broke both arms, and lost his dream of being a pilot. | top `portrait_navy.jpg` · pill **JACQUES COUSTEAU** |
| This is Lifestyle Legends: the people who lived first and figured out the work later. | you, full screen |
| He was a sickly kid, and a troublemaker. He got thrown out of school for breaking seventeen windows. | top `school.jpg` · pill **THE TROUBLEMAKER** |
| At thirteen, he saved up for a movie camera, and took it apart to see how it worked. | top `camera.jpg` · pill **AGE 13: FIRST CAMERA** |
| He joined the French Navy to fly planes. | top `naval_aviation.jpg` · pill **THE FRENCH NAVY** |
| Then the crash ended all of it. | you, full screen |
| To get his arms working again, he started swimming every day in the Mediterranean. | full screen `swim.mp4` · pill **THE REHAB** |
| One summer morning in 1936, a friend handed him a pair of swimming goggles. | top `goggles.jpg` · pill **1936: THE GOGGLES** |
| He put his face under the water, and that was it. | full screen `underwater.mp4` |
| He wrote: sometimes we are lucky enough to know that our lives have been changed. | you, full screen |
| There was one problem. You could only stay down as long as you could hold your breath. |  |
| So during the war, he and an engineer named Emile Gagnan built a way to breathe underwater. They called it the Aqua-Lung. | top `aqualung.jpg` · pill **1943: THE AQUA-LUNG** |
| Every scuba tank on earth comes from that idea. |  |
| Then he got hold of an old minesweeper, named it Calypso, and sailed it around the world with a camera. | top `calypso.jpg` · pill **CALYPSO** |
| His film The Silent World won the top prize at Cannes, and an Oscar. | top `silent_world.jpg` · pill **CANNES + OSCAR** |
| Then the TV shows, the red cap, and a whole generation who wanted to explore the ocean. | top `red_cap.jpg` · pill **THE RED CAP** |
| And the part nobody tells you: he became one of the loudest voices fighting to protect the sea he'd spent his life filming. | top `older.jpg` · pill **THE PROTECTOR** |
| He wanted the sky. He got the whole ocean instead. | you, full screen |
| Follow for the next legend: the climber who ate cat food and built Patagonia. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT: YVON CHOUINARD

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait_navy.jpg`: Young Cousteau in naval uniform (check licence) or an illustration
- `school.jpg`: 1920s French school or boarding school, old postcard
- `camera.jpg`: 1920s Pathé home movie camera
- `naval_aviation.jpg`: 1930s French naval aviation photo
- `swim.mp4`: YOU: swimming laps in the Mediterranean
- `goggles.jpg`: Vintage swimming goggles on a rock
- `underwater.mp4`: YOU: underwater POV, fish and rocks
- `aqualung.jpg`: Early Aqua-Lung regulator and tanks
- `calypso.jpg`: The ship Calypso
- `silent_world.jpg`: Poster or book cover of The Silent World
- `red_cap.jpg`: A red wool cap on a ship's rail (YOU can shoot this)
- `older.jpg`: Older Cousteau (check licence) or open ocean

</details>

✓ Check before posting: the 1936 car accident and the end of his naval-aviation training; expelled for breaking 17 windows; buying a movie camera at 13 and taking it apart; goggles from Philippe Tailliez at Le Mourillon, 1936; the 'lucky enough' quote from The Silent World; Aqua-Lung with Émile Gagnan, 1943; Calypso, a former minesweeper; The Silent World: Palme d'Or 1956, Oscar 1957; his campaigns against dumping waste in the sea.

### B. Guess the Legend: `cousteau_b_guess`

**Length:** about 50 s (121 words). **Film:** One take to camera, no pauses, leaning in like you're quizzing a friend. A red cap in your hand is the silent last clue.

**Built on:** Guess the footballer: one breathless present-tense run-on, a new image every clue, the reveal at about 90%, then 'comment when you knew'. See [BREAKDOWNS.md](BREAKDOWNS.md).

| Say | On screen |
|---|---|
| Can you imagine living this explorer's life? Comment the second you know who it is. | top `portrait.jpg` (pixelated) · pill **GUESS THE LEGEND** |
| A sickly kid who gets thrown out of school for breaking windows, | top `school.jpg` · pill **THE TROUBLEMAKER** |
| buys his first movie camera at thirteen, | top `camera.jpg` · pill **AGE 13** |
| joins the navy to become a pilot, | top `naval_aviation.jpg` · pill **THE NAVY** |
| then a car crash breaks both his arms and ends it. | top `old_car.jpg` · pill **THE CRASH** |
| He swims in the sea every day to recover, | full screen `swim.mp4` · pill **THE REHAB** |
| puts on a pair of goggles, and never looks back. | top `goggles.jpg` · pill **THE GOGGLES** |
| During the war, he helps invent a way to breathe underwater, | top `aqualung.jpg` · pill **THE INVENTION** |
| sails an old minesweeper around the world with a camera, | top `calypso.jpg` (pixelated) · pill **THE SHIP** |
| and wins an Oscar for showing everyone what's down there. | top `oscar.jpg` · pill **THE OSCAR** |
| Last clue: the red cap. | top `red_cap.jpg` · pill **LAST CLUE** |
| It's Jacques Cousteau. | top `portrait.jpg` · pill **JACQUES COUSTEAU** |
| Comment when you got it, and follow for the next one. | you, full screen |

End card from "follow": **GUESS THE LEGEND** / NEXT: A CLIMBER TURNED BILLIONAIRE

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Cousteau, face pixelated by the editor
- `school.jpg`: 1920s French school, old postcard
- `camera.jpg`: 1920s home movie camera
- `naval_aviation.jpg`: 1930s naval aviation photo
- `old_car.jpg`: 1930s car on a mountain road
- `swim.mp4`: YOU: swimming in the sea
- `goggles.jpg`: Vintage swimming goggles
- `aqualung.jpg`: Early scuba regulator
- `calypso.jpg`: The ship, name on the hull pixelated
- `oscar.jpg`: An Oscar statuette or 1950s premiere photo
- `red_cap.jpg`: YOU: holding a red wool cap

</details>

✓ Check before posting: the same facts as version A.

### C. In Their Footsteps: `cousteau_c_footsteps`

**Length:** about 75 s (131 words). **Film:** Two days on the Riviera. 01 at Le Mourillon beach in Toulon (selfie, goggles in hand), 02 outside the Oceanographic Museum in Monaco. Plus underwater POV and the drive along the coast.

**Built on:** Stevenson Trail + Hever Castle: a title over a selfie hook in the real place, B-roll every 1.5–3 s, you back on camera at the emotional beats, ending at the legend's landmark. See [BREAKDOWNS.md](BREAKDOWNS.md).

**Opening title** (until "1936"): *Following Cousteau / along the Riviera*

| Say | On screen |
|---|---|
| This little beach in Toulon is where Jacques Cousteau first put his face in the sea. |  |
| In 1936 he was a navy officer with two broken arms, swimming here every day to get them working again. | top `portrait_navy.jpg` · pill **LE MOURILLON, 1936** |
| A friend gave him a pair of goggles. He looked down, and that was it. | top `goggles.jpg` · pill **THE GOGGLES** |
| So I brought goggles. | you, full screen |
| This is what he saw. | full screen `underwater.mp4` |
| Seven years later, he and an engineer invented the Aqua-Lung, and took it into this same sea. | top `aqualung.jpg` · pill **1943: THE AQUA-LUNG** |
| Then I followed the coast to Monaco. | full screen `coast_drive.mp4` |
| Cousteau ran the Oceanographic Museum here for more than thirty years. | top `museum.mp4` · pill **OCEANOGRAPHIC MUSEUM, MONACO** |
| The man who wanted to fly ended up with the whole ocean. | you, full screen |
| Honestly, I get it. Put your face in the water for five minutes and tell me you don't. |  |
| Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT: CHOUINARD'S SURF RULE

<details><summary>Footage and images to gather</summary>

- `01_mourillon.mp4`: you talking to camera
- `02_monaco.mp4`: you talking to camera
- `portrait_navy.jpg`: Young Cousteau in naval uniform (check licence) or an illustration
- `goggles.jpg`: Vintage goggles on these rocks
- `underwater.mp4`: YOU: underwater POV off Le Mourillon
- `aqualung.jpg`: Early Aqua-Lung regulator and tanks
- `coast_drive.mp4`: YOU: driving or on the train along the coast
- `museum.mp4`: YOU: walking up to the museum

</details>

✓ Check before posting: Le Mourillon, Toulon as the 1936 goggles beach; the Aqua-Lung's first sea dives off the Provence coast; director of the Oceanographic Museum of Monaco, 1957–1988.

---

## Legend 2: Yvon Chouinard

### A. The Origin Story: `chouinard_a_origin`

**Length:** about 90 s (196 words). **Film:** One take to camera at a crag or a surf break. Plus clips of you: a car boot full of gear, and surfing.

**Built on:** Lens on Legends, Dua Lipa + Let's Talk About It: a two-sentence hook from tiny to huge, the series line, short sentences, the detail nobody tells, a callback. See [BREAKDOWNS.md](BREAKDOWNS.md).

| Say | On screen |
|---|---|
| At eighteen, Yvon Chouinard bought a used forge from a junkyard. Sixty-five years later, he gave away a three-billion-dollar company. | top `forge.jpg` · pill **1957** |
| This is Lifestyle Legends: the people who lived first and figured out the work later. | you, full screen |
| He was the French kid in a California school who barely spoke English. | top `young.jpg` · pill **THE OUTSIDER** |
| He found falconry. Falconry led him to climbing. Climbing led him to Yosemite. | top `yosemite.jpg` · pill **YOSEMITE** |
| He couldn't afford gear. So he taught himself to blacksmith, and made his own. | top `pitons.jpg` · pill **HOMEMADE PITONS** |
| He sold it from the back of his car. A dollar fifty each. | top `car_boot.mp4` · pill **$1.50 EACH** |
| He lived on about a dollar a day. Sometimes that meant cat food. | top `cat_food.jpg` · pill **THE DIET** |
| By 1970, he was the biggest climbing gear supplier in America. | you, full screen |
| Then he saw his gear was scarring the rock he loved. So he stopped selling it. | top `scarred_rock.jpg` · pill **SCARRING THE ROCK** |
| He started selling clothes instead. He called the company Patagonia. | top `patagonia.jpg` · pill **1973: PATAGONIA** |
| The rule at work? When the surf's up, go surfing. | full screen `surf.mp4` · pill **COMPANY POLICY** |
| In 2022, he gave the whole company away to fight climate change. Earth is now the only shareholder. | top `headline.png` · pill **2022** |
| The part nobody tells you: he always said he hated being called a businessman. | you, full screen |
| The kid with the junkyard forge just wanted to keep climbing. |  |
| Follow for the next legend. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `forge.jpg`: An old coal forge and anvil
- `young.jpg`: Photo of young Chouinard (licensed) or a 1940s California schoolyard
- `yosemite.jpg`: El Capitan or Camp 4, old photo
- `pitons.jpg`: Old steel pitons
- `car_boot.mp4`: YOU: opening a car boot full of climbing gear
- `cat_food.jpg`: A dented tin of cat food
- `scarred_rock.jpg`: Close-up of a scarred granite crack
- `patagonia.jpg`: Patagonia shopfront or logo
- `surf.mp4`: YOU: surfing
- `headline.png`: Screenshot of the news headline

</details>

✓ Check before posting: 1957 used forge from a junkyard (he was 18); spoke only French at school in California; falconry led to climbing; pitons at $1.50, living on about $1 a day; the cat food story; biggest US climbing hardware supplier by 1970; phasing out pitons (1972 'clean climbing'); Patagonia 1973; 2022 transfer, ~$3B, 'Earth is now our only shareholder'; his line about hating to admit being a businessman (Let My People Go Surfing).

### B. Guess the Legend: `chouinard_b_guess`

**Length:** about 50 s (123 words). **Film:** One take to camera in a fleece, outdoors, no pauses.

**Built on:** Guess the footballer: one breathless present-tense run-on, a new image every clue, the reveal at about 90%, then 'comment when you knew'. See [BREAKDOWNS.md](BREAKDOWNS.md).

| Say | On screen |
|---|---|
| Can you imagine living this climber's life? Comment the second you know who it is. | top `portrait.jpg` (pixelated) · pill **GUESS THE LEGEND** |
| A French-speaking outsider in a California school, | top `1940s_california.jpg` · pill **THE OUTSIDER** |
| gets into falconry, which gets him into climbing, | top `falcon.jpg` · pill **FALCONRY** |
| teaches himself blacksmithing to make his own gear, | top `forge.jpg` · pill **SELF-TAUGHT BLACKSMITH** |
| sells it from the back of his car, lives on a dollar a day, eats cat food, | top `cat_food.jpg` · pill **THE DIET** |
| builds the biggest climbing gear company in America, then quits his best seller because it's damaging the rock, | top `scarred_rock.jpg` · pill **QUITS HIS BEST SELLER** |
| brings home a rugby shirt from Scotland and starts selling clothes, | top `rugby_shirt.jpg` · pill **THE RUGBY SHIRT** |
| writes a book called Let My People Go Surfing, | top `book.jpg` (pixelated) · pill **THE BOOK** |
| and in 2022 gives the entire company away to fight climate change. | top `headline.png` (pixelated) · pill **LAST CLUE** |
| It's Yvon Chouinard. The founder of Patagonia. | top `portrait.jpg` · pill **YVON CHOUINARD** |
| Comment when you got it, and follow for the next one. | you, full screen |

End card from "follow": **GUESS THE LEGEND** / NEXT: ANOTHER LEGEND

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Chouinard, face pixelated
- `1940s_california.jpg`: 1940s Southern California street
- `falcon.jpg`: A falcon on a glove
- `forge.jpg`: An old coal forge and anvil
- `cat_food.jpg`: A dented tin of cat food
- `scarred_rock.jpg`: Scarred granite crack
- `rugby_shirt.jpg`: A striped 1970s rugby shirt
- `book.jpg`: YOU: holding the book, company name covered
- `headline.png`: News headline, company name pixelated

</details>

✓ Check before posting: the 1970 rugby shirt from Scotland that started the clothing line.

### C. In Their Footsteps: `chouinard_c_footsteps`

**Length:** about 70 s (118 words). **Film:** A 'surf's up' workday: talk takes at dawn and in the afternoon, B-roll of the surf, laptop work while still wet, and a climb.

**Built on:** Harry DuBois + Stevenson Trail: a stacked-accomplishments hook under a big title, you living it in fast B-roll, back on camera for what you learned. See [BREAKDOWNS.md](BREAKDOWNS.md).

**Opening title** (until "name"): *Living by Patagonia's / one rule for a day*

| Say | On screen |
|---|---|
| He forged his own climbing gear, ate cat food to stay in Yosemite, and built a three-billion-dollar company around one rule. Today I'm following it. |  |
| His name is Yvon Chouinard, and the rule is the title of his book: Let My People Go Surfing. | top `portrait.jpg` · pill **YVON CHOUINARD**<br>top `book.jpg` · pill **THE RULE** |
| When the surf's up, you go surfing. You fit the work around it. | full screen `surf_dawn.mp4` · pill **DAWN PATROL** |
| So: surf first. | you, full screen |
| Then the laptop, still salty. | top `laptop.mp4` · pill **THEN WORK** |
| Then a climb in the afternoon. | full screen `climb.mp4` |
| Here's what surprised me: I got more done in four hours than on a normal day. | you, full screen |
| Chouinard's trick is flexibility. Chase the good conditions, and fit the work around them. | top `portrait.jpg` · pill **THE TRICK** |
| He built a company that way, then gave it all away. | top `headline.png` · pill **2022: GIVES IT AWAY** |
| Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND

<details><summary>Footage and images to gather</summary>

- `01_dawn.mp4`: you talking to camera
- `02_afternoon.mp4`: you talking to camera
- `portrait.jpg`: Photo of Chouinard (licensed) or an illustration
- `book.jpg`: YOU: holding the book
- `surf_dawn.mp4`: YOU: dawn surf session
- `laptop.mp4`: YOU: working on a laptop in a towel
- `climb.mp4`: YOU: bouldering or a scramble
- `headline.png`: Screenshot of the news headline

</details>

✓ Check before posting: Patagonia's flextime ('let my people go surfing') policy; only say the 'four hours' line if it's true for you.

---

## Legend 3: pick one of five

| | Legend | Why they fit | Data signal | Status |
|---|---|---|---|---|
| 1 | **Robert Louis Stevenson** | Sickly kid from a family of lighthouse engineers. Trained as a lawyer and never really practised. In 1878 he walked the Cévennes with a donkey, then wrote *Treasure Island* and *Jekyll and Hyde*, sailed the Pacific, and ended his life in Samoa. | The Stevenson Trail walk (@heleneinbetween) is **65× with 11% engagement**, the strongest In Their Footsteps result in the data. The route is in France, a day's drive from the Riviera. | Not scripted yet |
| 2 | **Jack London** | Oyster pirate at 15, sailor, hobo and gold-rusher, then a bestselling author who learned to surf at Waikiki. | A *Call of the Wild* film-clip reel did **53.7M views (15×)**, so the story pulls on its own. The oysters and surfing tie straight into your world. | **3 scripts ready** (below) |
| 3 | **Ian Fleming** | Failed at everything his family wanted, then wrote James Bond at 43 after a morning swim in Jamaica. | Bond is the biggest name recognition of the five. I found no direct Fleming reel in the data to compare. | **3 scripts ready** (below) |
| 4 | **Ernest Hemingway** | Ambulance driver wounded at 18, Paris in the 1920s, then marlin fishing in Key West and Cuba. *The Old Man and the Sea* won him the Nobel. | A Hemingway film clip did **13M views (13×)**. One caveat: he was writing from 17, so his story is "lived it, then wrote it", not "work came later". | Not scripted yet |
| 5 | **Anthony Bourdain** | Line cook into his 40s. *Kitchen Confidential* came out when he was 44. His first raw oyster, as a boy in France, changed his life, which suits your oyster audience. | A Bourdain tribute reel did **3.2M views (9×)**. His death needs care: never make it the twist. | Not scripted yet |

**My pick: Robert Louis Stevenson.** He has the best proven format in the data and a trail you can actually walk, which is a ready-made In Their Footsteps episode. If you want to film this week, **Jack London** is the runner-up, and his scripts are ready below.


### Ready to film: Jack London

#### A. The Origin Story: `london_a_origin`

**Length:** about 80 s (227 words). **Film:** One take to camera on a dock or harbour wall, golden hour. Then a surf clip of you for the Hawaii beat.

| Say | On screen |
|---|---|
| At fifteen, Jack London borrowed three hundred dollars and became a pirate. | top `portrait.jpg` · pill **JACK LONDON** |
| This is Lifestyle Legends: the people who lived first and figured out the work later. | you, full screen |
| Jack grew up broke in Oakland, working ten-hour shifts in a cannery for ten cents an hour. | top `cannery.jpg` · pill **AGE 14: CANNERY WORKER** |
| So he borrowed three hundred dollars from the woman who'd nursed him as a baby, bought a little sloop called the Razzle Dazzle, and started raiding oyster beds in San Francisco Bay at night. | top `sloop.jpg` · pill **THE RAZZLE DAZZLE**<br>top `oysters_night.mp4` · pill **OYSTER PIRATE** |
| The waterfront called him the Prince of the Oyster Pirates. |  |
| At seventeen he sailed to Japan on a sealing ship. | top `sealing_ship.jpg` · pill **1893: SEALING SHIP TO JAPAN** |
| At eighteen he was riding freight trains across America, and got thrown in jail for vagrancy. | top `freight_train.jpg` · pill **AGE 18: HOBO** |
| At twenty-one he went north for the Klondike gold rush. | top `klondike.jpg` · pill **1897: KLONDIKE GOLD RUSH** |
| He found no gold. He came home with scurvy, no money, and a head full of stories. | you, full screen |
| So he made himself write a thousand words a day, and editors kept sending them back. | top `notebook.mp4` · pill **1,000 WORDS A DAY** |
| Then The Call of the Wild came out, and he became one of the most famous writers in the world. | top `call_of_the_wild.jpg` · pill **1903: THE CALL OF THE WILD** |
| And the part nobody tells you? Already famous, he sailed to Hawaii and learned to surf at Waikiki. | top `waikiki_1907.jpg` · pill **1907: LEARNS TO SURF**<br>full screen `surf.mp4` |
| He wrote one of the first articles that made the world care about surfing. |  |
| He didn't plan a career. He lived first, and wrote it down later. | you, full screen |
| Follow for the next legend. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of young Jack London (public domain, Wikimedia Commons)
- `cannery.jpg`: 1890s cannery workers (Library of Congress)
- `sloop.jpg`: Old oyster sloop on San Francisco Bay
- `oysters_night.mp4`: YOU: shucking oysters on a dock at night by torchlight
- `sealing_ship.jpg`: 1890s sealing schooner
- `freight_train.jpg`: Hobos on a freight train, 1890s
- `klondike.jpg`: Chilkoot Pass, 1898 (public domain)
- `notebook.mp4`: YOU: writing in a notebook, close on the pen
- `call_of_the_wild.jpg`: 1903 first-edition cover (public domain)
- `waikiki_1907.jpg`: Waikiki surfers, early 1900s (public domain)
- `surf.mp4`: YOU: paddling out and catching a wave

</details>

✓ Check before posting: the $300 loan from Virginia Prentiss at 15 and the Razzle Dazzle; cannery wages (10 cents an hour, 10+ hour shifts); sealing voyage at 17 (1893); 30 days for vagrancy at 18 (1894); Klondike 1897 and scurvy; 1,000 words a day; Waikiki 1907 and his surfing article 'A Royal Sport'.

#### B. Guess the Legend: `london_b_guess`

**Length:** about 50 s (121 words). **Film:** One take to camera, anywhere with character (a dock, a bar, a beach). Lean in like you're quizzing a friend.

| Say | On screen |
|---|---|
| Can you guess this legend from the story of his life? Comment the second you know. | top `portrait.jpg` (pixelated) · pill **GUESS THE LEGEND** |
| Age fourteen: working in a cannery for ten cents an hour. | top `cannery.jpg` · pill **AGE 14** |
| Age fifteen: buys a boat with borrowed money and steals oysters at night. | top `sloop.jpg` · pill **AGE 15** |
| Then switches sides and joins the fish patrol, catching the pirates he used to sail with. | top `fish_patrol.jpg` · pill **SWITCHES SIDES** |
| Age seventeen: sails to Japan on a sealing ship. | top `sealing_ship.jpg` · pill **AGE 17** |
| Age eighteen: thirty days in jail for vagrancy. | top `jail.jpg` · pill **AGE 18** |
| Age twenty-one: the Klondike. No gold. Scurvy. | top `klondike.jpg` · pill **AGE 21** |
| Age twenty-seven: writes a book about a dog that sells millions. | top `sled_dog.jpg` · pill **AGE 27** |
| Age thirty-one: learns to surf in Hawaii. | top `waikiki_1907.jpg` · pill **AGE 31** |
| Still nothing? You probably read his book in school. | top `call_of_the_wild.jpg` (pixelated) · pill **LAST CLUE** |
| It's Jack London. | top `portrait.jpg` · pill **JACK LONDON** |
| Comment when you got it, and follow for the next one. | you, full screen |

End card from "follow": **GUESS THE LEGEND** / NEXT: ANOTHER LEGEND

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Jack London, face pixelated by the editor
- `cannery.jpg`: 1890s cannery workers
- `sloop.jpg`: Old oyster sloop
- `fish_patrol.jpg`: California Fish Patrol boat or 1890s patrol photo
- `sealing_ship.jpg`: 1890s sealing schooner
- `jail.jpg`: 1890s jail or penitentiary photo
- `klondike.jpg`: Chilkoot Pass, 1898
- `sled_dog.jpg`: Historic sled-dog photo
- `waikiki_1907.jpg`: Waikiki surfers, early 1900s
- `call_of_the_wild.jpg`: 1903 cover with the title pixelated

</details>

✓ Check before posting: ages for each beat (born January 1876); California Fish Patrol after the oyster piracy.

#### C. In Their Footsteps: `london_c_footsteps`

**Length:** about 75 s (156 words). **Film:** Two talk takes: 01 on a dock at night with oysters, 02 next morning on the beach with a board. Plus b-roll of you on a boat, writing, and surfing.

| Say | On screen |
|---|---|
| I'm shucking oysters on a dock at midnight because of a writer who used to steal them. |  |
| In 1891, a fifteen-year-old named Jack London raided oyster beds like these in San Francisco Bay. | top `portrait.jpg` · pill **JACK LONDON** |
| He did it in a sloop called the Razzle Dazzle, bought with three hundred borrowed dollars. | top `sloop.jpg` · pill **THE RAZZLE DAZZLE** |
| Then he went to sea, rode the rails, chased gold in the Klondike, and came home broke. | full screen `boat.mp4` |
| Everything he lived, he wrote down. A thousand words a day. | top `notebook.mp4` · pill **1,000 WORDS A DAY** |
| So that's the plan for this trip: live it first, write it down after. | you, full screen |
| And the next morning, I'm doing what he did once he was already famous. |  |
| In 1907 he sailed to Hawaii and learned to surf at Waikiki. | top `waikiki_1907.jpg` · pill **WAIKIKI, 1907** |
| He got so sunburned he was stuck in bed, and went straight back out. | full screen `surf.mp4` |
| Here's what I think he figured out. The adventure wasn't a break from the work. It was the work. | you, full screen |
| Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND

<details><summary>Footage and images to gather</summary>

- `01_dock_night.mp4`: you talking to camera
- `02_beach_morning.mp4`: you talking to camera
- `portrait.jpg`: Portrait of young Jack London
- `sloop.jpg`: Old oyster sloop
- `boat.mp4`: YOU: on a boat or sailing, wide shot
- `notebook.mp4`: YOU: writing in a notebook on the dock
- `waikiki_1907.jpg`: Waikiki surfers, early 1900s
- `surf.mp4`: YOU: catching a wave

</details>

✓ Check before posting: 1891 oyster piracy at 15; the sunburn after his first surf sessions in 1907.

---

### Ready to film: Ian Fleming

#### A. The Origin Story: `fleming_a_origin`

**Length:** about 85 s (216 words). **Film:** One take to camera by the sea, linen shirt. Plus a snorkel clip of you for the routine beat.

| Say | On screen |
|---|---|
| Ian Fleming. The man who invented James Bond. By forty, he'd failed at almost everything. | top `portrait.jpg` · pill **IAN FLEMING** |
| This is Lifestyle Legends: the people who lived first and figured out the work later. | you, full screen |
| His big brother was the famous one, a best-selling travel writer. Ian was the problem child. | top `family.jpg` · pill **THE FAMOUS BROTHER** |
| He left military academy early. He failed the Foreign Office exam. | top `sandhurst.jpg` · pill **STRIKE ONE, STRIKE TWO** |
| He became a stockbroker, and later called himself the worst stockbroker in the world. | top `stock_exchange.jpg` · pill **THE WORST STOCKBROKER** |
| Then the war came. He became the right-hand man to the head of British naval intelligence, planning operations straight out of a spy novel. | top `admiralty.jpg` · pill **NAVAL INTELLIGENCE** |
| In 1944 he visited Jamaica, and told a friend he'd live there one day. | top `jamaica_map.jpg` · pill **JAMAICA, 1944** |
| Two years later he built a house on the water and called it Goldeneye. | top `goldeneye.jpg` · pill **GOLDENEYE** |
| He even got his newspaper to give him two months off every winter to go there. | you, full screen |
| Every morning: swim the reef, then write about two thousand words. | full screen `snorkel.mp4` · pill **THE ROUTINE** |
| At forty-three, he sat down at Goldeneye and wrote Casino Royale. | top `casino_royale.jpg` · pill **1952: CASINO ROYALE** |
| He named his spy after the author of a bird book on his shelf, because he wanted the dullest name he could find. | top `birds_book.jpg` · pill **BIRDS OF THE WEST INDIES** |
| Fourteen Bond books. Every one written in the Jamaican winter. | top `bond_books.jpg` · pill **14 BOND BOOKS** |
| He failed at the careers everyone wanted for him, then built one around the life he wanted. | you, full screen |
| Follow for the next legend. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Ian Fleming (check licence) or an illustrated portrait
- `family.jpg`: 1920s English country house or family photo
- `sandhurst.jpg`: Royal Military College, Sandhurst (old postcard)
- `stock_exchange.jpg`: 1930s London Stock Exchange
- `admiralty.jpg`: The Admiralty building, London, 1940s
- `jamaica_map.jpg`: Old map of Jamaica
- `goldeneye.jpg`: Goldeneye house or the cove at Oracabessa
- `snorkel.mp4`: YOU: snorkelling over a reef
- `casino_royale.jpg`: YOU holding a copy of Casino Royale
- `birds_book.jpg`: The bird book by ornithologist James Bond
- `bond_books.jpg`: YOU: a stack of the paperbacks

</details>

✓ Check before posting: left Sandhurst early; failed the Foreign Office exam; the 'worst stockbroker' self-description; assistant to Admiral Godfrey, Director of Naval Intelligence; 1944 Jamaica visit; Goldeneye built 1946; Sunday Times contract with two months off each winter; Casino Royale written early 1952, age 43; named after ornithologist James Bond, 'the dullest name'; 14 Bond books written at Goldeneye.

#### B. Guess the Legend: `fleming_b_guess`

**Length:** about 50 s (123 words). **Film:** One take to camera. A martini on the table is a nice silent clue.

| Say | On screen |
|---|---|
| Can you guess this legend from the story of his life? Comment the second you know. | top `portrait.jpg` (pixelated) · pill **GUESS THE LEGEND** |
| Rich family. Famous older brother. He's the disappointment. | top `family.jpg` · pill **THE DISAPPOINTMENT** |
| Leaves military academy early. Strike one. | top `sandhurst.jpg` · pill **STRIKE ONE** |
| Fails the Foreign Office exam. Strike two. | top `foreign_office.jpg` · pill **STRIKE TWO** |
| Becomes a stockbroker, and says he's the worst one in the world. Strike three. | top `stock_exchange.jpg` · pill **STRIKE THREE** |
| Then the war: he's planning secret operations for naval intelligence. | top `admiralty.jpg` · pill **WORLD WAR II** |
| After the war, he builds a house above a reef in Jamaica. | top `goldeneye.jpg` · pill **THE HIDEOUT** |
| He swims every morning, and writes every morning. | full screen `snorkel.mp4` |
| At forty-three, he writes his first novel in about two months. | top `typewriter.jpg` · pill **FIRST NOVEL** |
| Last clue: his main character likes his martini shaken, not stirred. | top `martini.jpg` · pill **LAST CLUE** |
| It's Ian Fleming. The man who invented James Bond. | top `portrait.jpg` · pill **IAN FLEMING** |
| Comment when you got it, and follow for the next one. | you, full screen |

End card from "follow": **GUESS THE LEGEND** / NEXT: ANOTHER LEGEND

<details><summary>Footage and images to gather</summary>

- `01_talk.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Ian Fleming, face pixelated
- `family.jpg`: 1920s English country house
- `sandhurst.jpg`: Sandhurst, old postcard
- `foreign_office.jpg`: The Foreign Office, London
- `stock_exchange.jpg`: 1930s London Stock Exchange
- `admiralty.jpg`: The Admiralty, 1940s
- `goldeneye.jpg`: The cove at Oracabessa, Jamaica
- `snorkel.mp4`: YOU: snorkelling over a reef
- `typewriter.jpg`: Old typewriter on a terrace
- `martini.jpg`: YOU: a martini on the bar

</details>

✓ Check before posting: Casino Royale written in about two months (Jan–Mar 1952).

#### C. In Their Footsteps: `fleming_c_footsteps`

**Length:** about 70 s (127 words). **Film:** A full 'Fleming day' somewhere with a reef: talk takes in the morning and evening, b-roll of the swim, writing on a terrace, lunch and a nap.

| Say | On screen |
|---|---|
| I'm about to live one day exactly like the man who wrote James Bond. |  |
| His name was Ian Fleming, and he wrote Casino Royale at a house on the water in Jamaica called Goldeneye. | top `portrait.jpg` · pill **IAN FLEMING**<br>top `goldeneye.jpg` · pill **GOLDENEYE, JAMAICA** |
| His routine was simple. Wake up, swim the reef. | full screen `snorkel.mp4` · pill **STEP 1: SWIM** |
| Then he'd sit down and write about two thousand words before lunch. | top `writing.mp4` · pill **STEP 2: 2,000 WORDS** |
| Lunch. A long nap. A little more work in the evening. | full screen `lunch_nap.mp4` · pill **STEP 3: LUNCH, NAP** |
| That's it. That's the schedule that built fourteen Bond books. | top `bond_books.jpg` · pill **14 BOOKS** |
| So, I did it. Here's my two thousand words, written with salt still in my hair. | top `my_pages.mp4` · pill **MY 2,000 WORDS** |
| Honest review: the swim makes the writing easier. Your brain shows up already awake. | you, full screen |
| Fleming didn't separate the life from the work. The sea is all over those books. |  |
| Follow for the next legend's footsteps. |  |

End card from "Follow": **LIFESTYLE LEGENDS** / NEXT WEEK: A NEW LEGEND

<details><summary>Footage and images to gather</summary>

- `01_morning.mp4`: you talking to camera
- `02_evening.mp4`: you talking to camera
- `portrait.jpg`: Portrait of Ian Fleming (check licence)
- `goldeneye.jpg`: The cove at Oracabessa
- `snorkel.mp4`: YOU: snorkelling over a reef
- `writing.mp4`: YOU: writing on a terrace, sea behind
- `lunch_nap.mp4`: YOU: lunch with a view, then a hammock
- `bond_books.jpg`: YOU: a stack of the paperbacks
- `my_pages.mp4`: YOU: flipping through your written pages

</details>

✓ Check before posting: his routine (morning swim, about 2,000 words, nap, evening revision) from his essay 'How to Write a Thriller'; only say the 'honest review' line if it's true for you.
