#!/usr/bin/env python3
"""
Create a Craft Bank card in Notion with the full two-layer structure.

Enforces the two rules that matter: the card gets both an Original Thoughts
section and a Where We Dug section, and if you have no verbatim it writes a
visible backfill stub instead of quietly shipping a synthesis-only card.

Setup:
    export NOTION_API_KEY=[YOUR_API_KEY]
    export CRAFT_BANK_DB=[YOUR_DATABASE_ID]

Usage:
    python create_card.py --technique "Endorse then stunt" \
        --show "Some Show" --episode "S01E03" \
        --how "What the mechanic is." \
        --apply-when "When you need X." \
        --relevance "How it applies to my thing." \
        --tags "misdirection,status" \
        --verbatim-file raw.txt \
        --dug-file synthesis.md

    # No verbatim yet? It will write a backfill stub and warn you.
    python create_card.py --technique "..." --show "..." --how "..."
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.notion.com/v1/"
VERSION = "2025-09-03"
CHUNK = 1900  # Notion caps a single rich_text object at 2000 chars

BACKFILL_STUB = (
    "📌 Backfill pending: no verbatim captured for this card. "
    "Ask before treating the synthesis as complete."
)


def api(path, body=None, method="GET"):
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        sys.exit("Set NOTION_API_KEY first.")
    req = urllib.request.Request(
        API + path,
        data=json.dumps(body).encode() if body else None,
        headers={
            "Authorization": f"Bearer {key}",
            "Notion-Version": VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        sys.exit(f"Notion API error {e.code}: {e.read().decode()[:400]}")


def text_prop(value):
    return {"rich_text": [{"text": {"content": value[:2000]}}]} if value else {"rich_text": []}


def heading(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": text}}]}}


def para(text):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": text}}]}}


def quote(text):
    return {"object": "block", "type": "quote",
            "quote": {"rich_text": [{"text": {"content": text}}]}}


def chunked(text, block_fn):
    """Notion rejects rich_text over 2000 chars. Split long text across blocks."""
    out = []
    for i in range(0, len(text), CHUNK):
        out.append(block_fn(text[i:i + CHUNK]))
    return out or [block_fn("")]


def read(path):
    return open(path, encoding="utf-8").read().strip() if path else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--technique", required=True)
    ap.add_argument("--show", default="")
    ap.add_argument("--source-show", default="")
    ap.add_argument("--episode", default="")
    ap.add_argument("--how", default="", help="How It Works")
    ap.add_argument("--apply-when", default="")
    ap.add_argument("--relevance", default="", help="Project Relevance")
    ap.add_argument("--tags", default="", help="comma separated")
    ap.add_argument("--examples", default="", help="Additional Examples")
    ap.add_argument("--verbatim-file", help="file holding their raw words, untouched")
    ap.add_argument("--dug-file", help="file holding your synthesis")
    ap.add_argument("--db", default=os.environ.get("CRAFT_BANK_DB"))
    args = ap.parse_args()

    if not args.db:
        sys.exit("Set CRAFT_BANK_DB or pass --db")

    verbatim = read(args.verbatim_file)
    dug = read(args.dug_file)

    props = {
        "Technique": {"title": [{"text": {"content": args.technique}}]},
        "Episode": text_prop(args.episode),
        "How It Works": text_prop(args.how),
        "Apply When": text_prop(args.apply_when),
        "Project Relevance": text_prop(args.relevance),
        "Additional Examples": text_prop(args.examples),
        "Source Show": text_prop(args.source_show),
    }
    if args.show:
        props["Show"] = {"select": {"name": args.show}}
    if args.tags:
        props["Tags"] = {"multi_select":
                         [{"name": t.strip()} for t in args.tags.split(",") if t.strip()]}

    body = [heading("Original Thoughts")]
    if verbatim:
        body += chunked(verbatim, quote)
    else:
        body.append(para(BACKFILL_STUB))
    body.append(heading("Where We Dug"))
    body += chunked(dug, para) if dug else [para("")]

    page = api("pages", {
        "parent": {"database_id": args.db},
        "properties": props,
        "children": body,
    }, "POST")

    print(f"Created: {args.technique}")
    print(f"  {page.get('url','')}")
    print("  Original Thoughts: " +
          ("verbatim saved" if verbatim else "BACKFILL STUB, go get the verbatim"))
    print("  Where We Dug: " + ("populated" if dug else "EMPTY"))
    if not verbatim:
        print("\nThis card is incomplete. Rule 5: verbatim is the receipt.")


if __name__ == "__main__":
    main()
