---
name: skill-module-inspect-second-brain
effort: low
description: >
    Read Second Brain locate files for a JSON object name a layer
    already filled. Use when a skill- needs identifiers, or when the
    user runs /skill-module-inspect-second-brain.
metadata:
    short-description: "Read Second Brain from JSON object"
---

# Module inspect Second Brain

## When to Use

A layer already named the Notion entity to locate.

## Input Requirements

```json
{
    "object": "Resources",
    "docs_root": "<second-brain docs root>"
}
```

`docs_root` is filled by the layer. This module does not own a home path.

## Process

Refuse the call when `object` or `docs_root` is missing. Return `ok` false.

Read these files under `docs_root` in order. Do not invent collection IDs. Do not write pages.

1. `00-operating-contract.md`
2. `README.md`
3. `02-master-catalog.md`
4. `01-locate.md`
5. `03-identifiers.md`
6. The entity file for `object`. Open `02-master-catalog.md` to resolve the path.

## Output

Artifact `SecondBrainLocate`.

```json
{
    "ok": true,
    "error": null,
    "object": "Resources",
    "collection": "collection://<from 03-identifiers.md>",
    "data_source_id": "<from 03-identifiers.md>",
    "entity_path": "<docs_root>/<entity file>"
}
```

## Validation Checklist

- [ ] `collection` came from `03-identifiers.md`
- [ ] No YouTube fill table was read from Second Brain

## Backtrack Triggers

- Object absent from the catalog: `ok` false. The layer stops.

## Example

Layer sends `object` and `docs_root`. Module returns `SecondBrainLocate`.
