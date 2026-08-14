# Weights Log

Weights Log is one weight exercise sample under a Workout Session.

## Locate

| Item              | Value                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------- |
| Data source title | Weights Log                                                                                       |
| Data source ID    | see `../03-identifiers.md`                                                                        |
| Database page     | `https://app.notion.com/p/316919d41936817eaaf1d01584426c41`                                       |
| Surface           | Catalog `Name` `Workout Tracker`                                                                  |
| Title property    | `Exercise`                                                                                        |
| Templates         | Triceps, Bench Press, Bicep Curls, Pull Downs, Deadlifts, Leg Press, Squats, Calve Raises, Situps |

```sql
SELECT Exercise, Weight, Sets, Reps, url FROM "collection://316919d4-1936-8175-844c-000b3eac1557"
```

## Writable properties an Agent may set

| Property                  | Type     | Fill rule                                                     |
| ------------------------- | -------- | ------------------------------------------------------------- |
| `Exercise`                | title    | Exercise name. Copy a template title when the owner used one. |
| `Date`                    | date     | Expanded keys.                                                |
| `Weight`                  | number   | Load used.                                                    |
| `Sets`                    | number   | Set count.                                                    |
| `Reps`                    | number   | Repetition count.                                             |
| `Related Workout Session` | relation | Workout Sessions page for this sample.                        |
| `Related Fitness Record`  | relation | Optional aggregate.                                           |

## Do not write

Formula property `Exercise Report`.
