---
name: skill-inspect-second-brain
effort: low
description: >
    Read the owner Second Brain documentation under
    ~/.grok/docs/second-brain before locating or filling a Notion page
    in the Failure Managements workspace. Use when the user asks about
    Second Brain structure, Notion filing, Goal Task Project Area
    finance notes, or runs /skill-inspect-second-brain.
metadata:
    short-description: "Load Second Brain docs before Notion work"
---

# Inspect Second Brain

Layer for knowledge locate.

## When to Use

The owner asked about Second Brain structure, or another layer needs identifiers.

## Input Requirements

- Required: the Notion entity name from the owner, or `object` from the calling layer.

## Process

1. Fill `{"object":"<entity>"}`.
2. Call `~/.grok/skills/skill-module-inspect-second-brain/SKILL.md`.
3. Report `SecondBrainLocate`.

## Output

Artifact `SecondBrainLocate` (same JSON as the module).

## Validation Checklist

- [ ] Collection id came from the module JSON
- [ ] No YouTube fill was added

## Backtrack Triggers

- Module `ok` false: stop. The object is not in the catalog.

## Example

Owner asks where Resources live. Layer sends `{"object":"Resources"}`.
