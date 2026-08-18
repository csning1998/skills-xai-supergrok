# Sub-doc 99. Hook Operating Contract

This file is the complete form of Section 10 in `ENGINEERING_PRINCIPLES.md`. The baseline date is 2026-08-18.

The PreToolUse hook is the only hook event that can deny a tool call. The SessionStart hook creates session state and injects no file. The UserPromptSubmit hook records owner leave phrases and injects no file. The PostToolUse hook on a read records the opened path.

The PreToolUse hook inspects the tool name, the target path, and the text about to be written. The PreToolUse hook does not classify work from the wording of the owner's task. Two different phrasings of the same mutation receive the same decision.

## Section 1. Prerequisite Reading

1. **Trigger Condition**. When the current session will mutate `terraform/`, `ansible/`, or `packer/` under a repository whose name appears in `planning/architecture_<repo>*.md`, or will mutate `planning/` itself, the executing Agent MUST first open `planning/decisions.md` and at least one matching `planning/architecture*.md` with the read-file tool. The file-name convention is `architecture_<repo>_<topic>.md`. A repository whose name does not appear in those file names is outside this gate. When `planning/` contains `architecture.md` and contains no `architecture_<repo>*.md` file, the PreToolUse hook treats every governed path as inside the gate.

2. **Post-read Checklist**. After those reads, and before the first mutation, the executing Agent MUST write four checks. The four checks are the planned move, the planned name, the DAG direction, and whether the mutation sits inside the current task. Completing the four checks only in working memory does not satisfy Section 1 item 2. The PreToolUse hook does not read the written checklist. The PreToolUse hook only records that the files were opened.

3. **Reading Cannot Be Substituted**. A search-result fragment does not count as a read. Context from an earlier session does not count as a read. Inferring content from a file name does not count as a read. The PreToolUse hook counts a path only after the read-file tool opened that path in the current session.

## Section 2. Generic Module Authorization

1. **Authorization Phrase**. A mutation of `terraform/modules/` or `ansible/roles/utils_*` requires one of the following phrases in an owner prompt of the current session. The phrases are `允許改通用模組`, `授權改通用模組`, `你可以改這個通用`, `leave generic module`, and `authorized to edit generic`. The UserPromptSubmit hook records that phrase. A request such as `fix that module` does not record leave.

2. **Still Prohibited After Authorization**. After leave is recorded, the PreToolUse hook still denies a newly added environment alias, a newly added `vault.production` address, a newly added `vault = vault` map, and a newly added product token in a variable name, resource name, tag key, or output key.

3. **Authorization Scope**. Leave applies to the current session. When the owner prompt that carries the leave phrase also names a module path, the PreToolUse hook permits only a path that contains that name. When the owner prompt carries the leave phrase and names no module, the PreToolUse hook permits every generic-module path. Expanding the mutation to a module that the named list does not contain requires a new owner prompt that names that module.

## Section 3. Blocking Rules

### Item A. Blocking Conditions

1. The PreToolUse hook denies a write in each of the following cases.

    1. The target path is inside a repository covered by Section 1, and the current session has not opened the files that Section 1 requires.
    2. The target path is a generic module, and the current session has no leave that covers that path.
    3. The write adds an environment alias (`prod`, `stg`, `dev`) or adds `vault.production` or `vault = vault` inside a generic module.
    4. The write adds a product name to a variable name, resource name, tag key, or output key inside a generic module.
    5. The write adds a `local-exec` provisioner, a `remote-exec` provisioner, an Ansible `shell` or `command` task that lacks `changed_when` or `creates` or `removes`, a guest `psql` or `ALTER USER` command, or a mint (`random_password` or a vault-credential module call) inside a consumer layer.

A pre-existing fragment that already matched a forbidden pattern does not deny a write that only edits other lines. An image tag does not deny a write. A lock-file edit does not deny a write.

2. **Behavior After Blocking**. After a deny, the executing Agent MUST print the rule identifier and the line numbers from the deny reason. The executing Agent MUST NOT rewrite the payload so that the pattern no longer matches while the same action remains. A rewrite of that kind is itself a violation.

3. **Exceptions**. Owner intent for a time-bounded exception MUST be a named entry in `planning/decisions.md`. The named entry MUST state the scope and the end date. A comment in code MUST NOT declare an exception. The PreToolUse hook does not read `planning/decisions.md` for exceptions. The named entry therefore does not disable Item A. A local experiment that must pass Item A requires `ENGINEERING_PRINCIPLES_HOOK=0`.

## Section 4. Disabling

1. **How to Disable**. The owner disables the hook by setting `ENGINEERING_PRINCIPLES_HOOK=0`.

2. **Restrictions on Disabling**. `ENGINEERING_PRINCIPLES_HOOK=0` is allowed only on a local experiment. A CI job and any environment that produces a mergeable change MUST keep the hook enabled. A change produced while the hook is disabled MUST be re-checked with the hook enabled before the change is committed.

## Section 5. Behavioral Requirements for the Executing Agent

1. **Scope Must Not Expand**. The executing Agent MUST mutate only the range that the owner named. When the executing Agent finds a defect outside the named range, the executing Agent MUST report the defect in text and MUST NOT edit the out-of-range defect.

2. **Fact Verification**. Before the executing Agent states a version, a default, a flag name, or a deprecation status, the executing Agent MUST verify that claim. When verification fails, the executing Agent MUST write `目前缺乏足夠的最新資訊` and MUST stop on the unverified claim. The executing Agent MUST NOT fill the gap with a guess. The high-volatility list is Section 2 of `00-loading-protocol.md`.

3. **Rules Must Not Be Self-downgraded**. When a rule and convenience conflict, the executing Agent MUST follow the rule and MUST report the conflict. The executing Agent MUST NOT decide that a clause does not apply to the current case.
