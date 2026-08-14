# Classes and Sports Log

Classes and Sports Log is one class or sport sample under a Workout Session. The live data source title is `Classes & Sports Log`.

## Locate

| Item              | Value                                                                                         |
| ----------------- | --------------------------------------------------------------------------------------------- |
| Data source title | `Classes & Sports Log`                                                                        |
| Data source ID    | see `../03-identifiers.md`                                                                    |
| Database page     | `https://app.notion.com/p/316919d419368153a66ef8059b1be39e`                                   |
| Surface           | Catalog `Name` `Workout Tracker`                                                              |
| Title property    | `Exercise`                                                                                    |
| Templates         | Yoga Session, HIIT Session, Pilates, Meditation / Restorative, Tennis, Football, Martial Arts |

```sql
SELECT Exercise, Intensity, Minutes, url FROM "collection://316919d4-1936-8147-873f-000bc874be35"
```

## Writable properties an Agent may set

| Property                  | Type     | Fill rule                                                           |
| ------------------------- | -------- | ------------------------------------------------------------------- |
| `Exercise`                | title    | Class or sport name. Copy a template title when the owner used one. |
| `Date`                    | date     | Expanded keys.                                                      |
| `Minutes`                 | number   | Duration in minutes.                                                |
| `Intensity`               | select   | One of `Low`, `Medium`, `High`.                                     |
| `Related Workout Session` | relation | Workout Sessions page for this sample.                              |
| `Related Fitness Record`  | relation | Optional aggregate.                                                 |

## Do not write

Formula property `Exercise Report`.
