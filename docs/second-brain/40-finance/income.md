# Income

Income is a cash inflow event. The live data source title is one leading space plus `Income`.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Live title is one leading space plus `Income`               |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681d7b937db2044f33737` |
| Surface           | Catalog `Name` `Financial Inbox`                            |
| Title property    | `Title`                                                     |

## Writable properties an Agent may set

| Property                 | Type     | Fill rule                                                                                     |
| ------------------------ | -------- | --------------------------------------------------------------------------------------------- |
| `Title`                  | title    | What arrived, in owner language.                                                              |
| `Category`               | select   | One of `Salary`, `Part-Time Income`, `Commission`, `Miscellaneous`, `Allowance`, `Sold Item`. |
| `Budgeted Income`        | number   | Planned New Taiwan Dollar amount.                                                             |
| `Actual Income`          | number   | Received New Taiwan Dollar amount.                                                            |
| `Payment Date`           | date     | Sole receipt timestamp. Invoice dates are not used.                                           |
| `Status`                 | status   | `Pending` or `Received`.                                                                      |
| `Related Monthly Budget` | relation | Required. Exactly one Monthly Budget.                                                         |
| `Related Fiscal Year`    | relation | Matching Fiscal Years page.                                                                   |
| `Related Contact`        | relation | Limit 1. Optional payer.                                                                      |
| `Notes`                  | text     | Owner language only.                                                                          |
