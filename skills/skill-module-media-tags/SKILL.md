---
name: skill-module-media-tags
effort: low
description: >
    Read ffprobe format tags from a JSON media_path and return raw
    keys as JSON. Use when a layer needs sibling tags, or when the
    user runs /skill-module-media-tags.
metadata:
    short-description: "Read ffprobe tags as JSON"
---

# Module media tags

## When to Use

A layer already has a local media path and needs raw tags.

## Input Requirements

```json
{
    "media_path": "~/Videos/file.mp4"
}
```

## Process

1. Run ffprobe on `media_path`.
2. Return the printed keys as JSON. Do not assemble a Resource payload.
3. Do not call `yt-dlp --print` on a local path. Do not read `.info.json`.

```bash
ffprobe -v error -show_entries format_tags=comment,title,artist,date,description,synopsis -of default=noprint_wrappers=1 "<media_path>"
```

## Output

Artifact `MediaTags`.

```json
{
    "ok": true,
    "error": null,
    "media_path": "~/Videos/file.mp4",
    "comment": "https://www.youtube.com/watch?v=ID",
    "title": "video title",
    "artist": "channel name",
    "date": "2026-08-14",
    "description": "youtube description",
    "synopsis": null
}
```

Missing tags are `null`.

## Validation Checklist

- [ ] Every value is copied from ffprobe
- [ ] Title or Author was not composed here

## Backtrack Triggers

- ffprobe exits nonzero: `ok` false. The layer stops payload fill.

## Example

Layer sends `{"media_path":"..."}`. Module returns `MediaTags`.
