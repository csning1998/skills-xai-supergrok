# Wish List

Wish List is an intention. Wish List is not a ledger event. Wish List and ledger events are disjoint.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Wish List                                                   |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d419368193926bfa9a977b0acb` |
| Surface           | Catalog `Name` `Wish List`                                  |
| Title property    | `Item`                                                      |

## Writable properties an Agent may set

| Property             | Type         | Fill rule                                                       |
| -------------------- | ------------ | --------------------------------------------------------------- |
| `Item`               | title        | Desired item.                                                   |
| `Price`              | number       | New Taiwan Dollar.                                              |
| `List Selected`      | multi_select | Zero or more of `Electronics`, `Art and Designs`, `Equipments`. |
| `Shop / Source`      | select       | One of `PCHome`, `Other Online Store`, `Vacpack Official`.      |
| `userDefined:URL`    | url          | Optional product URL.                                           |
| `Purchased`          | checkbox     | `__YES__` only after the owner confirmed purchase.              |
| `Purchased Datetime` | date         | Set only when Purchased is `__YES__`.                           |

Do not convert a Wish List row into Income or Flexible Expenditure unless the owner asked to book the cashflow.
