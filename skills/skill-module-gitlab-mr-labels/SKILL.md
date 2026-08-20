---
name: skill-module-gitlab-mr-labels
effort: low
description: >
    Execute GitLab merge request label list or apply from JSON a layer
    already filled. Use when a skill- hands off that JSON, or when the
    user runs /skill-module-gitlab-mr-labels.
metadata:
    short-description: "Execute GitLab MR label apply from JSON"
---

# Module GitLab MR labels

## When to Use

A layer already filled `mode`, `group`, and `tables`.

## Input Requirements

JSON from the calling layer. Read it from `payload_path` when that key is set.

```json
{
    "mode": "dry-run",
    "group": "group/path",
    "include_subgroups": true,
    "sleep_s": 0.25,
    "only_if_changed": true,
    "allow_clear": false,
    "tables": {}
}
```

`mode` is `dry-run` or `apply`. `tables` is an object the layer filled. This module does not name or invent mapping keys.

## Process

1. Refuse the call when `mode`, `group`, or `tables` is missing. Return `ok` false.
2. Confirm `glab auth status`.
3. Run `scripts/realign.py` with the JSON path. Do not add a mapping that `tables` omitted.
4. Page group merge requests. Compute the label set from `tables` only.
5. For `dry-run`, return the change list. For `apply`, `PUT` each changed merge request and sleep `sleep_s`. Retry HTTP 429.

```bash
python3 scripts/realign.py "<payload_path>"
```

## Output

Artifact `GitlabMrLabelResult`.

```json
{
    "ok": true,
    "error": null,
    "mode": "dry-run",
    "total": 0,
    "noop": 0,
    "changed": 0,
    "applied": 0,
    "failed": [],
    "changes": [
        {
            "project_id": 1,
            "iid": 1,
            "path": "group/repo",
            "title": "title",
            "old": ["feature"],
            "new": ["type::feature"]
        }
    ]
}
```

`applied` is filled on `apply`. `changes` lists every row whose old set differs from the computed set.

## Validation Checklist

- [ ] No mapping was invented that the input JSON omitted
- [ ] Terraform files were not read
- [ ] `ok` is false when `glab` is not authenticated

## Backtrack Triggers

- `glab` not authenticated: `ok` false. The layer asks the owner to log in.
- HTTP 429 exhausted retries: `ok` false and the `failed` list.

## Example

Layer sends `payload_path` with `mode` `dry-run`. Module returns `GitlabMrLabelResult`.
