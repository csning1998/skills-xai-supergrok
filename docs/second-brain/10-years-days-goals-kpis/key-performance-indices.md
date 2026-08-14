# Key Performance Indices

Key Performance Indices is a numeric target attached to a Goal. Observed titles use `[KPI]` or `[KPI][Lag]`.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Key Performance Indices                                     |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d419368148b8c4e77005b52bfa` |
| Title property    | `Name`                                                      |

```sql
SELECT Name, Status, url FROM "collection://316919d4-1936-8148-be23-000b61759a1b"
WHERE Name LIKE '%[KPI]%'
```

## Writable properties an Agent may set

| Property                | Type     | Fill rule                                                                                                             |
| ----------------------- | -------- | --------------------------------------------------------------------------------------------------------------------- |
| `Name`                  | title    | Keep the `[KPI]` prefix when nearby rows use `[KPI]`.                                                                 |
| `Status`                | status   | One of `Inbox`, `Staged`, `In Progress`, `Closed`.                                                                    |
| `Related Goal`          | relation | Goal that the KPI measures.                                                                                           |
| `Related Area`          | relation | Optional. Do not set Area `TOP OF MIND`.                                                                              |
| `Object`                | text     | What is being measured.                                                                                               |
| `Spec`                  | text     | Measurement definition in owner language.                                                                             |
| `Start`                 | number   | Starting value.                                                                                                       |
| `Current`               | number   | Latest value. Prefer logging via KPI Logs.                                                                            |
| `Target`                | number   | Target value.                                                                                                         |
| `Unit`                  | select   | One of `USD`, `NTD`, `Occurance`, `Percent`, `GPA`, `Points`, `Index`, `Hours`, `Count`, `Composite`, `MiB`, `Score`. |
| `Metric`                | select   | One of `Accuracy`, `Score`, `Count`, `Duration`, `Cost`, `Latency`, `Availability`, `Other`.                          |
| `Comparator`            | select   | One of `At least (>=)`, `At most (<=)`, `Equal (=)`.                                                                  |
| `Aggregation`           | select   | One of `Last`, `Median`, `Mean`, `Sum`, `Min`, `Max`.                                                                 |
| `Window`                | select   | One of `Attempts`, `Days`, `Weeks`, `Minutes`, `Hours`, `Months`.                                                     |
| `Window Size`           | number   | Size of Window.                                                                                                       |
| `Validity`              | date     | Expanded keys.                                                                                                        |
| `Review Interval`       | number   | Days.                                                                                                                 |
| `Last Review Date`      | date     | Set only after an actual review.                                                                                      |
| `Related Execution Log` | relation | KPI Logs rows. Prefer writing the link on KPI Logs.                                                                   |

## Do not write

Buttons `Enable`, `Completed`, `Marked as Reviewed`. Formula properties including `Progress`, `Next Review`, `Review Overdue`, `KPI Report`.
