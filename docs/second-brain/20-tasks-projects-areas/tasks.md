# Tasks

Task is the executable next action. Task MUST set `Related Goal`. Task MAY leave `Related Project` empty.

## Locate

| Item                 | Value                                                         |
| -------------------- | ------------------------------------------------------------- |
| Data source title    | Tasks                                                         |
| Data source ID       | see `../03-identifiers.md`                                    |
| Database page        | `https://app.notion.com/p/316919d4193681cea4e9d4e08623bd61`   |
| Surfaces             | Catalog `Name` `Inbox`, Catalog `Name` `Tasks & Action View`  |
| Default template URL | `https://app.notion.com/p/316919d4193681a1a1aeff1f5bfde635`   |
| Listed page template | Live name is `[To-do] New Inbox Task` plus one trailing space |
| Icon string          | `:icons_notion_tick-tasks:`                                   |

Find a GitLab linked Task by `iid` token.

```sql
SELECT Name, url, Status FROM "collection://316919d4-1936-81e5-b1af-000b95494b22"
WHERE Name LIKE '%!123%' OR Name LIKE '%#123%'
```

A match needs both an `!<iid>` or `#<iid>` token at a digit boundary and the first four significant words of the merge request title.

## Name formats

| Situation                   | `Name` value                                                   |
| --------------------------- | -------------------------------------------------------------- |
| Merged GitLab merge request | `[**{title} !{iid}**]({web_url})`                              |
| Ordinary Task               | Owner wording. Existing inbox rows often start with `[To-do]`. |

## Writable properties an Agent may set

| Property              | Type         | Fill rule                                                                                                                                                                                                                                                                                          |
| --------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Name`                | title        | See Name formats.                                                                                                                                                                                                                                                                                  |
| `Description`         | text         | First paragraph after `## Summary` or `## Description` in the source body. Normalize `\r\n` to `\n` before splitting. Reject a bare heading such as `## Changes`.                                                                                                                                  |
| `content`             | page body    | Full source body. Rewrite any sentence that contains `{{`, `}}`, or `%{`.                                                                                                                                                                                                                          |
| `Status`              | status       | One of `Inbox`, `Someday / Maybe`, `Not Started`, `In Progress`, `Recurring Today`, `Paused`, `Done`, `Abandoned`. Use `Done` for a completed merge request.                                                                                                                                       |
| `Important`           | checkbox     | `__YES__` when the owner marked the Task important, or when filing a completed merge request in the established sync format.                                                                                                                                                                       |
| `isTaskComplete`      | checkbox     | `__YES__` when `Status` is `Done`.                                                                                                                                                                                                                                                                 |
| `Assignee`            | person       | Owner user ID from `../03-identifiers.md`.                                                                                                                                                                                                                                                         |
| `Context`             | multi_select | Completed computer work uses `HIGH STANIMA` and `Computer`. Other values are `Medium STANIMA`, `LOW STANIMA`, `Phone`, `Email`, `Home`, `On Desk`, `In School`, `In Office`, `Outside`, `Commute`.                                                                                                 |
| `Related Goal`        | relation     | Required. Goal page URL. Default for on-premise platform work is the Goal titled `[G][Coding] Build a On-premise Platform`.                                                                                                                                                                        |
| `Related Project`     | relation     | Optional. Set only when the Task belongs to a named Project bundle.                                                                                                                                                                                                                                |
| `Related Area`        | relation     | Optional. Do not set Area `TOP OF MIND`.                                                                                                                                                                                                                                                           |
| `Related Parent Task` | relation     | Set only when the new Task is a child of an existing Task.                                                                                                                                                                                                                                         |
| `Related Blocker`     | relation     | Task that must finish first.                                                                                                                                                                                                                                                                       |
| `Related Blockee`     | relation     | Task that waits on the current Task.                                                                                                                                                                                                                                                               |
| `userDefined:URL`     | url          | External URL such as a merge request `web_url`.                                                                                                                                                                                                                                                    |
| `Daily Priority`      | select       | One of `Quick & 1st`, `1` through `7`, `Recurring Today`. Leave empty unless the owner ranked the day.                                                                                                                                                                                             |
| `Deadline Date`       | date         | Expanded keys.                                                                                                                                                                                                                                                                                     |
| `Do Dates`            | date         | When two or more Task pages for the same Project land on the same Asia/Taipei calendar date, set `date:Do Dates:start` to `{date}T13:00:00+08:00` and `date:Do Dates:is_datetime` to `1`. Omit Do Dates when the Task is the only Task for the clustered Project on the Asia/Taipei calendar date. |
| `Started At`          | date         | Same clustering rule as Do Dates.                                                                                                                                                                                                                                                                  |
| `Completed At`        | date         | Convert source timestamp to Asia/Taipei. Example `2026-08-06T17:34:38+08:00`. Do not write the raw UTC value. Do not label the value `UTC+8`.                                                                                                                                                      |
| `icon`                | icon         | `:icons_notion_tick-tasks:`                                                                                                                                                                                                                                                                        |

## Status groups

- Complete group contains `Done` and `Abandoned`.
- In progress group contains `In Progress`, `Recurring Today`, and `Paused`.
- To do group contains `Inbox`, `Someday / Maybe`, and `Not Started`.

## Do not write

Formula, rollup, and button properties including `Net Minutes`, `Task Report`, `Process`, `Start / Pause`, `Completed`, `Incubate`, and every `notAvailableInQuerySql` column.

Do not substitute a schema-level S3 URL for `icon`. The schema icon hash `61491cd7-...` rendered blank.

## Create call

Parent is `{"type": "data_source_id", "data_source_id": "<Tasks UUID in 03-identifiers.md>"}`. Keep a batch near four pages.
