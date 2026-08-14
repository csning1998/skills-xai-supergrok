---
name: update-antigravity
description: >
  Update Google Antigravity IDE and Antigravity 2.0 Agent Manager on Linux
  from official tarballs on antigravity.google/download. Use when the user
  asks to update Antigravity, upgrade Antigravity IDE, update Agent Manager,
  refresh the Antigravity hub, or runs /update-antigravity.
metadata:
  short-description: "Update Antigravity IDE and Agent Manager"
---

# Update Antigravity

Update the product the user named. If the user says "Antigravity", "both", or "these", update IDE and Agent Manager. Do not update the CLI or SDK unless asked.

Run `scripts/probe.py` first. It prints official Linux x64 URLs plus every detected local install.

```bash
python3 "$HOME/.grok/skills/update-antigravity/scripts/probe.py"
```

Treat `ideVersion` in `product.json` as the IDE version. `antigravity-ide --version` reports the VS Code engine and MUST NOT be used for the upgrade decision.

## Hard rules

- Resolve current tarball URLs from `https://antigravity.google/download` on every run. Do not reuse a version or URL from a previous session.
- Download only official Google hosts (`storage.googleapis.com`, `dl.google.com`, `edgedl.me.gvt1.com`).
- Do not touch user data under `~/.antigravity-ide`, `~/.config/Antigravity IDE`, or `~/.config/Antigravity`.
- Stop a running app by its main PID from `ps -eo pid,ppid,args`. Never use `pgrep -f` or `pkill -f`.
- Replace the install tree that the active launcher actually starts.
- `/opt` replacement needs explicit sudo. If sudo is blocked or a password is required, install the hub under `~/.local/share/antigravity/Antigravity-x64` and point user launchers there.

## Step 1. Decide the target install

### Item A. Antigravity IDE

Typical layout:

- App root: `~/.local/share/antigravity-ide`
- Binary: `$root/antigravity-ide`
- CLI wrapper: `$root/bin/antigravity-ide`
- Version file: `$root/resources/app/product.json` field `ideVersion`
- Archive top directory: `Antigravity IDE/`
- Launcher: `/usr/local/bin/antigravity-ide` usually symlinks to `$root/bin/antigravity-ide`

### Item B. Agent Manager (Antigravity 2.0 hub)

Typical layout:

- User root: `~/.local/share/antigravity/Antigravity-x64`
- System root: `/opt/antigravity/Antigravity-x64`
- Binary: `$root/antigravity`
- Version: `package.json` `version` inside `$root/resources/app.asar`
- Archive top directory: `Antigravity-x64/`
- User launcher: `~/.local/bin/antigravity`
- System launcher: `/usr/local/bin/antigravity`

If both a user-local hub and `/opt` hub exist, update the one that `command -v antigravity` and the user desktop file start. Leave the unused copy unless the user asks to replace it.

## Step 2. Compare versions

Skip a product when the launched install already matches `official.<product>.version`. Otherwise continue.

## Step 3. Download and stage

```bash
mkdir -p /tmp/antigravity-update
curl -fL --retry 3 --retry-delay 2 -o /tmp/antigravity-update/ide.tar.gz "$IDE_URL"
curl -fL --retry 3 --retry-delay 2 -o /tmp/antigravity-update/hub.tar.gz "$HUB_URL"
tar -xzf /tmp/antigravity-update/ide.tar.gz -C /tmp/antigravity-update
tar -xzf /tmp/antigravity-update/hub.tar.gz -C /tmp/antigravity-update
```

Confirm staged versions before replacing anything:

- IDE: staged `resources/app/product.json` `ideVersion`
- Hub: staged asar `package.json` `version` via `scripts/probe.py` logic

If `tar -tzf ... | head` is used, do not combine it with `set -e` in the same script. `head` closes the pipe and can abort the rest of the script with SIGPIPE.

## Step 4. Stop the running app

Find the main PID (the binary with no `--type=` argument). Send `SIGTERM` to that PID, wait up to 20 seconds, then `SIGKILL` only that PID if it remains.

Preserve desktop icons from the old tree before moving it:

- IDE: `$root/resources/icon.png` and `$root/resources/app/resources/linux/antigravity.png`
- Hub: extract `icon.png` from `app.asar` if the staged tree has no `$root/resources/icon.png`

```bash
python3 "$HOME/.grok/skills/update-antigravity/scripts/probe.py" extract-hub-icon \
  "$STAGED/resources/app.asar" "$STAGED/resources/icon.png"
```

## Step 5. Replace

Backup, then move the staged tree onto the live root.

```bash
mv "$ROOT" "$ROOT.bak.$OLD_VERSION"
mv "$STAGED" "$ROOT"
```

After replace:

1. Restore missing icon files used by existing `.desktop` entries. New IDE tarballs often ship only `resources/app/resources/linux/code.png`.
2. Keep the existing symlink path. Recreate `~/.local/bin/antigravity` or `/usr/local/bin/antigravity-ide` only when the symlink is missing.
3. For a user-local hub, set the user desktop `Exec` and `Icon` to the user-local binary and `resources/icon.png`.
4. Match previous `chrome-sandbox` mode on that tree. Do not introduce setuid unless that install already used it.

Do not rewrite `/usr/share/applications` unless the user asked for a system-wide change.

## Step 6. Verify

1. Read the live version the same way as Step 2.
2. Confirm the launched binary path with `readlink -f "$(command -v antigravity-ide)"` or `readlink -f "$(command -v antigravity)"`.
3. Confirm desktop files still exist.
4. Remove `/tmp/antigravity-update`.

Report old version, new version, live path, and backup path. Tell the user to reopen the app from the menu.

## Privileged `/opt` hub

Replacing `/opt/antigravity` is a system mutation. Ask for sudo authorization first. If sudo cannot run, stop changing `/opt` and finish with the user-local hub instead.
