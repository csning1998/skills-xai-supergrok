---
name: skill-module-yt-dlp
effort: low
description: >
    Execute yt-dlp list or download from a JSON object a layer already
    filled. Use when a skill- hands off that JSON, or when the user
    runs /skill-module-yt-dlp.
metadata:
    short-description: "Execute yt-dlp from JSON"
---

# Module yt-dlp

## When to Use

A layer already chose `mode`, `url`, and `outdir`. This module only runs `yt-dlp`.

## Input Requirements

JSON from the calling layer.

```json
{
    "mode": "list",
    "url": "https://www.youtube.com/watch?v=ID",
    "outdir": "~/Videos",
    "playlist_end": 20,
    "dateafter": null,
    "archive_path": null
}
```

`outdir` is required when `mode` is `download`. `playlist_end`, `dateafter`, and `archive_path` may be `null`.

## Process

1. Refuse the call when `mode` or `url` is missing. Return `ok` false.
2. For `list`, map the JSON onto `yt-dlp --flat-playlist --no-download`. Drop `--flat-playlist` and `--playlist-end` when `playlist_end` is null.
3. For `download`, map `outdir` and `url` onto `yt-dlp -P`. Pass `--download-archive` only when `archive_path` is not null. Do not pass `--no-embed-metadata`.
4. Delete a sidecar `.info.json` if one appears.
5. Return JSON. Do not choose a new URL.

```bash
yt-dlp --flat-playlist --no-download \
  --playlist-end "<playlist_end>" \
  --print "%(upload_date)s\t%(title)s\t%(uploader)s\t%(id)s\t%(webpage_url)s\t%(duration)s" \
  "<url>"
```

```bash
yt-dlp \
  -P "<outdir>" \
  --no-overwrites \
  --download-archive "<archive_path>" \
  "<url>"
```

## Output

Artifact `YtDlpResult`.

```json
{
    "ok": true,
    "error": null,
    "mode": "download",
    "media_path": "~/Videos/file.mp4",
    "watch_url": "https://www.youtube.com/watch?v=ID",
    "rows": [
        {
            "upload_date": "20260814",
            "title": "title",
            "uploader": "channel",
            "id": "ID",
            "webpage_url": "https://www.youtube.com/watch?v=ID",
            "duration": 1800
        }
    ]
}
```

`rows` is filled on `list`. `media_path` and `watch_url` are filled on `download`.

## Validation Checklist

- [ ] No field was invented that the input JSON omitted
- [ ] `.info.json` is absent after download
- [ ] `ok` is false when the process exits nonzero

## Backtrack Triggers

- `yt-dlp` missing or not authenticated for the site: return the error JSON. The layer stops.
- Channel URL received with `mode` `download`: return `ok` false. The layer must pass a watch URL.

## Example

Layer sends `{"mode":"download","url":"https://youtu.be/ID","outdir":"~/Videos"}`. Module returns `YtDlpResult` with `media_path`.
