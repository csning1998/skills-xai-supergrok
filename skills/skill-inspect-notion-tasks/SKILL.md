---
name: skill-inspect-notion-tasks
effort: low
description: >
    Inspect the Failure Managements Notion Tasks database: workspace
    identity, schema, and SQL queries over existing rows. Use when the
    user asks to inspect, query, or look up Notion Tasks, or runs
    /skill-inspect-notion-tasks. Read-only. The write layer is
    /skill-sync-gitlab-mrs-to-notion.
metadata:
    short-description: "Query the Notion Tasks database"
---

# Inspect Notion Tasks

Layer for delivery read on Tasks.

## When to Use

The owner asked to inspect or look up Tasks.

## Input Requirements

- Required: none beyond the ask. Optional filter from the owner.

Call `~/.grok/skills/skill-module-inspect-second-brain/SKILL.md` with `{"object":"Tasks","docs_root":"<home>/.grok/docs/second-brain"}` first.

## Process

1. Take `collection` from `SecondBrainLocate`.
2. Fill the query. Default is `SELECT Name, url FROM "<collection>" LIMIT 100`. GitLab-style scan uses `WHERE Name LIKE '%!%' OR Name LIKE '%#%'`.
3. Call `~/.grok/skills/skill-module-inspect-notion-tasks/SKILL.md` with that JSON.
4. Report row count plus `Name`, `url`, and `iid_tokens`.

## Output

Artifact `NotionTaskRows` (same JSON as the module).

## Validation Checklist

- [ ] Query was filled in this layer
- [ ] No Task page was created

## Backtrack Triggers

- Locate `ok` false: stop.
- Query module `ok` false: stop.

## Example

Owner asks for GitLab-linked Tasks. Layer sends the `LIKE` query.
