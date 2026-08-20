---
name: skill-sync-gitlab-mrs-to-notion
effort: medium
description: >
    Orchestrate GitLab MR records and Notion Tasks queries, then create
    Notion Task pages for merged GitLab MRs that have no matching row.
    Use when the user asks to check, register, or sync GitLab MRs
    against Notion Tasks, or runs /skill-sync-gitlab-mrs-to-notion.
metadata:
    short-description: "Sync merged GitLab MRs into Notion Tasks"
---

# Sync GitLab MRs to Notion

Layer for delivery write. This file owns Task field fill for a merged MR.

## When to Use

The owner asked to check, register, or sync merged MRs against Tasks.

## Input Requirements

- Required: group or `owner/repo` from the owner.
- Artifacts produced in Process: `GitlabMrList`, `NotionTaskRows`, `SecondBrainLocate` for Tasks.

Read `~/.grok/skills/modules/shared/write-gate.md`.
Read `~/.grok/docs/second-brain/20-tasks-projects-areas/tasks.md` for the match rule and writable properties.

## Process

1. Locate Tasks: `{"object":"Tasks","docs_root":"<home>/.grok/docs/second-brain"}` through `skill-module-inspect-second-brain`.
2. Fill GitLab JSON and call `skill-module-inspect-gitlab-mrs`. Keep `GitlabMrList`.
3. Fill Tasks SQL and call `skill-module-inspect-notion-tasks`. Keep `NotionTaskRows`.
4. If the owner only asked to check or compare, stop after the candidate list.
5. Match with `tasks.md`. Spot-check two or three misses with a `LIKE` phrase.
6. For each missing MR, fill one Task JSON from `tasks.md`. Fill `summary_paragraph` here. Convert `merged_at` to Asia/Taipei with `+08:00` here. Create `/tmp/skill-sync-gitlab-mrs-to-notion/<iid>/` with mode `0700` and write `task-payload.json` there.
7. Create only when the write gate allows it. Send one `payload_path` per Task to `~/.grok/skills/skill-module-file-notion-resources/SKILL.md` with Tasks `data_source_id`. Loop. Keep about four creates in one turn.

## Output

Artifact `TaskFiled`.

```json
{
    "candidates": [{ "iid": 12, "title": "..." }],
    "created": [{ "url": "https://app.notion.com/p/...", "iid": 12 }]
}
```

## Validation Checklist

- [ ] Notion write went through `skill-module-file-notion-resources`
- [ ] `glab` was not called except through its module
- [ ] Create ran only after an ask in this turn

## Backtrack Triggers

- Module `blocked_snippet`: rewrite that `task-payload.json` and resubmit `payload_path`.
- HTML block: query titles first, then bisect the batch.
- Locate or list `ok` false: stop.

## Example

Owner says 「同步這個 group 的 merged MR」. Layer lists, matches, writes one payload file per miss, then loops `payload_path`.
