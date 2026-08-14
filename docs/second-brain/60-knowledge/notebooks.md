# Notebooks

Notebooks is a long-form grouping for Notes and Articles.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Notebooks                                                   |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936817c8e1cefe0322e6a98` |
| Surface           | Catalog `Name` `Notebooks`                                  |
| Title property    | `Title`                                                     |
| Default template  | `https://app.notion.com/p/316919d4193681eeb951f0edc76b6bd4` |

```sql
SELECT Title, Status, url FROM "collection://316919d4-1936-81b1-8b56-000b0aafd8bc"
```

## Writable properties an Agent may set

| Property              | Type     | Fill rule                                                                                                               |
| --------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| `Title`               | title    | Notebook name. Do not invent a duplicate.                                                                               |
| `Status`              | status   | One of `New Notebook`, `Highlighted Notebook`, `Live Notebook`, `Archived`. Use `Live Notebook` for an active grouping. |
| `Summary`             | text     | Owner language only.                                                                                                    |
| `Related Topic`       | relation | Knowledge Base Topics.                                                                                                  |
| `Related Note`        | relation | Prefer writing the link on Notes.                                                                                       |
| `Related CS Articles` | relation | Prefer writing the link on Articles.                                                                                    |
| `Related Area`        | relation | Optional. Do not set Area `TOP OF MIND`.                                                                                |
| `Related Project`     | relation | Optional.                                                                                                               |

Leave `Attachments` empty unless the owner supplied a file.

## Do not write

Button `Process`. Formula and rollup properties including `Notebook Report`, `Notes/Refs Total`, `Age (Weeks)`, `Last Note Edit`, `Project Area`, `Topic Area`.
