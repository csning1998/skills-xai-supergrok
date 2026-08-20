---
name: skill-module-inspect-gitlab-mrs
effort: low
description: >
    Execute glab mr list from a JSON target a layer already filled.
    Use when a skill- hands off that JSON, or when the user runs
    /skill-module-inspect-gitlab-mrs.
metadata:
    short-description: "Execute glab MR list from JSON"
---

# Module inspect GitLab MRs

## When to Use

A layer already chose `target_type`, `target`, and `state`.

## Input Requirements

```json
{
    "target_type": "group",
    "target": "group/path",
    "state": "merged"
}
```

## Process

1. Confirm `glab auth status`.
2. Page `glab mr list` as JSON until a page is empty. Deduplicate by `id`.
3. Keep rows whose `state` equals the input `state`.
4. Map JSON fields only. Do not add `summary_paragraph`.

```bash
glab mr list --group <target> --all --per-page 100 --page 1 --output json
glab mr list -R <target> --all --per-page 100 --page 1 --output json
```

## Output

Artifact `GitlabMrList`.

```json
{
    "ok": true,
    "error": null,
    "records": [
        {
            "id": 1,
            "iid": 1,
            "title": "title",
            "web_url": "https://gitlab.example/group/repo/-/merge_requests/1",
            "merged_at": "2026-08-06T09:34:38Z",
            "description": "body",
            "project": "group/repo"
        }
    ]
}
```

`description` has `\r\n` normalized to `\n`. `project` is `references.full` when present. `iid` is copied from GitLab JSON. It is the project-scoped merge request number in the URL and in `!` references.

## Validation Checklist

- [ ] `summary_paragraph` is absent
- [ ] Timezone conversion was not applied to `merged_at`

## Backtrack Triggers

- `glab` not authenticated: `ok` false. The layer asks the owner to log in.

## Example

Layer sends `{"target_type":"repo","target":"owner/repo","state":"merged"}`.
