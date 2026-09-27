# Notion setup

You do not have to use Notion. The card structure works in plain markdown files,
Obsidian, or anything else. This is just what the scripts here expect.

## Database properties

Create a database with these properties:

- `Technique` - Title
- `Show` - Select. Seed it with whatever you watch most. New shows can go in
  `Source Show` until you promote them.
- `Source Show` - Text
- `Episode` - Text
- `How It Works` - Text
- `Apply When` - Text
- `Project Relevance` - Text
- `Tags` - Multi-select
- `Additional Examples` - Text

## Why properties and page body are split

Properties stay short so the table view is browsable and filterable at a glance.
The page body holds the depth, including the verbatim that would make a table
cell unreadable.

If you put the verbatim in a property, you will stop reading the table. If you
put the synthesis only in the body, you will stop finding anything.

## Connecting the API

1. Create an integration at notion.so/my-integrations
2. Copy the secret, and set it: `export NOTION_API_KEY=[YOUR_API_KEY]`
3. Share your database with the integration from the page's Connections menu
4. Grab the database ID out of the URL. It is the 32-character string.

Note that recent Notion API versions expose both a `database_id` and a
`data_source_id`. Create pages against the database ID, query against the data
source ID.
