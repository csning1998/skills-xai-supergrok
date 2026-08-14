# KPI Logs

KPI Logs is one timestamped sample for a Key Performance Indices page.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | KPI Logs                                                    |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d419368193a831ecb8b06af3d2` |
| Title property    | `Name`                                                      |
| Template          | Live name is `@Now` plus one trailing space                 |

## Writable properties an Agent may set

| Property      | Type     | Fill rule                                                                                                   |
| ------------- | -------- | ----------------------------------------------------------------------------------------------------------- |
| `Name`        | title    | Short sample label. Copy the live `@Now` template style, including the trailing space in the template name. |
| `Current`     | number   | Measured value.                                                                                             |
| `Logged At`   | date     | Expanded keys. Sample time.                                                                                 |
| `Related KPI` | relation | Required. The Key Performance Indices page being sampled.                                                   |
