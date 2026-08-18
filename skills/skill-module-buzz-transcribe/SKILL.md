---
name: skill-module-buzz-transcribe
effort: low
description: >
    Execute one Buzz Flatpak add or a CUDA probe from a JSON object a
    layer already filled. Use when a skill- hands off that JSON, or
    when the user runs /skill-module-buzz-transcribe.
metadata:
    short-description: "Execute Buzz from JSON"
---

# Module Buzz transcribe

## When to Use

A layer already chose `media_path`, model, and language, or asked for a CUDA probe.

## Input Requirements

JSON from the calling layer.

```json
{
    "op": "add",
    "media_path": "~/Videos/file.mp4",
    "model_type": "whisper",
    "model_size": "medium",
    "language": "zh",
    "extract_speech": "no"
}
```

`op` is `probe` or `add`. For `probe`, the other keys may be omitted.

## Process

1. For `probe`, run the Flatpak Python one-liner and return `cuda_available` plus `device_name`.
2. For `add`, map the JSON onto `buzz add`. Add `--extract-speech` only when `extract_speech` is `yes`.
3. Pass exactly one `media_path`. Do not run `buzz --help`.
4. Return the sibling `.txt` path and the exit code.

```bash
flatpak run --command=python3 io.github.chidiwilliams.Buzz -c \
  'import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")'
```

```bash
flatpak run io.github.chidiwilliams.Buzz add \
  --task transcribe \
  --model-type "<model_type>" \
  --model-size "<model_size>" \
  --language "<language>" \
  --txt \
  --hide-gui \
  "<media_path>"
```

## Output

Artifact `BuzzResult`.

```json
{
    "ok": true,
    "error": null,
    "op": "add",
    "cuda_available": true,
    "device_name": "NVIDIA GeForce RTX 4070",
    "transcript_path": "~/Videos/[Transcript] file.txt",
    "exit_code": 0
}
```

## Validation Checklist

- [ ] Model size and language match the input JSON
- [ ] `ok` is false when `exit_code` is not 0
- [ ] No fallback transcoder was started

## Backtrack Triggers

- Exit 134: return `ok` false with that code. The layer decides whether to retry.
- CUDA probe printed `False`: return `cuda_available` false. The layer stops the add.

## Example

Layer sends `{"op":"probe"}` then `{"op":"add","media_path":"...","model_type":"whisper","model_size":"medium","language":"zh","extract_speech":"no"}`.
