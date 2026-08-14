# Installments

Installments is a multi-period commitment definition. Monthly instances land in Fixed Expenditure.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Installments                                                |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/319919d4193680cda283e5b1781a3f88` |
| Title property    | `Expenditure Title`                                         |

## Writable properties an Agent may set

| Property                     | Type     | Fill rule                                                          |
| ---------------------------- | -------- | ------------------------------------------------------------------ |
| `Expenditure Title`          | title    | Commitment name.                                                   |
| `Status`                     | status   | One of `Not Started`, `Live`, `Repaid`.                            |
| `Frequency`                  | select   | One of `Monthly`, `Yearly`, `Bi-Monthly`, `Half Year`.             |
| `Monthly Cost`               | number   | New Taiwan Dollar.                                                 |
| `Period on First Deduct`     | number   | Periods remaining or scheduled on first deduct. Copy a nearby row. |
| `First Deduct Date`          | date     | Expanded keys.                                                     |
| `Settlement Date`            | date     | Expanded keys.                                                     |
| `Related Financial Category` | relation | Limit 1. Required.                                                 |
| `Related Fiscal Year`        | relation | Matching Fiscal Years page.                                        |
| `Service Link`               | url      | Optional.                                                          |
| `Notes`                      | text     | Owner language only.                                               |

## Do not write

Formula properties including `Remaining Payment`, `Final Payment Date`, `Jar`.
