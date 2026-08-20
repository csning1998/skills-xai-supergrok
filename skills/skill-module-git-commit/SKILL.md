---
name: skill-module-git-commit
effort: low
description: >
    Execute or print batched git add and git commit from JSON a layer
    already filled. Never run git push. Use when a skill- hands off
    that JSON, or when the user runs /skill-module-git-commit.
metadata:
    short-description: "Execute or print git commit batches"
---

# Module git commit

## When to Use

A layer already filled `repo_root`, `execute`, and `commits`.

## Input Requirements

JSON from the calling layer. Read it from `payload_path` when that key is set.

```json
{
    "repo_root": "<git toplevel>",
    "execute": false,
    "allow_push": false,
    "header_max": 100,
    "commits": [
        {
            "paths": [".gitignore"],
            "message": "chore(gitignore): track python packaging paths"
        }
    ]
}
```

## Process

1. Refuse the call when `repo_root` or `commits` is missing. Return `ok` false.
2. If `allow_push` is true, return `ok` false. This module does not push.
3. Reject a message that is empty, contains a newline, or is longer than `header_max`.
4. Run `scripts/commit.py` with the JSON path.
5. When `execute` is true, `git add` the listed paths and `git commit` with that header. When `execute` is false, print the equivalent commands and do not change git state.

```bash
python3 scripts/commit.py "<payload_path>"
```

## Output

Artifact `GitCommitResult`.

```json
{
    "ok": true,
    "error": null,
    "execute": false,
    "commands": [
        "git add .gitignore",
        "git commit -m 'chore(gitignore): track python packaging paths'"
    ],
    "committed": []
}
```

`committed` lists hashes when `execute` is true.

## Validation Checklist

- [ ] `git push` is absent from every command
- [ ] Git state is unchanged when `execute` is false
- [ ] `ok` is false when a header exceeds `header_max`

## Backtrack Triggers

- `git commit` nonzero: return `ok` false and the remaining batches.
- Path outside `repo_root`: return `ok` false.

## Example

Layer sends `execute` false. Module prints `git add` and `git commit` lines.
