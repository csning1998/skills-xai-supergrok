# Weekly Meal Plan

Weekly Meal Plan is one planned meal slot. Recipes attach to Weekly Meal Plan.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Weekly Meal Plan                                            |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681b08b8ed43a1184dbae` |
| Surface           | Catalog `Name` `Meal Planner`                               |
| Title property    | `Name`                                                      |
| Templates         | Breakfast, Lunch, Dinner, Snack                             |

```sql
SELECT Name, Weekday, Setting, url FROM "collection://316919d4-1936-81b8-acfa-000bdb46b54a"
```

## Writable properties an Agent may set

| Property         | Type     | Fill rule                                                                            |
| ---------------- | -------- | ------------------------------------------------------------------------------------ |
| `Name`           | title    | Slot label. Copy a template title when the owner used one.                           |
| `Weekday`        | select   | One of `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`. |
| `Setting`        | select   | One of `Dine-In`, `Dine-Out`.                                                        |
| `Time`           | text     | Time label already used nearby.                                                      |
| `Related Recipe` | relation | Recipes planned for this slot.                                                       |
