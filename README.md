# Screenwriting Craft Bank

A skill for turning "that was really good" into something you can actually use
later. You talk about a show you are watching, and it files a technique card
with your own words preserved next to the analysis.

See [examples/sample-card.md](examples/sample-card.md). The best line on it is
the raw reaction, not the analysis: "she cant compete on pretty so she competes
on chaos."

## Why I built this

I kept noticing smart things in other people's shows and then losing them. A
week later all I had left was "there was a thing in that episode where she
does the... you know." The useful part, the specific mechanic, was always gone.

The other problem was worse. When I did write notes down with an AI, it would
tidy my reaction into clean professional sentences, and the clean version was
always duller than what I actually said while watching. My first reaction was
sharper than the summary of it. So the main rule here is that my raw words never
get replaced, only added to.

## How it works

1. **You talk.** You name a show and describe what you noticed. The assistant
   stays in thinking-partner mode and asks one or two questions about the
   specifics: what the shot was, how the other person reacted, what the music
   was doing. It does not write anything down yet.

2. **You say when.** When you say "bank it" or "wrap it up," it writes the card.
   One card per technique. Three techniques in one conversation means three
   cards, never one merged one.

3. **The card has two layers.** A short set of fields you can browse and filter
   (the mechanic, when to use it, tags), and a page body with your raw words
   untouched on top and the analysis underneath.

4. **Same mechanic, new show?** When the assistant recognises a mechanic you
   have already banked, it adds the new example to the existing card rather
   than making a near-duplicate, so techniques accumulate examples instead of
   scattering. The script only creates new cards for now. Automatic duplicate
   detection is on the build-next list.

<!-- Screenshot 1 goes here: the Craft Bank database in table view, filtered by a tag, showing a dozen technique cards -> docs/screenshot-table.png -->

<!-- Screenshot 2 goes here: a single card open, showing the Original Thoughts section with raw unedited text above the Where We Dug analysis -> docs/screenshot-card.png -->

## What is in here

```
SKILL.md              the skill itself, drop into your assistant
templates/            card format, and the database schema
scripts/create_card.py  makes a properly structured card via the Notion API
examples/             an invented sample card so you can see the shape
```

## What I used to build it

- **Claude** as the thinking partner and the thing that writes the cards
- **Notion** as the library, through its API
- **Python**, standard library only, no dependencies

Built with my AI assistant, Mr. Shrimp, running on Claude.

## How to use it yourself

**The skill on its own needs nothing.** For Claude Code, copy the whole folder
to `~/.claude/skills/craft-bank/` so `SKILL.md` sits at the top and can find
`templates/`. Or paste `SKILL.md` (and `templates/card-template.md`) into a
conversation and say "follow this."

**If you want the Notion side:**

```bash
git clone https://github.com/tesslagoblin/screenwriting-craft-bank.git
cd screenwriting-craft-bank
```

Build a database with the properties listed in `templates/notion-schema.md`,
then:

```bash
export NOTION_API_KEY=[YOUR_API_KEY]
export CRAFT_BANK_DB=[YOUR_DATABASE_ID]

python scripts/create_card.py \
  --technique "Endorse then stunt" \
  --show "Some Show" --episode "S01E04" \
  --how "What the mechanic is." \
  --apply-when "When you would reach for it." \
  --tags "status,misdirection" \
  --verbatim-file cards/raw.txt \
  --dug-file cards/synthesis.md
```

Keep those files in `cards/`. It is gitignored because it holds your real
reactions.

If you skip `--verbatim-file` it will still make the card, but it writes a
visible backfill stub in the Original Thoughts section and tells you the card is
incomplete. That is deliberate. A card without your original reaction is a card
you will not trust in six months.

Add `--dry-run` to print the card it would create without calling Notion. No
API key or database ID needed for that, so it is a good way to check your files
first.

You will need to share the database with your Notion integration first, or the
API will tell you it does not exist.

<!-- Screenshot 3 goes here: terminal output from create_card.py, including the warning it prints when verbatim is missing -> docs/screenshot-script.png -->

## The rules, in short

1. Observations about other people's shows go here, not into your own project
   notes. How it applies to your work lives inside the card.
2. You think out loud first. Nothing gets carded until you ask for it.
3. It suggests wrapping up at natural points: a change of topic, a clean
   takeaway, or a long stretch on one thing. One line each time, never nagging.
4. Every card gets both layers: the browsable fields and the page body.
5. Your exact words are the receipt. They never get paraphrased away.
6. Same mechanic, different show: it adds to the existing card rather than
   making a duplicate.
7. It tells you what it saved and where. Nothing is saved silently.

## What I would build next

- **Tag cleanup.** Tags accumulate and drift. `cold-open` and `opening-beat` end
  up as two things.
- **A "what have I not used" view.** Cards get banked and then never looked at
  again. Surfacing untouched ones against whatever I am currently writing would
  close the loop.
- **Backfill detection.** A pass that finds cards missing their verbatim and
  chases them, rather than me noticing by accident.
- **Stacking in the script.** Right now the assistant spots repeats in
  conversation. The script should also check existing cards itself before
  making a new one.

## A note on the material

The example card is invented. No real cards, no personal viewing history and no
source material are in this repo, and `.gitignore` blocks the obvious paths.
