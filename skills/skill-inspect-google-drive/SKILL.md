---
name: skill-inspect-google-drive
effort: medium
description: >
    Census the owner Google Drive PARA tree via MCP, reconcile it with
    Notion Projects and local ~/Downloads (Inbox) plus ~/Documents
    (Projects), and file local files into folders named after Notion
    Project Name. Use when the user asks about Google Drive structure,
    GTD filing, Downloads or Documents classification, creating local
    project folders from Drive, or runs /skill-inspect-google-drive.
    Drive MCP cannot move files. Local mkdir and mv require an explicit
    ask in the current turn.
metadata:
    short-description: "Census Drive PARA and file local GTD"
---

# Inspect Google Drive

Layer for workspace census and local filing.

## When to Use

The owner asked about Drive PARA, Downloads, Documents, or local classify.

## Input Requirements

- Required: the ask in this turn.
- Locate Projects through `skill-module-inspect-second-brain` with `{"object":"Projects","docs_root":"<home>/.grok/docs/second-brain"}`.

Read `~/.grok/skills/modules/shared/write-gate.md`.
Read `~/.grok/docs/second-brain/20-tasks-projects-areas/projects.md`.

## Process

1. Fill Drive census JSON and call `~/.grok/skills/skill-module-drive-para/SKILL.md`.

    ```json
    {
        "root_names": [
            "01-Inbox",
            "02-Projects",
            "03-Resources",
            "04-Archived Projects and Resources",
            "05-Archived Multimedias"
        ],
        "projects_collection": "<from locate>",
        "projects_query": "SELECT Name, Status, url FROM \"<collection>\" ORDER BY Status, Name",
        "create_folder_name": null,
        "trash_file_id": null
    }
    ```

2. List `~/Downloads` and `~/Documents` at depth 1.
3. Report a three-way table: Notion `Name`, Status, local path, Drive `02` folder.
4. Join key is Notion Projects `Name` copied exactly. Remap Drive `[P] Apply for GT OMSCS` to Notion `[P] GT OMSCS Admission Application`.
5. When the write gate allows classify, fill `mkdir_paths`, `rename`, and `moves`, then call `~/.grok/skills/skill-module-local-gtd/SKILL.md`.

Do not precreate folders for `Not started`, `Inbox`, `Draft`, or future `[P][Audit]`. Do not move ISOs, credentials, font caches, `_files` trees, or opaque UUID media. Inbox is `~/Downloads`. Projects is `~/Documents`.

Leave product folders such as `Colab Notebooks` alone.

## Output

Artifact `WorkspaceCensus`.

```json
{
    "rows": [
        {
            "name": "[P] x",
            "status": "Live Project",
            "local_path": "~/Documents/[P] x",
            "drive_folder": "present"
        }
    ],
    "moved": [],
    "left_in_inbox": []
}
```

## Validation Checklist

- [ ] Join key was filled in this layer
- [ ] Local mv ran only after an ask in this turn
- [ ] Drive move was not invented

## Backtrack Triggers

- Two Live projects could claim a file: leave it in Inbox.
- Module `ok` false: report and stop that step.

## Example

Owner asks for a census. Layer calls Drive module and reports the three-way table. Classify waits for an explicit ask.
