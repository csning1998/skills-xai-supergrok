# Recipes

Recipes is a recipe that uses Ingredients and may appear on Weekly Meal Plan.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Recipes                                                     |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d419368161a2e2feac1101a15b` |
| Surface           | Catalog `Name` `Recipe Manager`                             |
| Title property    | `Name`                                                      |
| Default template  | `https://app.notion.com/p/316919d4193681d8819cebbc6bdf39fd` |

```sql
SELECT Name, Category, url FROM "collection://316919d4-1936-8100-997a-000b84a1817c"
```

## Writable properties an Agent may set

| Property                   | Type     | Fill rule                                                                      |
| -------------------------- | -------- | ------------------------------------------------------------------------------ |
| `Name`                     | title    | Recipe name.                                                                   |
| `Category`                 | select   | One of `Dessert`, `Appetizer`, `Main Course`, `Smoothie`, `Condiment`, `Side`. |
| `Difficulty`               | select   | One of Easy, Medium, Hard. Each live option name starts with a leading space.  |
| `Rating`                   | select   | One of `★★★★★`, `★★★★☆`, `★★★☆☆`, `★★☆☆☆`, `★☆☆☆☆`.                            |
| `Prep Minutes`             | number   | Preparation minutes.                                                           |
| `Cook Minutes`             | number   | Cook minutes.                                                                  |
| `Kcal`                     | number   | Calories.                                                                      |
| `Recipe Link`              | url      | Optional source URL.                                                           |
| `Related Ingredient`       | relation | Limit 1 in the live schema. Link the primary Ingredients page.                 |
| `Related Weekly Meal Plan` | relation | Limit 1. Prefer writing the plan link on Weekly Meal Plan.                     |
| `Favourite`                | checkbox | `__YES__` only when the owner starred the recipe.                              |
| `Archive`                  | checkbox | Leave empty unless the owner archived the recipe.                              |

Leave `Cover` empty unless the owner supplied a file.
