# Financial Categories

Financial Category is the mutually exclusive dictionary that a ledger event references. Financial Category belongs to Jar.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Financial Categories                                        |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/a0b3a63958d2422ab33b23f73a956085` |
| Title property    | `Financial Categories`                                      |

## Writable properties an Agent may set

| Property               | Type     | Fill rule                                                                  |
| ---------------------- | -------- | -------------------------------------------------------------------------- |
| `Financial Categories` | title    | Stable, mutually exclusive name. Changing the name later distorts history. |
| `Related Jar`          | relation | The Jar that receives the rollup.                                          |
| `Monthly Cap`          | number   | New Taiwan Dollar monthly cap.                                             |
| `Is Fixed Commitment`  | checkbox | `__YES__` when the category is a recurring commitment.                     |
| `Notes`                | text     | Owner language only.                                                       |

## Do not write

LTD interceptors or `Financial Category Report`.
