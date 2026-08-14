# Fitness Records

Fitness Records is an aggregate view over Weights Log, Cardio Log, and Classes and Sports Log. Prefer writing the sample on the log data source. Create a Fitness Records row only when the owner asked for a new aggregate.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Fitness Records                                             |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936816f8c0ef96da494361d` |
| Surface           | Catalog `Name` `Workout Tracker`                            |
| Title property    | `Name`                                                      |

```sql
SELECT Name, Type, url FROM "collection://316919d4-1936-8185-a5f9-000bc4e2bf59"
```

## Writable properties an Agent may set

| Property                    | Type         | Fill rule                                             |
| --------------------------- | ------------ | ----------------------------------------------------- |
| `Name`                      | title        | Aggregate name already used nearby.                   |
| `Type`                      | multi_select | Zero or more of `Cardio`, `Weights`, `Class / Sport`. |
| `Related Weight Log`        | relation     | Prefer writing the link on Weights Log.               |
| `Related Cardio Log`        | relation     | Prefer writing the link on Cardio Log.                |
| `Related Class & Sport Log` | relation     | Prefer writing the link on Classes and Sports Log.    |

## Do not write

Rollup and formula properties including `Latest Weight`, `Max Weight`, `Latest Cardio`, `Fastest Pace`, `Latest Class`, `Avg Class Duration`, `Overview`.
