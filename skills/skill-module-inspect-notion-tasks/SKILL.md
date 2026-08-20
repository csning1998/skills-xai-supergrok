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
    "data_source_url": "<from locate>",
    "query": "SELECT Name, url FROM \"<from locate>\" LIMIT 100"
}
```

`data_source_url` and `query` come from the layer. This module does not own a collection ID. If the URL is missing, return `ok` false.

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
            "Name": "title !<iid>",
            "url": "https://app.notion.com/p/...",
            "iid_tokens": ["<iid>"]
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
