# Topics

Topics is a Knowledge Base topic tag. Notes, Resources, Journal, Projects, and Areas may hang from Topics. CS Topics is a different data source.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Topics                                                      |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936812088cae5ff8ffcedcd` |
| Surface           | Catalog `Name` `Topics`                                     |
| Title property    | `Title`                                                     |
| Default template  | `https://app.notion.com/p/316919d4193681508733dd95db0889ce` |

```sql
SELECT Title, url FROM "collection://316919d4-1936-811b-a0f3-000bc17b8c49"
WHERE Title LIKE '%Platform%'
```

Do not query CS Topics (`collection://2f8919d4-1936-8138-9e39-000b52d840d5`) when locating a Knowledge Base Topic. Both live titles are `Topics`.

## Writable properties an Agent may set

| Property                | Type     | Fill rule                                                  |
| ----------------------- | -------- | ---------------------------------------------------------- |
| `Title`                 | title    | Topic name already used nearby. Do not invent a duplicate. |
| `userDefined:URL`       | url      | Optional topic URL.                                        |
| `Related Area`          | relation | Optional. Do not set Area `TOP OF MIND`.                   |
| `Related Note`          | relation | Prefer writing the link on Notes.                          |
| `Related Resource`      | relation | Prefer writing the link on Resources.                      |
| `Related Project`       | relation | Optional.                                                  |
| `Related Journal Entry` | relation | Optional.                                                  |
| `Related CS Articles`   | relation | Optional Articles pages.                                   |
| `Archive`               | checkbox | `__YES__` only when the owner retired the Topic.           |

## Do not write

Button `Archive Now`. Rollup and formula properties including `Notes Count`, `Resources Count`, `Projects Count`, `Journal Entries Count`, `Topic Report`.
