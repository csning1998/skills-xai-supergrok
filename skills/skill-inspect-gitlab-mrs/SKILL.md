---
name: skill-inspect-gitlab-mrs
description: >
  Enumerate GitLab merge requests with glab and return a stable field
  contract (iid, title, web_url, merged_at, description, summary
  paragraph). Use when the user asks to inspect, list, or pull GitLab
  MRs, or runs /skill-inspect-gitlab-mrs. Read-only. This is a module;
  the write layer is /skill-sync-gitlab-mrs-to-notion.
metadata:
  short-description: "List GitLab MRs via glab"
---

# Inspect GitLab MRs

Read GitLab merge requests with `glab` and return structured records. Do not create or update Notion pages from this skill.

If the user did not name a group or repository, ask for that target before listing.

## Auth

Confirm `glab` is authenticated with `glab auth status` before any `glab mr list` call.

## Enumerate

Pull MRs in JSON. That JSON already includes the full MR `description` field, so a separate `glab mr view` per MR is unnecessary.

```bash
glab mr list --group <group> --all --per-page 100 --page 1 --output json
glab mr list -R <owner>/<repo> --all --per-page 100 --page 1 --output json
```

Increment `--page` until a page returns an empty array. Merge pages and deduplicate by `id`.

Default filter is `"state": "merged"`. Apply a different state only when the user asked for it.

## Record contract

Keep these fields for every retained MR:

- `id`
- `iid`
- `title`
- `web_url`
- `merged_at` (raw GitLab timestamp; do not convert the timezone here)
- `description` (full body, with `\r\n` normalized to `\n`)
- `project` (use `references.full` when present, otherwise the path GitLab already put on the record)
- `summary_paragraph` (see below)

Do not invent extra fields.

## summary_paragraph

Take the first paragraph after the body's `## Summary` or `## Description` heading, with inline code backticks preserved. If neither heading exists, use the first non-heading paragraph.

Normalize `\r\n` to `\n` before splitting. Several MR bodies use CRLF, and a naive `\n\n` split then fails.

Reject a bare heading such as `## Changes`. The value MUST be a real sentence.

## Report

When this skill is invoked on its own, report the target, the retained count, and a compact table of `iid`, `title`, `merged_at`, and `web_url`. Include `summary_paragraph` only when the user asked for descriptions.
