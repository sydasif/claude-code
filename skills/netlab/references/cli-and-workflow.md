# CLI and workflow reference

Usage strings verified against netlab 26.09. `netlab <command> -h` always prints the current options. Almost every command accepts `-i/--instance` (which lab, relevant with `multilab`), `-v` and `-q`.

Contents: lab lifecycle, config and validation, inspecting data, offline generation, tools and misc, debugging recipes.

## Lab lifecycle

| Command | Purpose | Flags worth knowing |
|---|---|---|
| `netlab up [topology]` | create files, start the lab, configure devices | `-p PROVIDER` override provider, `-d DEVICE` default device, `--plugin`, `-s key=value` add topology parameters, `--no-config` start only, `--no-tools`, `--dry-run`, `--fast-config`, `--snapshot [FILE]` restart from an existing snapshot, `-r DIR` reload saved configs |
| `netlab down` | destroy the lab | `--cleanup` also removes files created by `netlab create`, `--force`, `--dry-run` |
| `netlab restart` | down + up again | see `netlab restart -h` |
| `netlab status` | running lab instances | `--all`, `--memory`, `--log`, `--cleanup`, `--reset`, `--format json|yaml|text` |

## Working with devices

| Command | Purpose |
|---|---|
| `netlab connect <node>` | SSH or `docker exec` into a device (or print a tool URL, e.g. `netlab connect graphite`); `-s "show ip route"` runs a show command; the rest of the args go to SSH/docker exec |
| `netlab exec <nodes> <command...>` | run a command on one or several nodes (names, groups, device types, patterns); `--header`, `--dry-run` |
| `netlab capture <node> [intf]` | packet capture; extra arguments go to the capture utility |
| `netlab config <template> [-l LIMIT] [-e VAR=VALUE...] [-r]` | deploy a custom Jinja2 template (or a directory of templates); `-r` reloads saved device configs |
| `netlab initial` | rerun parts of the configuration: `-i` initial only, `-n` normalize only, `-m [modules]` module configs (comma-separated), `-c` custom templates, `-l NODES` limit, `--ready`, `--fast` |
| `netlab collect` | download device configs into `./config` (`-o DIR`, `--suffix`, `--tar FILE`, `--cleanup`) |
| `netlab tc {enable,disable,show,set}` | manage link impairments (containerlab and libvirt) |

## Validation

`netlab validate` runs the topology's `validate:` tests against the running lab. Exit codes: 0 all passed, 1 a test failed, 2 no usable test, 3 warnings. Useful flags: see `netlab validate -h` (list tests, errors only, verbose output). The tests come from the saved snapshot created by `netlab up`; after editing tests in a running lab, recreate the snapshot with the hidden `netlab create --unlock` (docs).

## Inspecting data (no running lab needed)

| Command | Purpose |
|---|---|
| `netlab create [topology] [-o formats]` | transform the topology and write provider + Ansible files; `-o` selects output formats (e.g. `-o graph`, `-o yaml`); errors here mean the topology is invalid |
| `netlab initial -o cfg` | write the generated device configurations to a directory instead of deploying them (add `--clean` to delete generated files afterwards) |
| `netlab inspect [expr] [--node N] [--all] [--format yaml|json]` | dump transformed data for nodes/links/modules (this is the data custom templates see) |
| `netlab report <name> [file]` | reports such as `addressing`; `--node` to limit |
| `netlab graph [-t topology|bgp|isis] [-f formats] [-e graphviz|d2] [file]` | generate Graphviz or D2 diagrams |
| `netlab show attributes [-m MODULE] [match]` | valid attributes per module/global; `--format text|yaml|table` |
| `netlab show defaults [match]`, `netlab defaults <glob>` | system/user/project defaults and where they come from (`-s`) |
| `netlab show devices`, `show modules`, `show images` | supported devices with support levels, module support matrix, default images per provider |
| `netlab install [script...]` | install system software (`ubuntu`, `ansible`, `containerlab`, `libvirt`, ...; run with no args for the list; `-y`, `--all`) |

## Debugging recipes

1. **Topology error**: read the `[ERROR]`/`Errors encountered` block; it names the section (`nodes`, `links`, `evpn`, ...) and often the fix. Re-run `netlab create -v`.
2. **What did netlab decide?** `netlab report addressing`, `netlab inspect --node r1`, `netlab inspect --node r1 bgp.neighbors`, `netlab initial -o cfg` to view the exact config.
3. **Device did not converge**: `netlab connect r1 -s "show ip ospf neighbor"` (or the platform equivalent), then `netlab initial -m ospf -l r1` to redo one module on one node, or `netlab config <template> -l r1` for a custom fix.
4. **Image missing** (`netlab up` fails at clab deploy): `netlab show images`; import/build the image or override with `defaults.devices.<dev>.clab.image`.
5. **Change without full restart**: `netlab down --cleanup` then `netlab up` is the reliable path; containerlab labs restart in seconds, VMs do not (use `--snapshot` or `netlab collect` first to keep configs).
6. **Permission errors** with containerlab: user must be in `clab_admins` and `docker`; re-login after group changes.
7. **Global overrides without editing the topology**: `netlab up -s defaults.device=frr`, `netlab up -p clab`, project-level `topology-defaults.yml` in the lab directory, user-level `~/.netlab.yml`, or `netlab defaults`.
