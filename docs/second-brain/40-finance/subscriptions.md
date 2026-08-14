# Subscriptions

Subscriptions is the recurring commitment definition. Monthly instances land in Fixed Expenditure.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Subscriptions                                               |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681a1b758f97ac6ed1768` |
| Title property    | `Expenditure Title`                                         |

## Writable properties an Agent may set

| Property                     | Type     | Fill rule                                                           |
| ---------------------------- | -------- | ------------------------------------------------------------------- |
| `Expenditure Title`          | title    | Service name.                                                       |
| `Status`                     | status   | One of `Not Started`, `Live`, `Cancelled`.                          |
| `Frequency`                  | select   | One of `Monthly`, `Yearly`, `Bi-Monthly`, `Half Year`, `Quarterly`. |
| `Unit Payment`               | number   | New Taiwan Dollar per Frequency unit.                               |
| `Start Date`                 | date     | Expanded keys.                                                      |
| `Cancelled Date`             | date     | Set only when Status is `Cancelled`.                                |
| `Related Financial Category` | relation | Limit 1. Required.                                                  |
| `Related Fiscal Year`        | relation | Matching Fiscal Years page.                                         |
| `Service Link`               | url      | Optional vendor URL.                                                |

## Do not write

Formula properties including `Monthly Cost`, `Yearly Cost`, `Jar`, `Next Payment Date`.
