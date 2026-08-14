# Articles

Articles is a Computer Science notebook. Articles uses the same `Status` and `Note Type` values as Notes. Articles is not Notes. Create an Articles row only when the owner asked for a Computer Science article.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Articles                                                    |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/2f8919d41936812e8414c72e753a691c` |
| Title property    | `Title`                                                     |
| Default template  | `https://app.notion.com/p/2f8919d4193681bb9973d6bf07dd1fb0` |

```sql
SELECT Title, "Note Type", Status, url FROM "collection://2f8919d4-1936-817b-8ccd-000bc34fb63f"
WHERE Title LIKE '%Kubernetes%'
```

## Note Type versus Status

`Note Type` is the Zettelkasten class.

- `Fleeting Note`
- `Literature Note`
- `Permanent Note`
- `Archived`

`Status` is document progress.

- To do group contains `Inbox` and `Not Started`.
- In progress group contains `Paused`, `In Progress`, and `Staging`.
- Complete group contains `Stable` and `Abandoned`.

## Writable properties an Agent may set

| Property            | Type         | Fill rule                                                                                       |
| ------------------- | ------------ | ----------------------------------------------------------------------------------------------- |
| `Title`             | title        | Article title. Copy the Notes `YYYYMMDD-HHMM` pattern only when nearby Articles already use it. |
| `Note Type`         | select       | Default `Permanent Note` unless the owner asked for Fleeting or Literature.                     |
| `Status`            | status       | `In Progress` while drafting. `Stable` when the owner accepted the article.                     |
| `Abstract`          | text         | Short owner-facing summary.                                                                     |
| `Classification`    | select       | One of `Reference`, `Concept`, `Guide`, `Decision`, `Debug`, `Tool`.                            |
| `Life Cycle`        | select       | One of `Theorem`, `Day 0 Planning`, `Day 1 Development`, `Day 2 Operation`.                     |
| `Related CS Topics` | relation     | CS Topics pages. Do not use Knowledge Base Topics here.                                         |
| `Main Skills`       | relation     | Limit 1. One CS Topics page.                                                                    |
| `Related Topic`     | relation     | Optional Knowledge Base Topic.                                                                  |
| `Related Notebook`  | relation     | Optional.                                                                                       |
| `Related Project`   | relation     | Optional.                                                                                       |
| `Related Skills`    | multi_select | Existing skill tags only. Do not invent a tag.                                                  |
| `userDefined:URL`   | url          | Source URL when one exists.                                                                     |
| `Source Author`     | text         | For a Literature Note.                                                                          |
| `Topic Hint`        | text         | Optional.                                                                                       |
| `Blocked by`        | relation     | Other Articles that must finish first.                                                          |
| `Blocking`          | relation     | Other Articles that wait on this article.                                                       |
| `Favourites`        | checkbox     | Leave empty unless the owner starred the article.                                               |

Leave `AI Abstract`, `Attachments`, `Author`, `Last Highlighted`, `Last Synced`, `Task Started Time`, and `Task Completed Time` empty unless the owner asked.

## Do not write

Buttons `Add to System`, `Staging`, `Start / Pause`. Formula and rollup reports including `Report: Show Abstract`, `Report: Knowledge`, `Report: Metadata`, `Report: Blocker`.
