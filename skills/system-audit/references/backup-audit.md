# Backup audit: keep the setup repo true to the machine

A machine drifts away from its Ansible/dotfiles repo over time: tools get installed by hand, old ones are abandoned, settings change in the GUI, and Ubuntu releases deprecate things. This audit compares the **live machine** against the **setup repo**, then **fixes the repo** so it can rebuild the machine as it actually is today.

## Boundaries (different from the other playbooks)

- **The machine stays read-only.** Never install, remove, enable, disable or change anything on the system, and never apply the playbook to it.
- **The repo is yours to fix**, but only in a **separate working clone**, on a **branch**, with **local commits**. Never push, merge, or force anything unless the user says so. Reviewing and pushing is the user's decision.
- Never put secrets in the repo (see "Leave out on purpose").

This playbook is Ubuntu/apt-centric because the user's repo targets Ubuntu desktops. If the OS or package manager differs, adapt the commands but keep the structure.

## 0. Get the repo

Default repo: `https://github.com/sydasif/ansible-ubuntu-setting` (use another if the user names one).

1. If the user already has a local checkout, check `git status`. If it has uncommitted changes, do not touch it; make a separate fresh clone instead. If it is clean, pull before branching: `git pull --ff-only` fails when the current branch has no upstream tracking set (it returns an error instead of fetching). In that case run `git pull origin <branch-name>` or set tracking first with `git branch --set-upstream-to=origin/<branch-name>`, then pull. Only then create the audit branch.
2. Otherwise clone it into a working directory (for example `~/ansible-ubuntu-setting` or `/tmp/`).
3. Create a branch, e.g. `backup-audit/<YYYY-MM-DD>`, and do all edits on it.
4. Read the repo's own conventions before changing anything: `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `.ansible-lint`, `.yamllint`. Follow them (role layout, tags, naming, idempotency, lint rules).
5. Locate the dotfiles repo the roles clone (usually `~/.dotfiles`) and treat it the same way if it needs changes.

## 1. Build the declared state (what the repo says)

Read `local.yml`, `group_vars/`, and each role's `tasks/` and `vars/main.yml`. Extract per role:
- apt packages, apt repos and keys, snaps, flatpaks, pipx/uv/pip tools, npm/cargo globals
- fonts, dconf/GNOME settings, default apps (e.g. default terminal)
- services enabled, user groups, Docker `daemon.json` values, storage paths
- the dotfiles that get symlinked into `~`
- pinned versions and Ubuntu-release-specific logic
- README.md "Supported Ubuntu versions" against `lsb_release` — a mismatch is an Update candidate (the repo may claim a newer release than the machine has, or vice versa).

## 2. Build the actual state (what the machine has)

Collect read-only evidence:
- **apt**: `apt-mark showmanual` (hand-installed set) minus what the base install ships (compare with `/var/log/installer/initial-status.gz` when available); `ls /etc/apt/sources.list.d/` — for each `.list`, confirm it maps to a role's `apt_repository` task. An unmapped repo (a vendor's own `.list`) is an **Add** candidate only after the user confirms intent and the key URL is verified (see Step 4 pitfall below).
- **snap / flatpak**: `snap list` — split OS-default snaps (firefox, snap-store, snapd, core/gnome/kde/mesa base snaps, gtk themes) from third-party snaps. Only third-party snaps are **Add** candidates; OS defaults belong in "Leave out on purpose." Use `flatpak list --app` for flatpaks.
- **user tools**: `pipx list` — also check injected packages (packages injected under a parent via `pipx inject`; they appear nested under the parent in the output, not as separate entries) — run `pipx list --include-injected` or scan for that pattern. Also `uv tool list`, `npm ls -g --depth=0`, `cargo install --list`, `~/.local/bin`.
- **fonts**: non-default families, especially in `~/.local/share/fonts`
- **GNOME**: `dconf dump /` filtered to meaningful paths (keybindings, extensions, interface, default apps), compared with what `setup_gnome` sets
- **services and groups**: `systemctl list-unit-files --state=enabled`, user services, `id`, `/etc/docker/daemon.json`
- **dotfiles**: which files in `~` and `~/.config` are symlinks into the dotfiles repo vs. loose untracked files; `git -C ~/.dotfiles status` and unpushed commits

Use usage evidence (shell history, config/cache mtimes, as in `app-audit.md`) to tell a deliberately kept tool from a forgotten leftover.

## 3. Diff into four buckets

- **Add**: on the machine, in use, not declared in the repo. Name the role it belongs in (or "new role needed").
- **Remove**: declared in the repo but absent from the machine, or present with no sign of use. Remove it from the repo; never from the machine.
- **Update**: declared but different from reality or out of date: changed versions or repo URLs, settings changed in the GUI since, packages renamed or replaced in newer Ubuntu releases, deprecated modules, roles assuming an older release, `group_vars` values that no longer match.
- **Leave out on purpose**: things that must not be in the repo: OS defaults, caches, transient state, large data, and **secrets** (SSH private keys, tokens, `.env` files, kubeconfigs, password stores). If something already in the repo looks like a secret, flag it as a risk and recommend Ansible Vault or an external store; do not copy its value anywhere. A package may be installed on the machine but intentionally excluded from the playbook at the user's request (for example, managed solely through a third-party apt repo without declaring the repo in the role). Respect that exclusion — do not add it just because it is installed.

## 4. Fix the repo

Apply the changes yourself in the working clone, on the branch:

- **Fix directly** the high-confidence Add / Remove / Update items. Put each package or setting in the role it belongs to, following existing patterns (tags, variable files, handlers, `creates`/`changed_when` for shell tasks, idempotent modules).
- **Don't guess** on uncertain items. Leave them untouched and do **not** list them for decision unless the user explicitly asks to add them. The user's standing preference is "do not add anything new" — uncertain items simply disappear from the verdict.
- **Don't guess vendor key URLs.** When an unmapped apt repo appears (a `.list` in `/etc/apt/sources.list.d/` with no matching role), read the URL from the file itself — never invent one. A guessed URL (e.g. appending `/gpg` to a download domain) often 404s because the vendor hosts the key at a different path. Flag the repo, note the URL you read from the file, and ask the user whether they want it managed.
- Keep changes **small and reviewable**: one commit per logical change, with clear messages (for example `setup_base: add ripgrep, in use on machine`).
- Update the README (role list, Quick facts, supported Ubuntu versions) and `requirements.txt`/`requirements.yml` when your changes make them stale.
- **Validate** before committing: `yamllint ./`, `ansible-lint`, and `ansible-playbook local.yml --syntax-check`. These read files and do not change the machine. These tools run on target systems and may not be installed in the environment where the audit runs — if they are missing, commit anyway and flag that validation was skipped rather than blocking the commit. If a lint failure existed before your change, report it separately instead of silently mixing it in.
- Do **not** run the playbook against the machine. `--check --diff` only if the user explicitly asks, because some modules ignore check mode.
- Commit locally on the branch. **Do not push or open a PR** unless the user asks; offer it at the end.

## 5. Verdict

End with:

1. One line on sync status **before** the fixes (**in sync / slightly drifted / significantly drifted**) and what it is now on the branch.
2. A table, ordered by priority:

   `| Item | Found where | Action (Add / Remove / Update) | Target role or file | Status (Fixed / Skipped) |`

3. The branch name, working-clone path, commit list, and `git diff --stat` against the base branch, so the user can review in one glance.
4. A **Do not back up** list (secrets, caches, large or regenerable data) with reasons, plus any secrets already found in the repo.
5. The next step for the user: review the branch, then push or merge it themselves, or ask you to.
