---
name: sync-gitlab-mrs-to-notion
description: >
  Orchestrate inspect-gitlab-mrs and inspect-notion-tasks, then create
  Notion Task pages for merged GitLab MRs that have no matching row.
  Use when the user asks to check, register, or sync GitLab MRs against
  Notion Tasks, or runs /sync-gitlab-mrs-to-notion.
metadata:
  short-description: "Sync merged GitLab MRs into Notion Tasks"
---

# Sync GitLab MRs to Notion

This skill is the write layer. It does not restate GitLab commands or Notion identifiers. Those facts live in the modules.

## Load modules

Before any other step, read both files in full and follow them:

- `/home/csning1998/.grok/skills/inspect-gitlab-mrs/SKILL.md`
- `/home/csning1998/.grok/skills/inspect-notion-tasks/SKILL.md`

Do not copy their identifiers, queries, or `glab` flags into this file.

## Step 1. Collect inputs

1. Run `inspect-gitlab-mrs` for the user-named group or repository. Keep the module's record contract, including `summary_paragraph`.
2. Run `inspect-notion-tasks` with its default GitLab-style registration query. Keep `Name`, `url`, and parsed iid tokens.

If the user only asked to check or compare, stop after Step 2 and print the candidate list. Create pages only when the user asked to register, sync, write, or otherwise create the missing entries.

## Step 2. Match

Exact full-title matching fails. Treat a Notion row as a match only when both conditions hold:

1. The Notion title contains a `#<iid>` or `!<iid>` token at a digit boundary for that MR's `iid`.
2. The first four significant words of the MR title all appear, case-insensitively, in the Notion title.

Any merged MR that fails this rule is a creation candidate. Before trusting a large missing list, spot-check two or three candidates with a direct `LIKE` search on a distinctive title phrase, so a matching-logic error is not treated as a real gap.

## Step 3. Build payloads

Take identifiers, icon, Assignee, Context, Related Goal, and `data_source_id` from `inspect-notion-tasks`. Take MR fields and `summary_paragraph` from `inspect-gitlab-mrs`.

Populate these properties for every page:

- `Name`: `[**{mr_title} !{mr_iid}**]({mr_web_url})`. Existing pages store a markdown link in the title, not a plain string.
- `Description`: the module's `summary_paragraph`.
- `content` (page body): the MR `description`, unmodified except for the template-syntax rewrite below.
- `Status`: `"Done"`.
- `Important`: `"__YES__"`.
- `isTaskComplete`: `"__YES__"`.
- `Assignee`: the Notion user ID from `inspect-notion-tasks`.
- `Context`: the completed-computer-work Context from `inspect-notion-tasks`.
- `userDefined:URL`: the MR `web_url`.
- `Related Goal`: the On-premise Platform Goal URL from `inspect-notion-tasks`, unless the user excluded that project from Goal linkage.
- `date:Completed At:start`: convert `merged_at` to Asia/Taipei (`GMT+8`) and write it with an explicit `+08:00` offset, for example `2026-08-06T17:34:38+08:00`. Do not write the raw UTC value and do not label it `UTC+8`. Convert in Python with `datetime.fromisoformat(...).astimezone(timezone(timedelta(hours=8)))`.
- `date:Completed At:is_datetime`: `1`.
- `icon`: the Task icon string from `inspect-notion-tasks`.

### Dense-day clustering for Do Dates and Started At

Group the MRs being created by `(project, GMT+8 calendar date)`. Use the converted local date, not the UTC date; a merge near UTC midnight can land on a different calendar day.

For any group with two or more MRs, set these on every MR in that group, using a fixed `13:00` local marker (the true work start time is not independently known):

- `date:Do Dates:start`: `{date}T13:00:00+08:00`
- `date:Do Dates:is_datetime`: `1`
- `date:Started At:start`: `{date}T13:00:00+08:00`
- `date:Started At:is_datetime`: `1`

Omit all four properties when the MR is the only one for that project on that GMT+8 date.

## Step 4. Create pages

Load `notion__notion-create-pages` through `search_tool` then `use_tool`. Parent is `{"type": "data_source_id", "data_source_id": "<id from inspect-notion-tasks>"}`.

Keep each batch around four pages so a blocked request is cheap to bisect.

Scan every `content` field for `{{`, `}}`, or `%{` before submit. Rewrite the surrounding sentence in plain prose instead of quoting that template syntax. Those strings match common Server-Side Template Injection signatures and have blocked the Notion connector with an HTML "Sorry, you have been blocked" page. Content is the trigger, not batch size. An 8-item batch and a 4-item batch with the same double-brace text both failed; the 4-item batch succeeded immediately after the pattern was removed.

If a batch returns an HTML block page or otherwise fails before Notion accepts it, query Notion for the affected titles first (a block happens before any write). Then bisect the batch, fix the offending entry, and resubmit.
