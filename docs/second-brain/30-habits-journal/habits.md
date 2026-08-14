# Habits

Habits is a recurring behaviour with Trigger, Action, Frequency, and Unit. Days is the daily log for Habits.

## Locate

| Item              | Value                                                       |
| ----------------- | ----------------------------------------------------------- |
| Data source title | Habits                                                      |
| Data source ID    | see `../03-identifiers.md`                                  |
| Database page     | `https://app.notion.com/p/316919d41936814fae0cec76cf5bd3bc` |
| Surface           | Catalog `Name` `Habit Tracker`                              |
| Title property    | `Name`                                                      |

## Writable properties an Agent may set

| Property            | Type     | Fill rule                                                              |
| ------------------- | -------- | ---------------------------------------------------------------------- |
| `Name`              | title    | Habit name in owner language.                                          |
| `Trigger`           | text     | Cue that starts the Habit.                                             |
| `Action`            | text     | Behaviour to perform.                                                  |
| `Frequency`         | number   | Count per Unit.                                                        |
| `Unit`              | select   | One of `Day`, `Week`, `Month`, `Quarter`.                              |
| `Start Date`        | date     | Expanded keys.                                                         |
| `End Date`          | date     | Expanded keys. Optional.                                               |
| `Related Goal`      | relation | Goal that the Habit supports.                                          |
| `Related Year`      | relation | Years page covering the Habit.                                         |
| `Related Daily Log` | relation | Days rows where the Habit was logged. Prefer writing the link on Days. |
| `Last Attempted`    | date     | Set when the owner marked achieved or failed.                          |
| `Log Updated`       | date     | Last daily log write.                                                  |
| `Archive`           | checkbox | `__YES__` only when the owner retired the Habit.                       |

## Do not write

Formula and button properties including `Habit Report`, `Achieve`, `Due Today`, `Next Due`, `% Progress`.
