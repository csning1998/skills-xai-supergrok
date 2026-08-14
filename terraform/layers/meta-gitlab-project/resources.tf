
ephemeral "vault_kv_secret_v2" "state_backend" {
  mount = "secret"
  name  = "meta-platform-credentials/state-backend"
}

data "gitlab_group" "personal" {
  full_path = "csning1998-lab/personal"
}

resource "gitlab_project" "this" {
  name             = "skills-xai-supergrok"
  path             = "skills-xai-supergrok"
  description      = "User Grok skills, Second Brain documentation, and harness policy."
  visibility_level = "private"
  namespace_id     = tonumber(data.gitlab_group.personal.id)

  merge_method                             = "ff"
  squash_option                            = "always"
  squash_commit_template                   = "%%{title}"
  only_allow_merge_if_pipeline_succeeds    = true
  remove_source_branch_after_merge         = true
  ci_push_repository_for_job_token_allowed = true
  issues_access_level                      = "enabled"
  wiki_access_level                        = "disabled"
  initialize_with_readme                   = false
  shared_runners_enabled                   = false
}

resource "gitlab_branch_protection" "main" {
  project = gitlab_project.this.id
  branch  = "main"

  allowed_to_push  = [{ access_level = "no one" }]
  allowed_to_merge = [{ access_level = "maintainer" }]

  allow_force_push = false
}
