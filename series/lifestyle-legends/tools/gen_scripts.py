"""Generate series/lifestyle-legends/SCRIPTS.md and plans/*.json from one source.

Run from anywhere: python3 series/lifestyle-legends/tools/gen_scripts.py

Every panel anchor is checked against the script text with the editor's own
word matcher, so the plans line up with what's said.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
from edit_legend import find_word  # noqa: E402

SERIES = "Lifestyle Legends"
SERIES_LINE = ("This is Lifestyle Legends: the people who lived first "
               "and figured out the work later.")
CENSOR = [0.25, 0.05, 0.5, 0.5]

# panel helpers: (anchor, kind, file, label, desc, extra)
def top(at, file, label, desc, **extra):
    return {"at": at, "file": file, "label": label, "desc": desc, **extra}


def full(at, file="talk", label=None, desc=None, **extra):
    d = {"at": at, "full": file, "desc": desc, **extra}
    if label:
        d["label"] = label
    return d


SCRIPTS = [
# ---------------------------------------------------------------- JACK LONDON
dict(id="london_a_origin", legend="Jack London", version="A", ep="Ep 01",
     fmt="The Origin Story", length="about 80 s",
     film="One take to camera on a dock or harbour wall, golden hour. Then a surf clip of you for the Hawaii beat.",
     talk=["01_talk.mp4"],
     highlight=["pirate", "pirates", "scurvy", "surf", "Klondike"],
     lines=[
        ("At fifteen, Jack London borrowed three hundred dollars and became a pirate.",
         [top("Jack", "portrait.jpg", "Jack London", "Portrait of young Jack London (public domain, Wikimedia Commons)")]),
        (SERIES_LINE, [full("This")]),
        ("Jack grew up broke in Oakland, working ten-hour shifts in a cannery for ten cents an hour.",
         [top("Oakland", "cannery.jpg", "Age 14: cannery worker", "1890s cannery workers (Library of Congress)")]),
        ("So he borrowed three hundred dollars from the woman who'd nursed him as a baby, bought a little sloop called the Razzle Dazzle, and started raiding oyster beds in San Francisco Bay at night.",
         [top("sloop", "sloop.jpg", "The Razzle Dazzle", "Old oyster sloop on San Francisco Bay"),
          top("raiding", "oysters_night.mp4", "Oyster pirate", "YOU: shucking oysters on a dock at night by torchlight")]),
        ("The waterfront called him the Prince of the Oyster Pirates.", []),
        ("At seventeen he sailed to Japan on a sealing ship.",
         [top("Japan", "sealing_ship.jpg", "1893: sealing ship to Japan", "1890s sealing schooner")]),
        ("At eighteen he was riding freight trains across America, and got thrown in jail for vagrancy.",
         [top("freight", "freight_train.jpg", "Age 18: hobo", "Hobos on a freight train, 1890s")]),
        ("At twenty-one he went north for the Klondike gold rush.",
         [top("Klondike", "klondike.jpg", "1897: Klondike gold rush", "Chilkoot Pass, 1898 (public domain)")]),
        ("He found no gold. He came home with scurvy, no money, and a head full of stories.",
         [full("found")]),
        ("So he made himself write a thousand words a day, and editors kept sending them back.",
         [top("himself", "notebook.mp4", "1,000 words a day", "YOU: writing in a notebook, close on the pen")]),
        ("Then The Call of the Wild came out, and he became one of the most famous writers in the world.",
         [top("Call", "call_of_the_wild.jpg", "1903: The Call of the Wild", "1903 first-edition cover (public domain)")]),
        ("And the part nobody tells you? Already famous, he sailed to Hawaii and learned to surf at Waikiki.",
         [top("Hawaii", "waikiki_1907.jpg", "1907: learns to surf", "Waikiki surfers, early 1900s (public domain)"),
          full("surf", "surf.mp4", desc="YOU: paddling out and catching a wave")]),
        ("He wrote one of the first articles that made the world care about surfing.", []),
        ("He didn't plan a career. He lived first, and wrote it down later.", [full("plan")]),
        ("Follow for the next legend: the worst stockbroker in London, who invented James Bond.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Ian Fleming"),
     verify=["the $300 loan from Virginia Prentiss at 15 and the Razzle Dazzle",
             "cannery wages (10 cents an hour, 10+ hour shifts)", "sealing voyage at 17 (1893)",
             "30 days for vagrancy at 18 (1894)", "Klondike 1897 and scurvy",
             "1,000 words a day", "Waikiki 1907 and his surfing article 'A Royal Sport'"]),

dict(id="london_b_guess", legend="Jack London", version="B", ep="Guess who #1",
     fmt="Guess the Legend", length="about 50 s",
     film="One take to camera, anywhere with character (a dock, a bar, a beach). Lean in like you're quizzing a friend.",
     talk=["01_talk.mp4"],
     highlight=["guess", "jail", "scurvy"],
     lines=[
        ("Can you guess this legend from the story of his life? Comment the second you know.",
         [top("guess", "portrait.jpg", "Guess the legend", "Portrait of Jack London, face pixelated by the editor", censor=CENSOR)]),
        ("Age fourteen: working in a cannery for ten cents an hour.",
         [top("cannery", "cannery.jpg", "Age 14", "1890s cannery workers")]),
        ("Age fifteen: buys a boat with borrowed money and steals oysters at night.",
         [top("boat", "sloop.jpg", "Age 15", "Old oyster sloop")]),
        ("Then switches sides and joins the fish patrol, catching the pirates he used to sail with.",
         [top("switches", "fish_patrol.jpg", "Switches sides", "California Fish Patrol boat or 1890s patrol photo")]),
        ("Age seventeen: sails to Japan on a sealing ship.",
         [top("Japan", "sealing_ship.jpg", "Age 17", "1890s sealing schooner")]),
        ("Age eighteen: thirty days in jail for vagrancy.",
         [top("jail", "jail.jpg", "Age 18", "1890s jail or penitentiary photo")]),
        ("Age twenty-one: the Klondike. No gold. Scurvy.",
         [top("Klondike", "klondike.jpg", "Age 21", "Chilkoot Pass, 1898")]),
        ("Age twenty-seven: writes a book about a dog that sells millions.",
         [top("dog", "sled_dog.jpg", "Age 27", "Historic sled-dog photo")]),
        ("Age thirty-one: learns to surf in Hawaii.",
         [top("surf", "waikiki_1907.jpg", "Age 31", "Waikiki surfers, early 1900s")]),
        ("Still nothing? You probably read his book in school.",
         [top("Still", "call_of_the_wild.jpg", "Last clue", "1903 cover with the title pixelated", censor=[0.1, 0.05, 0.8, 0.35])]),
        ("It's Jack London.",
         [top("Jack", "portrait.jpg", "Jack London", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: a spy novelist"),
     verify=["ages for each beat (born January 1876)", "California Fish Patrol after the oyster piracy"]),

dict(id="london_c_footsteps", legend="Jack London", version="C", ep="Ep 01 · In his footsteps",
     fmt="In Their Footsteps", length="about 75 s",
     film="Two talk takes: 01 on a dock at night with oysters, 02 next morning on the beach with a board. Plus b-roll of you on a boat, writing, and surfing.",
     talk=["01_dock_night.mp4", "02_beach_morning.mp4"],
     highlight=["oysters", "surf", "work"],
     lines=[
        ("I'm shucking oysters on a dock at midnight because of a writer who used to steal them.", []),
        ("In 1891, a fifteen-year-old named Jack London raided oyster beds like these in San Francisco Bay.",
         [top("Jack", "portrait.jpg", "Jack London", "Portrait of young Jack London")]),
        ("He did it in a sloop called the Razzle Dazzle, bought with three hundred borrowed dollars.",
         [top("sloop", "sloop.jpg", "The Razzle Dazzle", "Old oyster sloop")]),
        ("Then he went to sea, rode the rails, chased gold in the Klondike, and came home broke.",
         [full("sea", "boat.mp4", desc="YOU: on a boat or sailing, wide shot")]),
        ("Everything he lived, he wrote down. A thousand words a day.",
         [top("Everything", "notebook.mp4", "1,000 words a day", "YOU: writing in a notebook on the dock")]),
        ("So that's the plan for this trip: live it first, write it down after.", [full("plan")]),
        ("And the next morning, I'm doing what he did once he was already famous.", []),
        ("In 1907 he sailed to Hawaii and learned to surf at Waikiki.",
         [top("Hawaii", "waikiki_1907.jpg", "Waikiki, 1907", "Waikiki surfers, early 1900s")]),
        ("He got so sunburned he was stuck in bed, and went straight back out.",
         [full("sunburned", "surf.mp4", desc="YOU: catching a wave")]),
        ("Here's what I think he figured out. The adventure wasn't a break from the work. It was the work.",
         [full("Here's")]),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Ian Fleming's Jamaica"),
     verify=["1891 oyster piracy at 15", "the sunburn after his first surf sessions in 1907"]),

# --------------------------------------------------------------- IAN FLEMING
dict(id="fleming_a_origin", legend="Ian Fleming", version="A", ep="Ep 02",
     fmt="The Origin Story", length="about 85 s",
     film="One take to camera by the sea, linen shirt. Plus a snorkel clip of you for the routine beat.",
     talk=["01_talk.mp4"],
     highlight=["failed", "stockbroker", "Goldeneye", "Bond"],
     lines=[
        ("Ian Fleming. The man who invented James Bond. By forty, he'd failed at almost everything.",
         [top("Ian", "portrait.jpg", "Ian Fleming", "Portrait of Ian Fleming (check licence) or an illustrated portrait")]),
        (SERIES_LINE, [full("This")]),
        ("His big brother was the famous one, a best-selling travel writer. Ian was the problem child.",
         [top("brother", "family.jpg", "The famous brother", "1920s English country house or family photo")]),
        ("He left military academy early. He failed the Foreign Office exam.",
         [top("military", "sandhurst.jpg", "Strike one, strike two", "Royal Military College, Sandhurst (old postcard)")]),
        ("He became a stockbroker, and later called himself the worst stockbroker in the world.",
         [top("stockbroker", "stock_exchange.jpg", "The worst stockbroker", "1930s London Stock Exchange")]),
        ("Then the war came. He became the right-hand man to the head of British naval intelligence, planning operations straight out of a spy novel.",
         [top("war", "admiralty.jpg", "Naval intelligence", "The Admiralty building, London, 1940s")]),
        ("In 1944 he visited Jamaica, and told a friend he'd live there one day.",
         [top("visited", "jamaica_map.jpg", "Jamaica, 1944", "Old map of Jamaica")]),
        ("Two years later he built a house on the water and called it Goldeneye.",
         [top("Goldeneye", "goldeneye.jpg", "Goldeneye", "Goldeneye house or the cove at Oracabessa")]),
        ("He even got his newspaper to give him two months off every winter to go there.", [full("newspaper")]),
        ("Every morning: swim the reef, then write about two thousand words.",
         [full("swim", "snorkel.mp4", "The routine", "YOU: snorkelling over a reef")]),
        ("At forty-three, he sat down at Goldeneye and wrote Casino Royale.",
         [top("Casino", "casino_royale.jpg", "1952: Casino Royale", "YOU holding a copy of Casino Royale")]),
        ("He named his spy after the author of a bird book on his shelf, because he wanted the dullest name he could find.",
         [top("bird", "birds_book.jpg", "Birds of the West Indies", "The bird book by ornithologist James Bond")]),
        ("Fourteen Bond books. Every one written in the Jamaican winter.",
         [top("Bond books", "bond_books.jpg", "14 Bond books", "YOU: a stack of the paperbacks")]),
        ("He failed at the careers everyone wanted for him, then built one around the life he wanted.",
         [full("careers")]),
        ("Follow for the next legend: the climber who ate cat food and built Patagonia.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Yvon Chouinard"),
     verify=["left Sandhurst early; failed the Foreign Office exam", "the 'worst stockbroker' self-description",
             "assistant to Admiral Godfrey, Director of Naval Intelligence", "1944 Jamaica visit; Goldeneye built 1946",
             "Sunday Times contract with two months off each winter", "Casino Royale written early 1952, age 43",
             "named after ornithologist James Bond, 'the dullest name'", "14 Bond books written at Goldeneye"]),

dict(id="fleming_b_guess", legend="Ian Fleming", version="B", ep="Guess who #2",
     fmt="Guess the Legend", length="about 50 s",
     film="One take to camera. A martini on the table is a nice silent clue.",
     talk=["01_talk.mp4"],
     highlight=["guess", "strike"],
     lines=[
        ("Can you guess this legend from the story of his life? Comment the second you know.",
         [top("guess", "portrait.jpg", "Guess the legend", "Portrait of Ian Fleming, face pixelated", censor=CENSOR)]),
        ("Rich family. Famous older brother. He's the disappointment.",
         [top("Rich", "family.jpg", "The disappointment", "1920s English country house")]),
        ("Leaves military academy early. Strike one.",
         [top("military", "sandhurst.jpg", "Strike one", "Sandhurst, old postcard")]),
        ("Fails the Foreign Office exam. Strike two.",
         [top("Fails", "foreign_office.jpg", "Strike two", "The Foreign Office, London")]),
        ("Becomes a stockbroker, and says he's the worst one in the world. Strike three.",
         [top("stockbroker", "stock_exchange.jpg", "Strike three", "1930s London Stock Exchange")]),
        ("Then the war: he's planning secret operations for naval intelligence.",
         [top("war", "admiralty.jpg", "World War II", "The Admiralty, 1940s")]),
        ("After the war, he builds a house above a reef in Jamaica.",
         [top("house", "goldeneye.jpg", "The hideout", "The cove at Oracabessa, Jamaica")]),
        ("He swims every morning, and writes every morning.",
         [full("swims", "snorkel.mp4", desc="YOU: snorkelling over a reef")]),
        ("At forty-three, he writes his first novel in about two months.",
         [top("novel", "typewriter.jpg", "First novel", "Old typewriter on a terrace")]),
        ("Last clue: his main character likes his martini shaken, not stirred.",
         [top("Last", "martini.jpg", "Last clue", "YOU: a martini on the bar")]),
        ("It's Ian Fleming. The man who invented James Bond.",
         [top("Ian", "portrait.jpg", "Ian Fleming", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: a climber turned billionaire"),
     verify=["Casino Royale written in about two months (Jan–Mar 1952)"]),

dict(id="fleming_c_footsteps", legend="Ian Fleming", version="C", ep="Ep 02 · In his footsteps",
     fmt="In Their Footsteps", length="about 70 s",
     film="A full 'Fleming day' somewhere with a reef: talk takes in the morning and evening, b-roll of the swim, writing on a terrace, lunch and a nap.",
     talk=["01_morning.mp4", "02_evening.mp4"],
     highlight=["swim", "2,000", "Bond"],
     lines=[
        ("I'm about to live one day exactly like the man who wrote James Bond.", []),
        ("His name was Ian Fleming, and he wrote Casino Royale at a house on the water in Jamaica called Goldeneye.",
         [top("Ian", "portrait.jpg", "Ian Fleming", "Portrait of Ian Fleming (check licence)"),
          top("Goldeneye", "goldeneye.jpg", "Goldeneye, Jamaica", "The cove at Oracabessa")]),
        ("His routine was simple. Wake up, swim the reef.",
         [full("swim", "snorkel.mp4", "Step 1: swim", "YOU: snorkelling over a reef")]),
        ("Then he'd sit down and write about two thousand words before lunch.",
         [top("sit", "writing.mp4", "Step 2: 2,000 words", "YOU: writing on a terrace, sea behind")]),
        ("Lunch. A long nap. A little more work in the evening.",
         [full("Lunch", "lunch_nap.mp4", "Step 3: lunch, nap", "YOU: lunch with a view, then a hammock")]),
        ("That's it. That's the schedule that built fourteen Bond books.",
         [top("schedule", "bond_books.jpg", "14 books", "YOU: a stack of the paperbacks")]),
        ("So, I did it. Here's my two thousand words, written with salt still in my hair.",
         [top("Here's", "my_pages.mp4", "My 2,000 words", "YOU: flipping through your written pages")]),
        ("Honest review: the swim makes the writing easier. Your brain shows up already awake.", [full("Honest")]),
        ("Fleming didn't separate the life from the work. The sea is all over those books.", []),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Chouinard's surf rule"),
     verify=["his routine (morning swim, about 2,000 words, nap, evening revision) from his essay 'How to Write a Thriller'",
             "only say the 'honest review' line if it's true for you"]),

# ----------------------------------------------------------- YVON CHOUINARD
dict(id="chouinard_a_origin", legend="Yvon Chouinard", version="A", ep="Ep 03",
     fmt="The Origin Story", length="about 85 s",
     film="One take to camera at a crag or a surf break. Plus clips of you: car boot full of gear, and surfing.",
     talk=["01_talk.mp4"],
     highlight=["forge", "pitons", "cat", "Patagonia", "surfing"],
     lines=[
        ("In 1957, a broke eighteen-year-old climber bought a used forge from a junkyard. Sixty-five years later, he gave away a three-billion-dollar company.",
         [top("forge", "forge.jpg", "1957", "An old coal forge and anvil")]),
        (SERIES_LINE, [full("This")]),
        ("Yvon Chouinard was the kid who only spoke French at school in California, and got picked on for it.",
         [top("Yvon", "young.jpg", "Yvon Chouinard", "Photo of young Chouinard (licensed) or an illustration")]),
        ("He found falconry, then climbing, and then he basically lived in Yosemite.",
         [top("falconry", "yosemite.jpg", "Yosemite", "El Capitan or Camp 4, old photo")]),
        ("He couldn't afford gear, so he taught himself to blacksmith and made his own pitons.",
         [top("blacksmith", "pitons.jpg", "Homemade pitons", "Old steel pitons")]),
        ("He sold them out of the back of his car, a dollar fifty each, and lived on about a dollar a day.",
         [top("sold", "car_boot.mp4", "$1.50 each", "YOU: opening a car boot full of climbing gear")]),
        ("At one point, that meant eating cans of cat food.",
         [top("cans", "cat_food.jpg", "The diet", "A dented tin of cat food")]),
        ("By 1970 his little company was the biggest climbing hardware supplier in America.",
         [full("biggest")]),
        ("Then he noticed his pitons were wrecking the rock he loved, so he stopped selling his best product.",
         [top("wrecking", "scarred_rock.jpg", "Damaging the rock", "Close-up of a scarred granite crack")]),
        ("He started selling clothes instead. He called it Patagonia.",
         [top("clothes", "patagonia.jpg", "1973: Patagonia", "Patagonia shopfront or logo")]),
        ("And the company rule? When the surf's up, go surfing.",
         [full("rule", "surf.mp4", "Company policy", "YOU: surfing")]),
        ("In 2022, he gave the whole company away. He said Earth is now the only shareholder.",
         [top("gave", "headline.png", "2022", "Screenshot of the news headline")]),
        ("He never wanted to be a businessman. He just wanted to keep climbing.", [full("never")]),
        ("Follow for the next legend: the writer who went fishing every afternoon.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Ernest Hemingway"),
     verify=["1957 used forge from a junkyard", "spoke only French at school and was an outsider",
             "falconry led to climbing", "pitons at $1.50, living on about $1 a day",
             "the cat food story", "biggest US climbing hardware supplier by 1970",
             "phasing out pitons (1972 'clean climbing')", "Patagonia 1973", "2022 transfer, ~$3B"]),

dict(id="chouinard_b_guess", legend="Yvon Chouinard", version="B", ep="Guess who #3",
     fmt="Guess the Legend", length="about 50 s",
     film="One take to camera in a fleece, outdoors.",
     talk=["01_talk.mp4"],
     highlight=["guess", "cat"],
     lines=[
        ("Can you guess this legend from the story of his life? Comment the second you know.",
         [top("guess", "portrait.jpg", "Guess the legend", "Portrait of Chouinard, face pixelated", censor=CENSOR)]),
        ("Grows up a French-speaking outsider in Southern California.",
         [top("Grows", "1940s_california.jpg", "The outsider", "1940s Southern California street")]),
        ("Gets into falconry, which gets him into climbing.",
         [top("falconry", "falcon.jpg", "Falconry", "A falcon on a glove")]),
        ("Teaches himself blacksmithing to make his own climbing gear.",
         [top("blacksmithing", "forge.jpg", "Self-taught blacksmith", "An old coal forge and anvil")]),
        ("Sells it from the back of his car. Lives on a dollar a day. Eats cat food.",
         [top("Sells", "cat_food.jpg", "The diet", "A dented tin of cat food")]),
        ("Builds the biggest climbing hardware company in America, then quits making his best seller because it's damaging the rock.",
         [top("quits", "scarred_rock.jpg", "Quits his best seller", "Scarred granite crack")]),
        ("Brings back a rugby shirt from Scotland, and starts selling clothes.",
         [top("rugby", "rugby_shirt.jpg", "The rugby shirt", "A striped 1970s rugby shirt")]),
        ("Writes a book called Let My People Go Surfing.",
         [top("Writes", "book.jpg", "The book", "YOU: holding the book, company name covered", censor=[0.0, 0.7, 1.0, 0.3])]),
        ("Last clue: in 2022, he gives the entire company away to fight climate change.",
         [top("Last", "headline.png", "Last clue", "News headline, company name pixelated", censor=[0.0, 0.0, 1.0, 0.4])]),
        ("It's Yvon Chouinard. The founder of Patagonia.",
         [top("Yvon", "portrait.jpg", "Yvon Chouinard", "The same portrait, no pixelation")]),
        ("Comment when you got it, and follow for the next one.", [full("got")]),
     ],
     end_card=dict(at="follow", title="Guess the Legend", sub="Next: a teenage pirate"),
     verify=["the 1970 rugby shirt from Scotland that started the clothing line"]),

dict(id="chouinard_c_footsteps", legend="Yvon Chouinard", version="C", ep="Ep 03 · In his footsteps",
     fmt="In Their Footsteps", length="about 70 s",
     film="A 'surf's up' workday: talk takes at dawn and afternoon, b-roll of the surf, laptop work still wet, and a climb.",
     talk=["01_dawn.mp4", "02_afternoon.mp4"],
     highlight=["surf's", "surfing", "Patagonia"],
     lines=[
        ("The founder of Patagonia had one company rule, and today I'm following it.", []),
        ("His name is Yvon Chouinard, and the rule is the title of his book: Let My People Go Surfing.",
         [top("Yvon", "portrait.jpg", "Yvon Chouinard", "Photo of Chouinard (licensed) or an illustration"),
          top("book", "book.jpg", "The rule", "YOU: holding the book")]),
        ("When the surf's up, you go surfing. You fit the work around it.",
         [full("surf's", "surf_dawn.mp4", "Dawn patrol", "YOU: dawn surf session")]),
        ("He built that rule from years of climbing in Yosemite and surfing in Malibu, back when he sold homemade gear out of his car.",
         [top("climbing", "yosemite.jpg", "Yosemite, 1960s", "El Capitan or Camp 4, old photo")]),
        ("So: surf first.", [full("So")]),
        ("Then the laptop, still salty.",
         [top("laptop", "laptop.mp4", "Then work", "YOU: working on a laptop in a wetsuit or towel")]),
        ("Then a climb in the afternoon.",
         [full("climb", "climb.mp4", desc="YOU: bouldering or a scramble")]),
        ("Here's what surprised me: I got more done in four hours than on a normal day.", [full("Here's")]),
        ("Chouinard's trick is flexibility. Chase the good conditions, and fit the work around them.",
         [top("trick", "portrait.jpg", "The trick", "Same Chouinard photo")]),
        ("He built a three-billion-dollar company that way, then gave it all away.",
         [top("gave", "headline.png", "2022: gives it away", "Screenshot of the news headline")]),
        ("Follow for the next legend's footsteps.", []),
     ],
     end_card=dict(at="Follow", title=SERIES, sub="Next: Hemingway's Key West"),
     verify=["Patagonia's flextime ('let my people go surfing') policy",
             "only say the 'four hours' line if it's true for you"]),
]


def anchor_for(at, words, lo, hi):
    """Return at or at#n so that it resolves inside tokens [lo, hi)."""
    for n in range(1, 30):
        cand = at if n == 1 else f"{at}#{n}"
        i = find_word(cand, words)
        if i is None:
            break
        if lo <= i < hi:
            return cand
    raise SystemExit(f"anchor '{at}' not found in its line")


def build(script):
    words, ranges = [], []
    for line, _ in script["lines"]:
        toks = line.split()
        ranges.append((len(words), len(words) + len(toks)))
        words += [{"text": t} for t in toks]
    panels = []
    for (line, ps), (lo, hi) in zip(script["lines"], ranges):
        for p in ps:
            p = {k: v for k, v in p.items() if k != "desc" and v is not None}
            p["at"] = anchor_for(p["at"], words, lo, hi)
            panels.append(p)
    ec = dict(script["end_card"])
    ec["at"] = anchor_for(ec["at"], words, *ranges[-1]) if ec["at"] in script["lines"][-1][0] \
        else anchor_for(ec["at"], words, *ranges[-2])
    plan = {
        "footage": f"input/{script['id']}",
        "series_tag": f"{SERIES} · {script['ep']}",
        "highlight": script["highlight"],
        "sequence": [{"talk": t} for t in script["talk"]],
        "panels": panels,
        "end_card": ec,
    }
    return plan, len(words)


def md(script, n_words):
    out = [f"### {script['version']}. {script['fmt']}: `{script['id']}`", ""]
    out.append(f"**Length:** {script['length']} ({n_words} words). **Film:** {script['film']}")
    out.append("")
    out.append("| Say | On screen |")
    out.append("|---|---|")
    for line, ps in script["lines"]:
        cells = []
        for p in ps:
            if p.get("full") == "talk":
                cells.append("you, full screen")
            elif p.get("full"):
                lab = f" · pill **{p['label'].upper()}**" if p.get("label") else ""
                cells.append(f"full screen `{p['full']}`{lab}")
            else:
                cz = " (pixelated)" if p.get("censor") else ""
                cells.append(f"top `{p['file']}`{cz} · pill **{p['label'].upper()}**")
        out.append(f"| {line} | {'<br>'.join(cells)} |")
    out.append("")
    ec = script["end_card"]
    out.append(f"End card from \"{ec['at']}\": **{ec['title'].upper()}** / {ec['sub'].upper()}")
    out.append("")
    files = {}
    for _, ps in script["lines"]:
        for p in ps:
            f = p.get("file") or (p["full"] if p.get("full") != "talk" else None)
            if f and f not in files:
                files[f] = p.get("desc") or ""
    out.append("<details><summary>Footage and images to gather</summary>")
    out.append("")
    for t in script["talk"]:
        out.append(f"- `{t}`: you talking to camera")
    for f, d in files.items():
        out.append(f"- `{f}`: {d}")
    out.append("")
    out.append("</details>")
    out.append("")
    out.append("✓ Check before posting: " + "; ".join(script["verify"]) + ".")
    out.append("")
    return "\n".join(out)


def main():
    plans_dir = REPO / "series/lifestyle-legends/plans"
    for old in plans_dir.glob("*.json"):
        old.unlink()
    sections = {}
    for s in SCRIPTS:
        plan, n = build(s)
        (plans_dir / f"{s['id']}.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
        sections.setdefault(s["legend"], []).append(md(s, n))
    head = Path(__file__).with_name("scripts_head.md").read_text()
    body = "\n---\n\n".join(f"## {legend}\n\n" + "\n".join(parts)
                            for legend, parts in sections.items())
    (REPO / "series/lifestyle-legends/SCRIPTS.md").write_text(head + "\n" + body)
    print(f"{len(SCRIPTS)} scripts, plans in {plans_dir}")


if __name__ == "__main__":
    main()
