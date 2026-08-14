# Flexible Expenditure Logs

Flexible Expenditure Logs is one actual spend line under a Flexible Expenditure envelope. This is the daily 記帳 write target.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Flexible Expenditure Logs                                   |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/319919d4193680d0a35ceb048b789a59` |
| Title property    | `Log Entry`                                                 |
| Template          | Live name is `@Now` plus one trailing space                 |

## Writable properties an Agent may set

| Property                       | Type     | Fill rule                                              |
| ------------------------------ | -------- | ------------------------------------------------------ |
| `Log Entry`                    | title    | What was spent.                                        |
| `Amount`                       | number   | Single transaction delta in New Taiwan Dollar.         |
| `Log Time`                     | date     | Expanded keys with time.                               |
| `Related Flexible Expenditure` | relation | Required. Limit 1. The envelope.                       |
| `Related Category`             | relation | Limit 1. Should match the envelope Financial Category. |
| `Related Day`                  | relation | Days page for the spend date.                          |
| `Related Project`              | relation | Optional.                                              |
| `Notes`                        | text     | Owner language only.                                   |
| `Migrated`                     | checkbox | Leave empty for a new row.                             |

## Do not write

Rollup properties `Budget Month` and `Rollup Category`.
