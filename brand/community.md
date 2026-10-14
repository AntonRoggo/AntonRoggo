# Lifestyle Legends: community plan

Skool: https://www.skool.com/natura-veritas-9920/about (group name: Lifestyle Legends)
Discord: discord.gg/XwfDe9Q3dZ

## Who it's for (2026-10-14, from Anton)

People like Anton:
1. **Health first.** They train, eat real food, sleep, and get outside.
2. **Nature and adventure.** Kitesurfing, hikes, oysters straight from the farm, trips with friends.
3. **Freedom.** Many want to earn online and live on their own schedule. This is a draw, but a quieter one: say "freedom", not "make money online".

They're "lifestyle legends": people who live the life, achieve something, and go on crazy adventures.

The long-term goal is to grow this into trips and residencies (e.g. a month in Japan), first online, then in person.

## How the funnel works

1. **Skool is the free front door.** Joining is free and all posts are private (members only). Skool isn't where the talking happens. It collects the email and points people to Discord.
2. **The email goes to Kit straight away.** One membership question asks for it.
3. **Discord is where the community lives.** New members introduce themselves in #introductions, and that unlocks the lessons.
4. **Anton gets a notification** for every new member.

### Setup checklist

**Skool (Settings):**
- [ ] Privacy: **Private**.
- [ ] Price: **Free**.
- [ ] Membership questions (max 3):
  1. "What's your best email? (we'll send trip invites and new lessons here)" (email type)
  2. "What's one adventure you want to do in the next 12 months?"
  3. "Health, adventure or freedom: which one are you here for most?"
- [ ] Approval: turn on auto-approve if your plan offers it, so joining is instant. Otherwise approve once a day.
- [ ] Pin one welcome post, the only thing new members see. Copy is below.
- [ ] Classroom: set every course's access to **private / manually granted**. Lessons unlock after the Discord intro (see the gating options).
- [ ] Turn off "allow members to post" in all categories except a single "Start here" one, so the talking moves to Discord.

**Email to Kit (Zapier, ~10 minutes):**
- Zap 1: Skool trigger **"New answered membership questions"**, then Kit action **"Add subscriber to tag"**. Tag: `lifestyle-legends`. Map the email answer to Email, the name to First name, and answers 2-3 to custom fields if you want them.
- Zap 2 (the notification): same Skool trigger, then a **Discord webhook** posting to a private `#new-members` channel: "🆕 {name} joined Lifestyle Legends: {answer 2}". If you'd rather get an email, use Gmail or Kit instead.
- The free Zapier plan allows 2-step Zaps, which is why this is two Zaps instead of one 3-step Zap.

**Discord:**
- Channels: `#start-here` (rules plus the Skool link), `#introductions`, `#general`, `#adventures`, `#health`, `#freedom` (online work), `#trips` (future residencies), `#lessons` (locked), `#new-members` (admin only).
- Native **Onboarding** (Server settings > Onboarding): new members only see `#start-here` and `#introductions` until they get the `Legend` role.
- **Intro unlocks access:** when someone posts in `#introductions`, they get the `Legend` role. Use a bot such as Carl-bot or YAGPDB (trigger: message in #introductions, action: add role), or a mod gives it by hand. The role unlocks every channel, including `#lessons`.

**Gating the Skool lessons (pick one):**
- **A. Automatic (recommended):** the lesson links live in the Discord `#lessons` channel, which only unlocks after the intro. Skool Classroom courses stay open to all members, but nobody finds them without the Discord link. There's no manual work.
- **B. Strict:** Skool courses stay private. After someone's Discord intro, you (or a mod) unlock the course for them in Skool. This takes 10 seconds per person but needs daily attention.

## Copy

**Skool "About" headline:** Lifestyle Legends: get healthy, go on adventures, gain freedom.

**Skool "About" description:**
> A free community for people who want more out of life than the 9 to 5 loop.
> We train, eat real food, get outside, and go on proper adventures: kitesurfing in Brazil, oyster farms in North Carolina, summers in Europe. Some of us are building online work so we can do it more often.
>
> Inside:
> - A Discord full of people who actually live like this
> - Lessons on health, travel and building freedom
> - First access to in-person trips and residencies (Japan is next on the list)
>
> How to get in: join here (free) → introduce yourself in the Discord → lessons unlock.

**Pinned welcome post (Skool):**
> Welcome, legend. 🌊
> This group is the front door. The real community is on Discord: [link]
> 1. Join the Discord
> 2. Post in #introductions: who you are, where you're based, and one adventure you want to do this year
> 3. That unlocks #lessons and the rest of the server
> See you in there.

**Discord #start-here:**
> Welcome to Lifestyle Legends: health, adventure, freedom.
> Introduce yourself in #introductions (name, where you're based, one adventure you want this year) to unlock the server and the lessons.
> Be good to each other. No spam, no selling in DMs.

## Later
- Trips and residencies: use the `lifestyle-legends` Kit tag plus membership answer 2 ("adventure you want to do") to pick destinations and email the waitlist.
- Add the Skool link to every YouTube description (done from the Austin vlog on) and to the Instagram bio.
