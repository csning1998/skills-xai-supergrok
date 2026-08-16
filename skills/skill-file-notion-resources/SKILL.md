---
name: skill-file-notion-resources
effort: medium
description: >
  Create Notion Resources pages from a payload the owner picked.
  Use when the user asks to file a source into Resources, ingest a
  YouTube transcript, or runs /skill-file-notion-resources.
  Default is list-only. Creating a page requires an explicit ask
  in the current turn.
metadata:
  short-description: "File picked sources into Notion Resources"
---

# File Notion Resources

Layer for knowledge filing.

## When to Use

The owner asked to file a source and a `payload_path` is already in this turn.

## Input Requirements

- Required: `payload_path` to a `VideoResourcePayload` JSON file, or a bookmark JSON the owner already filled.

Read `~/.grok/skills/modules/shared/write-gate.md`.

Call `~/.grok/skills/skill-module-inspect-second-brain/SKILL.md` with `{"object":"Resources"}`. Take `data_source_id` from that JSON. Do not copy the id into this file.

Do not recompute keys that `payload_path` already holds.

## Process

1. Lookup first. Send `op` `lookup` plus the URL from `payload_path` to `~/.grok/skills/skill-module-file-notion-resources/SKILL.md`.
2. Stop after lookup unless the write gate allows create or update.
3. Fill relations only when the owner named Topic or Area pages. Copy the named Topic's `Related Area`. Do not set `TOP OF MIND`.
4. Send `op` `create` or `update` with `payload_path`. Do not paste payload keys into the module call.

Leave `Related Note`, `Related Goal`, `Related Project`, and `Related Journal Entry` empty unless the owner named those pages. Do not create a Literature Note.

## Output

Artifact `ResourceFiled`.

```json
{
  "url": "https://app.notion.com/p/...",
  "title": "YYYYMMDD video title"
}
```

## Validation Checklist

- [ ] Payload keys were not recomputed when already present
- [ ] Create ran only after an ask in this turn
- [ ] yt-dlp and Buzz were not called from this layer

## Backtrack Triggers

- Lookup already has a row: report that url and skip create. When the owner asked to file in this turn, update that page.
- Module `blocked_snippet`: rewrite the payload file and resubmit `payload_path`.

## Example

Owner says 「灌」 with a `payload_path`. Layer lookups, then sends that path to the Notion module.
