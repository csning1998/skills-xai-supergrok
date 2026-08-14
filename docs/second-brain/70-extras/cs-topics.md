# CS Topics

CS Topics is the topic tree for Articles. The live data source title is `Topics`. CS Topics is not Knowledge Base Topics.

## Locate

| Item                     | Value                                                       |
| ------------------------ | ----------------------------------------------------------- |
| Data source title        | `Topics`                                                    |
| Object name in this tree | `CS Topics`                                                 |
| Data source ID           | see `../03-identifiers.md`                                  |
| Database page            | `https://app.notion.com/p/2f8919d4193681918b30e787becc8ff7` |
| Title property           | `Main Topic`                                                |
| Default template         | `https://app.notion.com/p/2f8919d41936815ab83ff8c442b929c8` |

```sql
SELECT "Main Topic", url FROM "collection://2f8919d4-1936-8138-9e39-000b52d840d5"
```

Do not query Knowledge Base Topics (`collection://316919d4-1936-811b-a0f3-000bc17b8c49`) when locating a CS Topics page.

## Writable properties an Agent may set

| Property              | Type     | Fill rule                                                                         |
| --------------------- | -------- | --------------------------------------------------------------------------------- |
| `Main Topic`          | title    | Topic name already used nearby. Do not invent a duplicate.                        |
| `Related CS Articles` | relation | Prefer writing the link on Articles.                                              |
| `Related Tasks`       | relation | Articles relation used as a task-style link. Prefer writing the link on Articles. |
| `Blocked by`          | relation | Other CS Topics pages that must finish first.                                     |
| `Blocking`            | relation | Other CS Topics pages that wait on this topic.                                    |
| `Archived`            | checkbox | `__YES__` only when the owner retired the topic.                                  |

## Do not write

Formula and rollup properties including `Project Report` and `# Related Articles`.
