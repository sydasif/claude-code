# Where things are documented

Live docs: https://netlab.tools/ . Markdown sources (fetchable from a sandbox that can reach GitHub raw): `https://raw.githubusercontent.com/ipspace/netlab/dev/docs/<path>.md`, or `git clone --depth 1 https://github.com/ipspace/netlab.git` and read `docs/`. netlab releases monthly (YY.MM); release notes live in `docs/release/<version>.md`.

## Core docs (`docs/`)

| Topic | File |
|---|---|
| Topology overview and reference (all top-level keys) | `topology-overview.md`, `topology-reference.md` |
| Nodes and their attributes | `nodes.md` |
| Links: formats, attributes, types, gateways, netem | `links.md` |
| Addressing pools and static addressing | `addressing.md`, `prefix.md` |
| Groups | `groups.md` |
| Defaults (system, user, project) | `defaults.md`, `topology/` (validate, etc.) |
| Modules overview and per-module pages | `modules.md`, `module-reference.md`, `module/<name>.md` |
| Providers and platform support tables | `providers.md`, `platforms.md`, `labs/clab.md`, `labs/libvirt.md`, `labs/external.md` |
| Per-device notes and quirks | `labs/<device>.md` (`eos`, `frr`, `srlinux`, `iosxr`, `vyos`, `csr`, ...) |
| Multi-provider labs | `labs/multi-provider.md` |
| Custom config templates | `custom-config-templates.md` |
| Extending attribute sets | `extend-attributes.md` |
| Plugins | `plugins.md`, `plugins/<name>.md` (`fabric`, `files`, `bgp.session`, `bgp.policy`, `multilab`, ...) |
| External tools (Graphite, SuzieQ, Edgeshark, ...) | `extools.md`, `extool/` |
| CLI commands | `netlab/<command>.md`, `cli-overview.md` |
| Lab validation | `topology/validate.md`, `netlab/validate.md` |
| Installation | `install.md`, `install/ubuntu.md`, `install/ubuntu-vm.md`, `install/linux.md`, `install/cloud.md`, `install/clone.md` |
| Tutorials | `tutorials.md` |
| Developer docs (adding devices, quirks, tests) | `dev/` |

## Sample topologies

https://github.com/ipspace/netlab-examples: folders by feature (BGP, EVPN, VLAN, VRF, MPLS, routing, DHCP, plugins, multi-platform, tools). Each folder usually has a `topology.yml` plus a README. Good starting points: `EVPN/`, `VLAN/`, `VRF/`, `MPLS/`, `BGP/`. Also https://bgplabs.net/ for validated lab exercises that use `validate:` tests and the same tooling.

## Blog

https://blog.ipspace.net/tag/netlab/ : release announcements, design rationale and vendor-specific caveats. Ivan Pepelnjak's post about ChatGPT-generated netlab topologies documents typical AI mistakes (wrong link nesting, invented attributes); this skill's lint step exists to catch them.

## When the docs and this skill disagree

Trust, in order: (1) the installed tool (`netlab show ...`, `netlab create` errors), (2) the docs at the version the user runs (`netlab version`), (3) this skill.
