# Ingredients

Ingredients is the ingredient master used by Recipes.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Ingredients                                                 |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681e59ea5f7fb1825b2e4` |
| Surface           | Catalog `Name` `Ingredients`                                |
| Title property    | `Name`                                                      |
| Default template  | `https://app.notion.com/p/316919d4193681ba98e2f4d2b289ea1a` |

```sql
SELECT Name, Category, Unit, url FROM "collection://316919d4-1936-81c6-b127-000b4e0ca135"
```

## Writable properties an Agent may set

| Property         | Type     | Fill rule                                                                                                                                          |
| ---------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Name`           | title    | Ingredient name. Do not invent a duplicate of an existing Name.                                                                                    |
| `Category`       | select   | One of `Fruit`, `Meat`, `Fish`, `Red Meat`, `Vegetable`, `Herbs & Spices`, `Dairy`, `Nuts & Seeds`, `Flours & grains`, `Sugars`, `Oils`, `Sauces`. |
| `Unit`           | select   | One of `KG`, `G`, `ML`, `L`, `tbsp`, `items`.                                                                                                      |
| `Amount`         | text     | Quantity text already used nearby.                                                                                                                 |
| `Note`           | text     | Owner language only.                                                                                                                               |
| `Related Recipe` | relation | Recipes that use this ingredient. Prefer writing the primary link on Recipes.                                                                      |
