# Areas

Area is a standing life domain in the PARA sense. Area does not have an end date. Project and Goal may point at Area. Area `TOP OF MIND` exists in the schema and stays owner-manual.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Areas                                                       |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936811ea19bf8b7c3826985` |
| Surface           | Catalog `Name` `Life Areas`                                 |
| Title property    | `Life Area`                                                 |

```sql
SELECT "Life Area", url, Archive FROM "collection://316919d4-1936-8195-930e-000bdd2a7bb9"
```

## Life Area values in use

Live `Life Area` titles:

- `Academic Excellence`
- `Career Development`
- `Content Creation`
- `Environment: House & Room`
- `Family & Social`
- `Finances`
- `Fun & Hobbies`
- `Personal Development`
- `Physical Health & Fitness`
- `Miscellaneous`
- `TOP OF MIND`

## Writable properties an Agent may set

| Property          | Type     | Fill rule                                                               |
| ----------------- | -------- | ----------------------------------------------------------------------- |
| `Life Area`       | title    | Do not invent a new Area name unless the owner asked to create an Area. |
| `Archive`         | checkbox | Leave `__NO__` or empty for a live Area.                                |
| `Related Goal`    | relation | Prefer writing the link on the Goal page.                               |
| `Related Project` | relation | Prefer writing the link on the Project page.                            |
| `Related Task`    | relation | Prefer writing the link on the Task page.                               |
| `Related Note`    | relation | Prefer writing the link on the Note page.                               |
| `Related Budget`  | relation | Monthly Budget that belongs to the Area.                                |

`Source` lists import origins such as Google Calendar and Google Tasks. Leave `Source` empty unless the owner is recording an import.

## Do not write

Area `TOP OF MIND` assignment. Formula and rollup properties including `Area Report`, `Live Projects Count`, `Completed Goals Count`.
