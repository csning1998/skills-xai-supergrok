# Projects

Project is a work breakdown structure or a bundle of similar Task pages under one Goal. Project is a subset of Goal. A Task page does not have to belong to a Project.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Projects                                                    |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681d784faf08a76859664` |
| Surface           | Catalog `Name` `Projects`                                   |
| Default template  | `https://app.notion.com/p/316919d4193681a0ab42f7bb2349ba1e` |

Observed title prefix is `[P]`, for example `[P] Platform Engineering Migration`.

```sql
SELECT Name, Status, url FROM "collection://316919d4-1936-816b-81cb-000baa220668"
WHERE Name LIKE '%[P]%'
```

## Writable properties an Agent may set

| Property           | Type         | Fill rule                                                                                                                         |
| ------------------ | ------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `Name`             | title        | Keep the `[P]` prefix when the surrounding Projects already use `[P]`.                                                            |
| `Status`           | status       | One of `Draft`, `Inbox`, `Not started`, `Live Project`, `Completed / Archived`, `Deprecated`. Use `Live Project` for active work. |
| `Type`             | multi_select | Zero or more of `Planning`, `Audit`, `Execution`, `Exploratory`.                                                                  |
| `Related Goal`     | relation     | Required when filing a Project. Goal page URL.                                                                                    |
| `Related Task`     | relation     | Prefer writing the link on each Task page through Task `Related Project`.                                                         |
| `Related Area`     | relation     | Area that the Project serves. Do not set Area `TOP OF MIND`.                                                                      |
| `Related Year`     | relation     | Years page covering the Project timeline.                                                                                         |
| `Timeline`         | date         | Expanded keys. Use a range when start and end are both known.                                                                     |
| `Review Interval`  | number       | Days. Copy a nearby live Project when the owner did not specify.                                                                  |
| `Last Review Date` | date         | Set only after an actual review.                                                                                                  |
| `Archived`         | checkbox     | `__YES__` only when the owner retired the Project.                                                                                |
| `Related Blocker`  | relation     | Project that must finish first.                                                                                                   |
| `Related Blockee`  | relation     | Project that waits on the current Project.                                                                                        |
| `Related Note`     | relation     | Optional.                                                                                                                         |
| `Related Contact`  | relation     | Optional.                                                                                                                         |

## Do not write

Buttons `Start Project`, `Complete`, `Save as Draft`, `Add To System`, `Mark Reviewed`. Formula and rollup properties including `Project Report`, `Next Review`, `Review Overdue`, `Net Minutes`, `Goal Area`.
