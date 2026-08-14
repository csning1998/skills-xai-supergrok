# Contacts

Contacts is a person record. Income and Flexible Expenditure may point at Contacts. Create a Contacts row only when the owner asked.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Contacts                                                    |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681128c97d1faca08a153` |
| Surface           | Catalog `Name` `Contacts`                                   |
| Title property    | `Name`                                                      |
| Templates         | New Work Contact TEMPLATE, New Personal Contact TEMPLATE    |

```sql
SELECT Name, "Contact Type", Status, url FROM "collection://316919d4-1936-814d-b8fc-000ba3f05e8b"
WHERE Name LIKE '%Ning%'
```

## Writable properties an Agent may set

| Property                       | Type         | Fill rule                                                             |
| ------------------------------ | ------------ | --------------------------------------------------------------------- |
| `Name`                         | title        | Person or organization name.                                          |
| `Contact Type`                 | select       | One of `Lead`, `Personal`, `Work`, `Tutor`.                           |
| `Status`                       | status       | One of `Inbox`, `Live`, `Archived`. Use `Live` for an active contact. |
| `Primary Contact`              | text         | Primary handle already used nearby.                                   |
| `Secondary Contact`            | text         | Optional.                                                             |
| `Email 1`                      | email        | Optional.                                                             |
| `Email 2`                      | email        | Optional.                                                             |
| `Phone`                        | phone_number | Optional.                                                             |
| `Address`                      | text         | Optional.                                                             |
| `Tax ID`                       | text         | Optional.                                                             |
| `URL 1`                        | url          | Optional.                                                             |
| `URL 2`                        | url          | Optional.                                                             |
| `Instagram`                    | url          | Optional.                                                             |
| `Twitter`                      | url          | Optional.                                                             |
| `First Connected`              | date         | Expanded keys.                                                        |
| `First Message`                | text         | Owner language only.                                                  |
| `Related Project`              | relation     | Optional.                                                             |
| `Related Note`                 | relation     | Optional.                                                             |
| `Related Income`               | relation     | Prefer writing the link on Income.                                    |
| `Related Flexible Expenditure` | relation     | Prefer writing the link on Flexible Expenditure.                      |
| `Archive`                      | checkbox     | Leave empty unless the owner archived the contact.                    |

Leave `Files` empty unless the owner supplied a file.

## Do not write

Button `Add To System`.
