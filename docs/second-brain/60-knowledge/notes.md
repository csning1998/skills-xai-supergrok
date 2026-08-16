# Notes

Note follows Zettelkasten types. The owner usually writes a Permanent Note directly. Note frequency is currently low. How Note will pair with AI is still open. Until the owner sets the AI pairing procedure, create a Note only when the owner asked for a Note.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Notes                                                       |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681ddace9dad6e1a37461` |
| Surface           | Catalog `Name` `Knowledge Base`                             |
| Templates         | New Fleeting Note, New Literature Note, New Permanent Note  |

Observed title pattern is `YYYYMMDD-HHMM` plus a topic, for example `20260308-2003 Financial Database Manual`.

```sql
SELECT Title, "Note Type", Status, url FROM "collection://316919d4-1936-81bb-93b1-000b2f5298db"
WHERE Title LIKE '%Financial Database%'
```

## Note Type versus Status

`Note Type` is the Zettelkasten class.

- `Fleeting Note`
- `Literature Note`
- `Permanent Note`
- `Archived`

The owner rarely uses `Literature Note`. Literature Note is close in nature to Resource.

`Status` is document progress, matching Computer Science Articles.

- To do group contains `Inbox` and `Not Started`.
- In progress group contains `Paused`, `In Progress`, and `Staging`.
- Complete group contains `Stable` and `Abandoned`.

Notes Inbox Status is not Tasks Inbox Status.

## Writable properties an Agent may set

| Property            | Type         | Fill rule                                                                   |
| ------------------- | ------------ | --------------------------------------------------------------------------- |
| `Title`             | title        | Use `YYYYMMDD-HHMM` plus topic when creating a new Note.                    |
| `Note Type`         | select       | Default `Permanent Note` unless the owner asked for Fleeting or Literature. |
| `Status`            | status       | `In Progress` while drafting. `Stable` when the owner accepted the Note.    |
| `Abstract`          | text         | Short owner-facing summary.                                                 |
| `Classification`    | select       | One of `Reference`, `Concept`, `Guide`, `Decision`, `Debug`, `Tool`.        |
| `Life Cycle`        | select       | One of `Theorem`, `Day 0 Planning`, `Day 1 Development`, `Day 2 Operation`. |
| `Related Goal`      | relation     | Optional.                                                                   |
| `Related Project`   | relation     | Optional.                                                                   |
| `Related Life Area` | relation     | Optional. Do not set Area `TOP OF MIND`.                                    |
| `Related Topic`     | relation     | Optional.                                                                   |
| `Related Note`      | relation     | Other Note pages this Note links to.                                        |
| `Related Skills`    | multi_select | Existing skill tags only. Do not invent a tag.                              |
| `userDefined:URL`   | url          | Source URL when one exists.                                                 |
| `Source Author`     | text         | For a Literature Note.                                                      |
| `Favourites`        | checkbox     | Leave empty unless the owner starred the Note.                              |

## Do not write

Formula reports, Archive button, and rollup columns. Do not set Notes `Status` to `Inbox` as a substitute for Tasks Inbox Status.
