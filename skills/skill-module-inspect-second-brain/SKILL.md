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
    "object": "Resources"
}
```

## Process

Read these files in order. Do not invent collection IDs. Do not write pages.

1. `~/.grok/docs/second-brain/00-operating-contract.md`
2. `~/.grok/docs/second-brain/README.md`
3. `~/.grok/docs/second-brain/02-master-catalog.md`
4. `~/.grok/docs/second-brain/01-locate.md`
5. `~/.grok/docs/second-brain/03-identifiers.md`
6. The entity file for `object`. Open `02-master-catalog.md` to resolve the path.

## Output

Artifact `SecondBrainLocate`.

```json
{
    "ok": true,
    "error": null,
    "object": "Resources",
    "collection": "collection://316919d4-1936-8163-bfbf-000bb3d012ce",
    "data_source_id": "316919d4-1936-8163-bfbf-000bb3d012ce",
    "entity_path": "~/.grok/docs/second-brain/60-knowledge/resources.md"
}
```

## Validation Checklist

- [ ] `collection` came from `03-identifiers.md`
- [ ] No YouTube fill table was read from Second Brain

## Backtrack Triggers

- Object absent from the catalog: `ok` false. The layer stops.

## Example

Layer sends `{"object":"Tasks"}`. Module returns the Tasks collection id.
