# Years

Years is the calendar year container. Days, Goals, Habits, Projects, Workout Sessions, Fiscal Years, and My Significant Events may hang from Years.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Years                                                       |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681fcb1c6f0780ea0bde3` |
| Surface           | Catalog `Name` `Goal Setting & Yearly Planner`              |
| Title property    | `Name`                                                      |

```sql
SELECT Name, url FROM "collection://316919d4-1936-816b-8db8-000b4e826d28"
```

## Writable properties an Agent may set

| Property                  | Type     | Fill rule                                                          |
| ------------------------- | -------- | ------------------------------------------------------------------ |
| `Name`                    | title    | Calendar year label already used in Workspace, for example `2026`. |
| `Related Fiscal Year`     | relation | Matching Fiscal Years page.                                        |
| `Related Day`             | relation | Prefer writing the link on the Days page.                          |
| `Related Goal`            | relation | Prefer writing the link on the Goals page.                         |
| `Related Project`         | relation | Prefer writing the link on the Projects page.                      |
| `Related Habit`           | relation | Prefer writing the link on the Habits page.                        |
| `Related Event`           | relation | Prefer writing the link on My Significant Events.                  |
| `Related Workout Session` | relation | Prefer writing the link on Workout Sessions.                       |

## Do not write

Rollup and formula properties including `Year Report`, `Total Goals Set`, `Total Goals Completed`, `Financial Report`.
