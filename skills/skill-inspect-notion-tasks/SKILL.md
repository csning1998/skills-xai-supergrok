---
name: skill-inspect-notion-tasks
description: >
  Inspect the Failure Managements Notion Tasks database: workspace
  identity, schema, fixed identifiers, and SQL queries over existing
  rows. Use when the user asks to inspect, query, or look up Notion
  Tasks, or runs /skill-inspect-notion-tasks. Read-only. This is a
  module; the write layer is /skill-sync-gitlab-mrs-to-notion.
metadata:
  short-description: "Query the Notion Tasks database"
---

# Inspect Notion Tasks

Read the Failure Managements Tasks database. Do not create or update pages from this skill.

Use Grok Notion MCP names (`notion__notion-*`) and `search_tool` plus `use_tool`.

## Required tools

Before the first Notion call in a session, call `search_tool` so the live schemas are loaded. A sufficient query is `notion fetch query data sources search`.

Then call these tools through `use_tool`:

- `notion__notion-search`
- `notion__notion-fetch`
- `notion__notion-query-data-sources`

## Fixed identifiers

Reuse these values. Do not rediscover them each run.

- Workspace: Failure Managements (`63b37ef9-7036-4629-8f11-77adb0602ab3`)
- Tasks data source ID: `316919d4-1936-81e5-b1af-000b95494b22`. Use `collection://316919d4-1936-81e5-b1af-000b95494b22` as the SQL table name. Use the bare UUID as `data_source_id` when a caller writes pages.
- Tasks database URL: `https://app.notion.com/p/316919d4193681cea4e9d4e08623bd61`
- Notion user ID for Assignee: `a4a9b51e-80e0-4778-8eaf-842944abd060`
- On-premise Platform Goal page: `https://app.notion.com/p/31a919d419368077a568c76d8757f00b`, titled `[G][Coding] Build a On-premise Platform`
- Task icon: the literal string `:icons_notion_tick-tasks:` (hyphen, not underscore). Custom emoji already uploaded to the workspace (`notion://custom_emoji/63b37ef9-7036-4629-8f11-77adb0602ab3/3b8919d4-1936-80ab-a34c-007a684f3fce`).
- Default page template `[To-do] New Task`: `316919d4-1936-81a1-a1ae-ff1f5bfde635`
- Context for completed computer work: `["HIGH STANIMA", "Computer"]`. `HIGH STANIMA` is the closest existing option to "High Performance".

## Identity and schema

`notion__notion-fetch` with `id: "self"` returns the connected workspace and user.

`notion__notion-fetch` with `id: "collection://316919d4-1936-81e5-b1af-000b95494b22"` returns the Tasks schema. Some properties are listed under `notAvailableInQuerySql`. Do not SELECT those columns.

Date properties are not queryable under their display name. Use the expanded keys (`date:Completed At:start`, `date:Do Dates:start`, `date:Started At:start`, and the matching `:end` / `:is_datetime` keys).

## Query

Call `notion__notion-query-data-sources` with this payload shape:

```json
{
  "data": {
    "data_source_urls": [
      "collection://316919d4-1936-81e5-b1af-000b95494b22"
    ],
    "query": "SELECT Name, url FROM \"collection://316919d4-1936-81e5-b1af-000b95494b22\" LIMIT 100"
  }
}
```

The query tool caps results near 100 rows. If the row count hits that cap, add `ORDER BY Name` and page with `LIMIT` / `OFFSET` until a page returns fewer rows than the limit.

Default scan for GitLab-style registrations:

```sql
SELECT Name, url FROM "collection://316919d4-1936-81e5-b1af-000b95494b22"
WHERE Name LIKE '%!%' OR Name LIKE '%#%'
```

When the user names a different filter, write the SQL they asked for. Keep `Name` and `url` in the SELECT list unless they asked for other columns.

## Title tokens

Existing GitLab-linked titles use a newer `<title> !<iid>` suffix or an older `<title> #<iid>` suffix, sometimes with a `[Code Review]` prefix. A handful of titles paraphrase the MR title.

When this skill is asked for registrations, parse every `Name` for `#<iid>` or `!<iid>` tokens at a digit boundary and return those tokens with the row.

## Icon

Two hash-distinct S3 URLs exist for files that look like `icons_notion_tick_tasks.png`. The schema-level icon (`61491cd7-...`) rendered blank. The file on `[To-do] New Task` is the one that renders. Passing a guessed `:some-name:` value can silently create an empty custom emoji with no API-exposed delete path.

If the confirmed icon ever needs to be rediscovered, fetch a page already known to render correctly and read its `icon` attribute. Do not assume the data-source schema icon is correct. Do not substitute a schema-level S3 URL.

## Report

When this skill is invoked on its own, report the data source, the row count, and a compact table of `Name`, `url`, and parsed iid tokens. Include extra columns only when the user asked for them.
