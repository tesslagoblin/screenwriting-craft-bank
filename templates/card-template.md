# Card template

Two layers. Both must be populated for a card to count as complete.

## Layer 1: database properties

The browsable, filterable card view.

| Field | Type | What goes in it |
|---|---|---|
| Technique | title | Name the mechanic, not the moment. "Endorse then stunt," not "the scene where she..." |
| Show | select | Pick from your configured list |
| Source Show | text | Free text, for shows not in the select yet |
| Episode | text | S01E02, or the episode name |
| How It Works | text | The mechanic in two or three sentences |
| Apply When | text | The situation in your own writing where you would reach for this |
| Project Relevance | text | How it applies to your thing, specifically |
| Tags | multi-select | Short keywords. `needle-drop`, `cold-open`, `humiliation-arc`, `found-family` |
| Additional Examples | text | Other shows doing the same mechanic. This is where stacking goes. |

## Layer 2: page body

Two headings, always, in this order.

### Original Thoughts

Their raw reaction, verbatim, untouched. However rambling, however half-formed,
including dictation noise and transcription errors.

Never paraphrase this. If you do not have it, leave a visible stub:

> 📌 Backfill pending: no verbatim captured for this card. Ask before treating
> the synthesis as complete.

### Where We Dug

Your synthesis. The conversation thread that turned a raw reaction into a named
technique: the questions that pushed it, the beats you surfaced together. Pull
their sharpest lines out as block quotes.

## Blank card

```markdown
# [Technique name]

**Show:** [show] · **Episode:** [ep] · **Tags:** [tag], [tag]

**How it works:** [two or three sentences on the mechanic]

**Apply when:** [the situation where you would reach for this]

**Project relevance:** [how it applies to your own thing]

**Additional examples:** [other shows doing the same mechanic]

## Original Thoughts

[verbatim, untouched]

## Where We Dug

[synthesis, with block quotes]
```
