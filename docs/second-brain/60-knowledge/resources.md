# Resources

Resource is a web clipping or bibliographic source. An Agent MUST NOT create, edit, or refile a Resource unless the owner asked in the current turn.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Resources                                                   |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936814d83f8d8e1d5c9b544` |
| Surface           | Catalog `Name` `Knowledge Base`                             |
| Title property    | `Title`                                                     |
| Default template  | `https://app.notion.com/p/316919d41936819ab981f17802674ee4` |

```sql
SELECT Title, Type, url FROM "collection://316919d4-1936-8163-bfbf-000bb3d012ce"
WHERE Title LIKE '%Financial%'
```

## Writable properties an Agent may set

Fill the columns below only after the owner asked to write a Resource.

| Property                | Type     | Fill rule                                                                                                                                                                                          |
| ----------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Title`                 | title    | Source title.                                                                                                                                                                                      |
| `Type`                  | select   | One of `Article`, `Documentation`, `Thesis / Dissertation`, `Book`, `GitHub \| GitLab`, `Course`, `Podcast`, `Newsletter`, `Website`, `Video`, `Dataset`, `Textbook`, `Briefing Session`, `Forum`. |
| `userDefined:URL`       | url      | Source URL.                                                                                                                                                                                        |
| `Description`           | text     | Owner language only.                                                                                                                                                                               |
| `Author`                | text     | Source author.                                                                                                                                                                                     |
| `Translator`            | text     | Optional.                                                                                                                                                                                          |
| `Publisher`             | text     | Optional.                                                                                                                                                                                          |
| `ISBN`                  | text     | Optional.                                                                                                                                                                                          |
| `TIOL`                  | text     | Optional owner note.                                                                                                                                                                               |
| `Published`             | date     | Expanded keys.                                                                                                                                                                                     |
| `Completed`             | date     | Expanded keys. Set only when the owner finished the source.                                                                                                                                        |
| `Rating`                | select   | One of `★★★★★`, `★★★★`, `★★★`, `★★`, `★`.                                                                                                                                                          |
| `Related Topic`         | relation | Knowledge Base Topics.                                                                                                                                                                             |
| `Related Note`          | relation | Optional.                                                                                                                                                                                          |
| `Related Notebook`      | relation | Optional.                                                                                                                                                                                          |
| `Related Area`          | relation | Optional. Do not set Area `TOP OF MIND`.                                                                                                                                                           |
| `Related Goal`          | relation | Optional.                                                                                                                                                                                          |
| `Related Project`       | relation | Optional.                                                                                                                                                                                          |
| `Related Journal Entry` | relation | Optional.                                                                                                                                                                                          |
| `Favourites`            | checkbox | Leave empty unless the owner starred the Resource.                                                                                                                                                 |
| `Archive`               | checkbox | Leave empty unless the owner archived the Resource.                                                                                                                                                |

Leave `Author (Notion)` and `AI Summary` empty unless the owner asked.

## Do not write

Button `Archive Now`. Formula and rollup properties including `Resource Report`, `Notes/Refs Count`, `Topic Areas`, `Topic Notebook`.
