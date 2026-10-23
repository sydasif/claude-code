---
description: Compare this machine with its Ansible/dotfiles backup repo, then fix the repo in a separate clone on a branch. **Machine is read-only** — never install, remove, or change anything on the system, and never push or merge without being asked.
argument-hint: [repo-url-or-path]
---

Run a backup audit. Detect the OS first (Linux / macOS / Windows), then proceed. Commands below are Ubuntu/apt-centric; adapt them if the OS differs. Default repo: `https://github.com/sydasif/ansible-ubuntu-setting` (use another if the user names one).

Optional argument `$ARGUMENTS`: repo URL or local path to audit. If empty, use the default repo above.

**Boundaries:** the machine stays read-only and the playbook is never applied to it. Repo edits happen only in a separate clone, on a branch, as local commits. Never put secrets in the repo.

1. **Get the repo** — if a local checkout exists and `git status` is clean, `git pull --ff-only` and use it. If it has uncommitted changes, leave it alone and make a fresh clone. Create a branch `backup-audit/<YYYY-MM-DD>`. Read the repo's own conventions first (`CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `.ansible-lint`, `.yamllint`) and follow them. Locate the dotfiles repo the roles clone (usually `~/.dotfiles`).

2. **Declared state** — read `local.yml`, `group_vars/`, and each role's `tasks/` and `vars/`. Extract apt packages/repos/keys, snaps, flatpaks, pipx/uv/npm/cargo tools, fonts, dconf/GNOME settings, enabled services, groups, Docker `daemon.json` values, symlinked dotfiles, pinned versions and release-specific logic.

3. **Actual state** — collect read-only evidence:
   - `apt-mark showmanual` minus the base install (compare with `/var/log/installer/initial-status.gz`), `/etc/apt/sources.list.d/`, `apt-cache policy`
   - `snap list`, `flatpak list --app`, `pipx list`, `uv tool list`, `npm ls -g --depth=0`, `cargo install --list`, `~/.local/bin`
   - non-default fonts, filtered `dconf dump /`, enabled systemd units (system and user), `id`, `/etc/docker/daemon.json`
   - loose vs. symlinked files in `~` and `~/.config`, `git -C ~/.dotfiles status`, unpushed commits
   - usage evidence (shell history, config/cache mtimes) to tell kept tools from forgotten leftovers

4. **Diff into four buckets**
   - **Add** — on the machine, in use, not in the repo. Name the target role.
   - **Remove** — declared but absent or unused. Remove from the repo only, never from the machine.
   - **Update** — changed versions or repo URLs, GUI settings changed since, packages renamed in newer Ubuntu releases, deprecated modules, stale `group_vars`.
   - **Leave out on purpose** — OS defaults, caches, transient or large data, and **secrets** (SSH private keys, tokens, `.env`, kubeconfigs, password stores). If a secret is already in the repo, flag it as a risk and suggest Ansible Vault; do not copy its value anywhere.

5. **Fix the repo** — in the clone, on the branch:
   - Apply the high-confidence Add/Remove/Update items in the right roles, following existing patterns (tags, vars, handlers, idempotent modules, `creates`/`changed_when` on shell tasks).
   - Do not guess on uncertain items; leave them untouched and list each with the question that would settle it.
   - One small commit per logical change, with a clear message.
   - Update the README (role list, supported Ubuntu versions) and `requirements.txt`/`requirements.yml` if they go stale.
   - Validate before committing: `yamllint ./`, `ansible-lint`, `ansible-playbook local.yml --syntax-check`. Report pre-existing lint failures separately.
   - Never run the playbook on the machine. `--check --diff` only if explicitly asked.
   - Do not push or open a PR unless asked; offer it at the end.

6. **Verdict** — end with:
   - Sync status before the fixes (in sync / slightly drifted / significantly drifted) and what it is now on the branch
   - A table: `| Item | Found where | Action (Add / Remove / Update) | Target role or file | Status (Fixed / Needs your decision) |`
   - Branch name, clone path, commit list, and `git diff --stat` against the base branch
   - **Uncertain** list with the question that resolves each
   - **Do not back up** list (secrets, caches, regenerable data) and any secrets already found in the repo
   - The next step: review the branch, then push or merge it, or ask to have it done
