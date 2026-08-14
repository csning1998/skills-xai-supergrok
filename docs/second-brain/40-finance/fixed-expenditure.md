# Fixed Expenditure

Fixed Expenditure is the monthly instance of a Subscription or an Installment. A Fixed Expenditure row MUST reference Subscription or Installment, and MUST NOT reference both.

## Locate

| Item | Value |
| --- | --- |
| Data source title | Fixed Expenditure |
| Data source ID | see `../03-identifiers.md` |
| Database page | `https://app.notion.com/p/1c347ff8c6e146bbab2feab9a765ae6f` |
| Surface | Catalog `Name` `Fixed Expenditures` |
| Title property | `Expenditure Title` |
| Default template | `https://app.notion.com/p/318919d4193680569c31cc00a142b988` |

```sql
SELECT "Expenditure Title", Status, url FROM "collection://a28876a5-e119-4755-a9f3-c986c49e60c6"
WHERE Status = 'Unpaid'
```

Create a Fixed Expenditure row only when the owner asked to book a committed charge for a specific Monthly Budget.

## Writable properties an Agent may set

| Property | Type | Fill rule |
| --- | --- | --- |
| `Expenditure Title` | title | Charge name. Copy the parent Subscription or Installment title when nearby rows do so. |
| `Status` | status | One of `Unpaid`, `Paid`, `Abandoned`. Use `Unpaid` for a new charge. |
| `Charge Date` | date | Expanded keys. Expected or posted charge date. |
| `Actual Expense` | number | New Taiwan Dollar amount paid. |
| `Related Budget Month` | relation | Required. Monthly Budget for the charge month. |
| `Related Subscription` | relation | Limit 1. Set when the parent is a Subscription. Leave empty when Related Installment is set. |
| `Related Installment` | relation | Limit 1. Set when the parent is an Installment. Leave empty when Related Subscription is set. |
| `Notes` | text | Owner language only. |

Exactly one of Related Subscription or Related Installment MUST be set.

## Do not write

Button `Paid`. Formula and rollup properties including `Source`, `Report`, `Predicted Expense`, `Category`, `Jar`, `Timeframe`, `Subscription Expense`, `Installment Expense`.
