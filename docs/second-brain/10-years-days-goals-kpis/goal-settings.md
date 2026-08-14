# Goal Settings

Goal Settings is the intake table for a raw Goal statement before a Goals page exists. Goal Settings is not the live Goals data source.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Goal Settings                                               |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d4193681819107cb95e50fa548` |
| Title property    | `Goal`                                                      |

## Writable properties an Agent may set

| Property   | Type     | Fill rule                                                                                         |
| ---------- | -------- | ------------------------------------------------------------------------------------------------- |
| `Goal`     | title    | Draft Goal wording.                                                                               |
| `Prompt`   | select   | Same Prompt options as Goals.                                                                     |
| `Horizon`  | select   | One of `1 Year`, `2 Years`, `3 Years`, `5 Years`, `10 Years`, `12 Years`, `15 Years`, `20 Years`. |
| `Deadline` | date     | Expanded keys.                                                                                    |
| `Priority` | checkbox | `__YES__` only when the owner marked the draft as a priority.                                     |

Promote a Goal Settings row into Goals only when the owner asked to file a live Goal.
