# Goals

Goal is the top of the execution chain. Task and Project both hang from Goal. Goal wording follows Covey The 7 Habits of Highly Effective People.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Goals                                                       |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681c4a525d4cab3bfa198` |
| Surface           | Catalog `Name` `Goal Setting & Yearly Planner`              |
| Default template  | `https://app.notion.com/p/316919d4193681c4b5d8f55d90e8e77d` |

Query by title.

```sql
SELECT Goal, Status, url FROM "collection://316919d4-1936-81ef-b890-000bb66c709b"
WHERE Goal LIKE '%On-premise%'
```

Observed title prefix is `[G]` plus an optional domain tag, for example `[G][Coding] Build a On-premise Platform`.

## Writable properties an Agent may set

| Property           | Type     | Fill rule                                                                                                                                                                                       |
| ------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Goal`             | title    | Full Goal statement. Keep the `[G]` prefix when the surrounding Goals already use `[G]`.                                                                                                        |
| `Status`           | status   | One of `Inbox`, `Not started`, `In progress`, `Completed`. Use `In progress` for a live Goal.                                                                                                   |
| `Prompt`           | select   | One of `I want to learn...`, `I want to have...`, `I want to be...`, `What I want to be doing is...`, `I want to create...`, `I want to try...`, `I want to experience...`, `I want to see...`. |
| `Time Frame`       | select   | One of `1 Year`, `2 Years`, `3 Years`, `5 Years`, `10 Years`, `12 Years`, `15 Years`, `20 Years`.                                                                                               |
| `Deadline`         | date     | Expanded keys `date:Deadline:start` and `date:Deadline:is_datetime`.                                                                                                                            |
| `Related Area`     | relation | URL of the Area that the Goal serves. Do not set Area `TOP OF MIND`.                                                                                                                            |
| `Related Task`     | relation | Created by linking from Task `Related Goal`. Prefer writing the link on the Task page.                                                                                                          |
| `Related Project`  | relation | Created by linking from Project `Related Goal`. Prefer writing the link on the Project page.                                                                                                    |
| `Year`             | relation | Years data source page for the planning year.                                                                                                                                                   |
| `Prioritise!`      | checkbox | `__YES__` only when the owner marked the Goal as a priority.                                                                                                                                    |
| `Obstacles`        | text     | Owner language. Leave empty unless the owner supplied text.                                                                                                                                     |
| `Solutions`        | text     | Owner language. Leave empty unless the owner supplied text.                                                                                                                                     |
| `Review Interval`  | number   | Days between reviews. Copy a nearby live Goal when the owner did not specify.                                                                                                                   |
| `Last Review Date` | date     | Set only after an actual review.                                                                                                                                                                |
| `Achieved`         | checkbox | `__YES__` only when the owner confirmed completion. Also set `date:Date Achieved:start`.                                                                                                        |

## Do not write

Formula, rollup, and button properties including `Report`, `Goal?`, `Next Review`, `Review Overdue`, `Set Live Goal`, `Set Completed`, `Set Achieved`, `Mark Reviewed`.
