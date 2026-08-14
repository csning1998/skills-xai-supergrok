# README for The Repository

This repository's working tree maps directly to `~/.grok`. Grok installation populates `~/.grok` with runtime files, causing `git clone` against this non-empty directory to fail. The setup attaches a Git remote to the existing `~/.grok` directory and checks out `main`.

## Section 1. Clone Repository into Existing Grok Home

### Step A. Prerequisites

1. Grok is installed and initialized via at least one successful login, generating `~/.grok/auth.json`.
2. SSH connectivity to `gitlab.com` is established with read access to `csning1998-lab/personal/skills-xai-supergrok`.
3. Target remote URI is `git@gitlab.com:csning1998-lab/personal/skills-xai-supergrok.git`.
4. Local directory `~/.grok` is not an existing Git repository.

### Step B. Tracked and Untracked Path Behavior

`.gitignore` enforces an allow-list model. Checkout operations mutate only tracked repository paths.

- **Paths Overwritten or Created During Checkout:**
    - `skills/`
    - `docs/second-brain/`
    - `docs/.markdownlint.json`
    - `docs/.mdlrc`
    - `memory/`
    - `terraform/`
    - `.gitlab-ci.yml`
    - `.gitlab/CODEOWNERS`
    - `.gitignore`
    - `tutorial-git-clone.md`
    - `config.toml` (typically exists in pre-installed environments; see Section 1 Step C.3)

- **Paths Preserved During Checkout:**
    - `auth.json`
    - `sessions/`
    - `bin/`
    - `bundled/`
    - `downloads/`
    - `vendor/`
    - `marketplace-cache/`
    - `docs/user-guide/`
    - `logs/`
    - `memtrace/`
    - `.lock` files, temporary caches, and `worktrees.db`

`git checkout -f` force-overwrites tracked local modifications. It does not purge untracked files blocking working tree checkouts.

### Step C. Execution Steps

1. **Verify Grok Directory Context**

    ```bash
    test -d "${HOME}/.grok"
    test -f "${HOME}/.grok/auth.json"
    ```

    Execute subsequent steps only if both commands return exit code `0`.

2. **Initialize Repository and Attach Remote**

    ```bash
    cd "${HOME}/.grok"
    git init --initial-branch=main
    git remote add origin git@gitlab.com:csning1998-lab/personal/skills-xai-supergrok.git
    git fetch origin
    ```

    If `git init` reports an existing repository, inspect state via `git remote -v` and `git status` to verify repository identity before updating the `origin` remote URL.

3. **Resolve `config.toml` Conflict**

    Existing installations contain an untracked `config.toml` that conflicts with the tracked repository file, causing `git checkout` to fail with `untracked working tree files would be overwritten`. Relocate local configuration to permit repository checkout:

    ```bash
    mv config.toml config.toml.local

    ```

    Merge machine-specific UI or model configurations manually from `config.toml.local` into `config.toml` post-checkout. Authentication credentials reside in `auth.json`.

4. **Checkout Branch `main**`

    ```bash
    git checkout -B main origin/main
    git status -sb
    ```

    Verify tracking state indicates `main...origin/main`. Confirm presence of `skills/`, `docs/second-brain/`, `memory/`, and `terraform/`. If untracked file conflicts persist, relocate conflicting paths and re-execute checkout.

5. **Post-Checkout Verification**
    1. Execute `grok` to verify authentication validity.
    2. Terraform operations targeting GitLab projects require local credentials: `~/.vault-token`, `~/.terraform.d/credentials.tfrc.json`, and `~/GitLab/meta-platform/vault/tls/ca.pem`. State is hosted on the GitLab HTTP backend (Project ID: `85419450`).
    3. Do not transfer `auth.json` across hosts.

6. **Prohibited Operations**
    1. Executing `git clone ... ~/.grok` directly against populated `~/.grok`.
    2. Overwriting `~/.grok` with a temporary clone directory containing `sessions/` or `auth.json`.
    3. Relying on `git checkout -f` to clear untracked `config.toml` files.

## Section 2. Terraform Operations

Verify the Bastion Vault instance under `meta-platform` is unsealed. Prior to executing Terraform commands, export HTTP state backend credentials:

```bash
export TF_HTTP_USERNAME='gitlab-ci-token'
export TF_HTTP_PASSWORD=$(VAULT_ADDR='[https://127.0.0.1:8200](https://127.0.0.1:8200)' VAULT_CACERT="/home/csning1998/GitLab/meta-platform/vault/tls/ca.pem" VAULT_TOKEN=$(cat$HOME/.vault-token) vault kv get -field=token secret/meta-platform-credentials/state-backend)
```
