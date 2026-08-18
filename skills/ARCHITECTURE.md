# Skills architecture

Read `~/.grok/docs/skill-system/README.md` before editing a skill. Upstream source and the reference list are `~/.grok/docs/skill-system/reference/NOTICE.md`.

A `skill-*` file is a layer. It fills JSON and owns field names. A `skill-module-*` file receives JSON, maps it onto one tool, and returns JSON. Second Brain is the ubiquitous language for Notion entities.

## Section 1. Contract

Every layer and every module uses these sections:

1. When to Use
2. Input Requirements
3. Process
4. Output (named artifact plus JSON)
5. Validation Checklist
6. Backtrack Triggers
7. Example

A later layer consumes a named artifact. It does not reopen an upstream module to recompute a field.

If the Notion API changes, only `skill-module-file-notion-resources` changes. yt-dlp and Buzz modules stay untouched.

## Section 2. Naming

| Kind   | Prefix          | Role                                                 |
| ------ | --------------- | ---------------------------------------------------- |
| Layer  | `skill-`        | Fill JSON. Sequence modules. Own destination fields. |
| Module | `skill-module-` | Execute one tool. Return JSON.                       |

Frontmatter `effort` on each `SKILL.md` is the spawn budget. Roles live in `~/.grok/roles/`. `low` maps to `exec-low`. `medium` maps to `exec-medium`. Do not spawn bare `general-purpose` for those two values.

## Section 3. Contexts

### Item A. Media ingest

- Layers: `skill-yt-dlp`, `skill-buzz-transcribe`, `skill-youtube-to-resources`
- Modules: `skill-module-yt-dlp`, `skill-module-buzz-transcribe`, `skill-module-media-tags`
- Artifacts: `WatchMedia`, `TranscriptDone`, `MediaTags`, `VideoResourcePayload`

`skill-youtube-to-resources` sequences download, transcribe, and Notion write. YouTube fill lives only in that layer.

### Item B. Knowledge filing

- Layers: `skill-inspect-second-brain`, `skill-file-notion-resources`
- Modules: `skill-module-inspect-second-brain`, `skill-module-file-notion-resources`
- Artifacts: `SecondBrainLocate`, `ResourceFiled`, `NotionWriteResult`

### Item C. Delivery

- Layers: `skill-inspect-gitlab-mrs`, `skill-inspect-notion-tasks`, `skill-sync-gitlab-mrs-to-notion`
- Modules: `skill-module-inspect-gitlab-mrs`, `skill-module-inspect-notion-tasks`, `skill-module-file-notion-resources`
- Artifacts: `GitlabMrList`, `NotionTaskRows`, `TaskFiled`

Task fill lives in `skill-sync-gitlab-mrs-to-notion` and `tasks.md`.

### Item D. Workspace

- Layers: `skill-inspect-google-drive`
- Modules: `skill-module-drive-para`, `skill-module-local-gtd`
- Artifacts: `DriveCensus`, `LocalGtdResult`, `WorkspaceCensus`

### Item E. Tooling

- Layers: `skill-update-antigravity`
- Modules: `skill-module-update-antigravity`
- Artifacts: `AntigravityResult`

### Item F. Architecture documents

- Layers: `skill-inspect-architecture-docs`, `skill-update-architecture-docs`
- Modules: `skill-module-inspect-gitlab-mrs`
- Artifacts: `ArchitectureConflictReport`, `ArchitectureDocsUpdated`

Inspect is read-only. Update writes the planning tree after an ask. A merged merge request that the owner asked to archive is handed to `skill-sync-gitlab-mrs-to-notion`. Task fill stays in that layer and `tasks.md`. These layers do not own Terraform DAG, security, test authoring, idempotency, or module-shape review.

## Section 4. Shared kernel

| File                           | Fact                                              |
| ------------------------------ | ------------------------------------------------- |
| `modules/shared/write-gate.md` | A write needs an explicit ask in the current turn |
| `modules/shared/notion-mcp.md` | Notion MCP bootstrap                              |

Collection IDs live in `~/.grok/docs/second-brain/03-identifiers.md`.

## Section 5. After every run

Follow `~/.grok/docs/skill-system/README.md` Section 5. Publish the retrospective. Patch the owning file when a field or flag was wrong.

## Section 6. Adding work

Run The Algorithm in `docs/skill-system/README.md` Section 3 Item A before adding a file.

1. Question the requirement.
2. Delete a step when that removes the need for a new skill.
3. Edit the layer fill table or the module JSON map.
4. Leave Second Brain unchanged unless a Notion entity itself changed.
