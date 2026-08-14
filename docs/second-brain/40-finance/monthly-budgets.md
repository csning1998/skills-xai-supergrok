# Monthly Budgets

Monthly Budget is the smallest reporting container. Every Income Event, Flexible Expenditure, and Fixed Expenditure MUST belong to one Monthly Budget.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Monthly Budgets                                             |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681cab737ce21c78e23e0` |
| Surface           | Catalog `Name` `Monthly Flexible Budgets`                   |
| Title property    | `Budget Month`                                              |

```sql
SELECT "Budget Month", Status, url FROM "collection://316919d4-1936-81aa-8509-000b553707a6"
WHERE Status = 'Live'
```

## Writable properties an Agent may set

| Property              | Type     | Fill rule                                                                   |
| --------------------- | -------- | --------------------------------------------------------------------------- |
| `Budget Month`        | title    | Month label the owner already uses. Copy a nearby row.                      |
| `Status`              | status   | One of `Not started`, `Live`, `Archived`. Use `Live` for the current month. |
| `Timeframe`           | date     | Expanded keys covering the calendar month.                                  |
| `Related Fiscal Year` | relation | Fiscal Years page.                                                          |
| `Related Area`        | relation | Optional. Do not set Area `TOP OF MIND`.                                    |
| `Related Project`     | relation | Optional.                                                                   |
| `Profit Target`       | number   | New Taiwan Dollar. Leave empty unless the owner set a target.               |

Prefer writing ledger links on Income, Flexible Expenditure, and Fixed Expenditure.

## Do not write

Formula or rollup totals such as `Actual Profit/Loss` or `Budget Report`.
