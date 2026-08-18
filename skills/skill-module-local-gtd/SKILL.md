---
name: skill-module-local-gtd
effort: low
description: >
    Execute mkdir, rename, and mv from JSON paths a layer already
    filled. Use when skill-inspect-google-drive hands off that JSON,
    or when the user runs /skill-module-local-gtd.
metadata:
    short-description: "Execute local mkdir and mv from JSON"
---

# Module local GTD

## When to Use

A layer already chose every destination path.

## Input Requirements

```json
{
    "mkdir_paths": ["~/Documents/[P] x"],
    "rename": null,
    "moves": [
        {
            "from": "~/Downloads/a.pdf",
            "to": "~/Documents/[P] x/a.pdf"
        }
    ]
}
```

`rename` is `null` or `{"from":"...","to":"..."}`.

## Process

1. `mkdir -p` each `mkdir_paths` entry.
2. Run `mv` for `rename` when it is not null.
3. Run `mv` for each `moves` item.
4. Do not choose a project folder.

## Output

Artifact `LocalGtdResult`.

```json
{
    "ok": true,
    "error": null,
    "created": ["~/Documents/[P] x"],
    "moved": ["~/Documents/[P] x/a.pdf"]
}
```

## Validation Checklist

- [ ] Every path came from the input JSON
- [ ] A file the layer omitted was not moved

## Backtrack Triggers

- `mv` fails: `ok` false with the path. The layer reports and stops that item.

## Example

Layer sends filled `mkdir_paths` and `moves`. Module returns the changed paths.
