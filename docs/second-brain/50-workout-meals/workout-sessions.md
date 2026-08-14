# Workout Sessions

Workout Sessions is one training session. Weights Log, Cardio Log, and Classes and Sports Log hang from Workout Sessions. Workout Sessions links Days and Years.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Workout Sessions                                            |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d419368148bce3feeb171c8ec4` |
| Surface           | Catalog `Name` `Workout Tracker`                            |
| Title property    | `Session`                                                   |
| Default template  | `https://app.notion.com/p/316919d4193681fc8176fb0e31cdc1f0` |

```sql
SELECT Session, Location, url FROM "collection://316919d4-1936-81fa-aeb8-000b43c877a3"
WHERE Session LIKE '%2026%'
```

## Writable properties an Agent may set

| Property             | Type     | Fill rule                                                                                 |
| -------------------- | -------- | ----------------------------------------------------------------------------------------- |
| `Session`            | title    | Session label already used nearby.                                                        |
| `Date`               | date     | Expanded keys. Calendar date of the session.                                              |
| `Start Time`         | date     | Expanded keys with time.                                                                  |
| `End Time`           | date     | Expanded keys with time.                                                                  |
| `Location`           | select   | One of `Gym - South London`, `Park`, `Yoga Studio - SE London`. Do not invent a location. |
| `Body Weight`        | number   | Body weight recorded for the session.                                                     |
| `Calories`           | number   | Calories recorded for the session.                                                        |
| `Related Day`        | relation | Matching Days page.                                                                       |
| `Related Year`       | relation | Matching Years page.                                                                      |
| `Related Weight Log` | relation | Prefer writing the link on Weights Log.                                                   |
| `Related Cardio Log` | relation | Prefer writing the link on Cardio Log.                                                    |
| `Related Class Log`  | relation | Prefer writing the link on Classes and Sports Log.                                        |

## Do not write

Formula and rollup properties including `Duration`, `Minutes`, `Overview`, `Total Weights`, `Total Cardio`, `Total Classes`.
