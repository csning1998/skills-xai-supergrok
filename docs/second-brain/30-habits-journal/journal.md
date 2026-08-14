# Journal

Journal is a reflection entry. The live data source title is `Journal` plus one trailing space. Journal `Type` selects a prompt template such as `Daily Reflection`.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Live title is `Journal` plus one trailing space             |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936818ab597fd83f90cb72d` |
| Surface           | Catalog `Name` `Journal`                                    |
| Title property    | `Name`                                                      |

## Writable properties an Agent may set

| Property          | Type         | Fill rule                                                                                                                                        |
| ----------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Name`            | title        | Entry title.                                                                                                                                     |
| `Type`            | multi_select | One or more template names such as `Just Write!`, `Daily Reflection`, `Thought Dump`, `Weekly Reflection`, `Monthly Reflection`, `Fear Setting`. |
| `Set Date`        | date         | Expanded keys. Entry date.                                                                                                                       |
| `Related Day`     | relation     | Matching Days page.                                                                                                                              |
| `Related Area`    | relation     | Optional. Do not set Area `TOP OF MIND`.                                                                                                         |
| `Related Project` | relation     | Optional.                                                                                                                                        |
| `Related Topic`   | relation     | Optional Knowledge Base Topic.                                                                                                                   |
| `AI Summary`      | text         | Leave empty unless the owner asked to store a summary.                                                                                           |
| `AI Tags`         | multi_select | Existing tag names only. Do not invent a tag.                                                                                                    |
| `Archive`         | checkbox     | Leave empty unless the owner archived the entry.                                                                                                 |

## Do not write

Formula properties including `Date`, `Summary`, `Report`, `Year`.
