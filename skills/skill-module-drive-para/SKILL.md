---
name: skill-module-drive-para
effort: low
description: >
    Execute Drive list and Projects SQL from JSON a layer already
    filled. Use when skill-inspect-google-drive hands off that JSON,
    or when the user runs /skill-module-drive-para.
metadata:
    short-description: "Execute Drive census from JSON"
---

# Module Drive PARA

## When to Use

A layer already filled PARA names and the Projects query.

## Input Requirements

Load `~/.grok/skills/modules/shared/notion-mcp.md`.

```json
{
    "root_names": ["01-Inbox", "02-Projects"],
    "projects_collection": "collection://...",
    "projects_query": "SELECT Name, Status, url FROM \"collection://...\" ORDER BY Status, Name",
    "create_folder_name": null,
    "trash_file_id": null
}
```

## Process

1. Load Drive and Notion MCP tools through `search_tool`.
2. List My Drive root. Return ids for each name in `root_names`.
3. List the Drive Projects folder the layer pointed at.
4. Run `projects_query` against `projects_collection`.
5. Run `create_folder` or `trash_file` only when those keys are not null.
6. Do not classify local files. There is no Drive move tool.

## Output

Artifact `DriveCensus`.

```json
{
    "ok": true,
    "error": null,
    "folders": [{ "name": "02-Projects", "id": "drive-id" }],
    "project_rows": [
        {
            "Name": "[P] x",
            "Status": "Live Project",
            "url": "https://app.notion.com/p/..."
        }
    ]
}
```

## Validation Checklist

- [ ] Join key was not invented
- [ ] A create plus trash sequence was not used as a move

## Backtrack Triggers

- Drive tool missing: `ok` false. The layer reports that limit.

## Example

Layer sends `root_names` and `projects_query`. Module returns `DriveCensus`.
