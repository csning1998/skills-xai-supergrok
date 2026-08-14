# Cardio Log

Cardio Log is one cardio sample under a Workout Session.

## Locate

| Item              | Value                                                                  |
| ----------------- | ---------------------------------------------------------------------- |
| Data source title | Cardio Log                                                             |
| Data source ID    | see `../03-identifiers.md`                                             |
| Database page     | `https://app.notion.com/p/316919d4193681b093acff62fc6727a1`            |
| Surface           | Catalog `Name` `Workout Tracker`                                       |
| Title property    | `Exercise`                                                             |
| Templates         | Cycling, Run (Outside), Walk / Hike, Run (Treadmill), Elliptical, Swim |

```sql
SELECT Exercise, Distance, Minutes, url FROM "collection://316919d4-1936-8147-8e32-000b6d41570a"
```

## Writable properties an Agent may set

| Property                  | Type     | Fill rule                                                     |
| ------------------------- | -------- | ------------------------------------------------------------- |
| `Exercise`                | title    | Exercise name. Copy a template title when the owner used one. |
| `Date`                    | date     | Expanded keys.                                                |
| `Distance`                | number   | Distance recorded.                                            |
| `Minutes`                 | number   | Duration in minutes.                                          |
| `Related Workout Session` | relation | Limit 1. Workout Sessions page for this sample.               |
| `Related Fitness Record`  | relation | Limit 1. Optional aggregate.                                  |

## Do not write

Formula properties `Pace (m/km)` and `Exercise Report`.
