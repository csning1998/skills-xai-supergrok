---
name: skill-module-inspect-notion-tasks
effort: low
description: >
    Execute Tasks SQL from a JSON query a layer already filled. Use
    when a skill- hands off that JSON, or when the user runs
    /skill-module-inspect-notion-tasks.
metadata:
    short-description: "Execute Tasks SQL from JSON"
---

# Module inspect Notion Tasks

## When to Use

A layer already filled `data_source_url` and `query`.

## Input Requirements

Load `~/.grok/skills/modules/shared/notion-mcp.md`.

```json
{
    "data_source_url": "collection://316919d4-1936-81e5-b1af-000b95494b22",
    "query": "SELECT Name, url FROM \"collection://316919d4-1936-81e5-b1af-000b95494b22\" LIMIT 100"
}
```

## Process

1. Call `notion__notion-query-data-sources` with the received URL and query.
2. Page with `LIMIT` / `OFFSET` when a page hits the tool cap.
3. When `Name` is present, add `iid_tokens` parsed from `#<digits>` or `!<digits>`.
4. Do not decide whether a row matches a merge request.

## Output

Artifact `NotionTaskRows`.

```json
{
    "ok": true,
    "error": null,
    "rows": [
        {
            "Name": "title !12",
            "url": "https://app.notion.com/p/...",
            "iid_tokens": ["12"]
        }
    ]
}
```

## Validation Checklist

- [ ] Query text matches the input JSON
- [ ] No Task property was filled for create

## Backtrack Triggers

- `object_not_found`: `ok` false. The layer stops.

## Example

Layer sends a GitLab-style `LIKE` query. Module returns `NotionTaskRows`.
