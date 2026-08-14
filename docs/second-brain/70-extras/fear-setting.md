# Fear Setting Database

Fear Setting Database is a Tim Ferriss style fear exercise under Catalog `Name` `Goal Setting & Yearly Planner`. Fear Setting Database is owner-manual. An Agent reads a row only when the owner asked. An Agent MUST NOT create a row unless the owner asked.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Fear Setting Database                                       |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936813297f4e675e72f45fd` |
| Surface           | Catalog `Name` `Goal Setting & Yearly Planner`              |
| Title property    | `I'm afraid of...`                                          |

```sql
SELECT "I'm afraid of...", url FROM "collection://316919d4-1936-8112-8cd7-000bb445053e"
```

## Writable properties an Agent may set

| Property           | Type  | Fill rule                          |
| ------------------ | ----- | ---------------------------------- |
| `I'm afraid of...` | title | Fear statement in owner language.  |
| `Define.`          | text  | What the fear is.                  |
| `Prevent.`         | text  | How to prevent the outcome.        |
| `Repair.`          | text  | How to repair the outcome.         |
| `Benefits.`        | text  | Benefits of attempting the action. |
| `Costs.`           | text  | Cost of inaction.                  |

All six property names include the trailing period shown above, except the title property.
