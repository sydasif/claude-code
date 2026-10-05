---
name: netlab
description: Build, validate, run and troubleshoot virtual network labs with netlab (https://netlab.tools/, the ipSpace.net lab tool, PyPI package "networklab"). Use this skill whenever the user mentions netlab, a netlab topology or topology.yml, "netlab up/create/initial/validate/connect", or wants a network lab described as YAML (nodes, links, modules) that runs on containerlab, Docker or libvirt with devices like Arista EOS/cEOS, FRR, Cisco IOS/CSR/IOL/NX-OS/IOS XR, Junos, SR Linux, VyOS, Aruba CX, or Linux hosts. Also use it for lab-as-code requests such as an OSPF, IS-IS, BGP, EVPN/VXLAN, VLAN, VRF, MPLS/L3VPN, SR-MPLS/SRv6, LAG/MLAG, VRRP or leaf-and-spine lab, for bgplabs/ipspace-style training labs with automated validation, or for generating vendor device configurations from a lab topology. Trigger even if the user only says "build me a lab with N routers running X" or "containerlab topology" and does not name netlab, because netlab is usually the better way to describe it.
---

# netlab: lab topologies as code

netlab turns a short YAML description of a lab (nodes, links, protocol modules) into a running virtual lab: it allocates addresses, generates the provider file (`clab.yml` or `Vagrantfile`) and an Ansible inventory, starts the lab, and deploys initial, protocol and custom configurations to every device. Same topology, many vendors.

This skill was built from the netlab documentation, the ipSpace.net netlab blog and the netlab-examples repository, and checked against **netlab 26.09** (Sept 2026). netlab changes monthly, so when something looks off run `netlab version` and check the live docs (see "Looking things up").

## The loop: write, lint, inspect, hand off

Claude's sandbox normally cannot start containers or VMs, but it **can** run `netlab create`, which performs the entire data-model transformation without any hypervisor. That catches nearly every topology mistake, so always close the loop with it instead of eyeballing YAML.

1. **Pin down intent.** Devices/vendors, which protocols, how many nodes, hosts needed, which provider (clab, libvirt, or both), where the lab will run. If the user gave enough, do not interrogate them: state assumptions in one line and build. Defaults when unspecified: `provider: clab`, `defaults.device: frr` (free, pulls automatically, boots in seconds) or `eos` if they mention Arista.
2. **Write `topology.yml`.** Start from the closest file in `assets/examples/` and adapt. Keep it minimal; netlab supplies addressing, router IDs, AS-level sessions and so on.
3. **Lint it:** `bash scripts/lint_topology.sh topology.yml --report`. It installs `networklab` if needed, runs `netlab create` in a scratch copy, and prints the addressing plan. Add `--configs` to inspect the exact configuration netlab would push (useful when the user wants to *see* vendor config, or to check a module did what they expect).
4. **Fix errors using the message, not memory.** netlab's errors name the bad attribute and location. `netlab show attributes [-m module] [match]` lists valid attributes; `netlab show modules` and `netlab show devices` show which devices support what. Never invent an attribute; if unsure, look it up.
5. **Hand off run instructions** (see "Running the lab"). Be explicit that lint success means "valid input", not "the lab converged", since only a host with containerlab can prove the latter.
6. If the user asks for a **validated/graded lab**, add a `validate:` section (see `references/topology-cookbook.md`).

Save the final file where the user can get it (`/mnt/user-data/outputs/topology.yml`) and present it. For a multi-file lab (custom templates, defaults), put each file in a folder.

## Topology anatomy (the 90% you need)

```yaml
provider: clab                 # clab | libvirt (primary when mixed with clab) | external
defaults.device: eos           # device type for nodes that do not name one
module: [ ospf, bgp ]          # modules configured on all routers (hosts do NOT inherit)
plugin: [ bgp.session ]        # optional built-in plugins
bgp.as: 65000                  # global module parameters

nodes:                         # list form: names only, all get defaults.device
  r1:                          # dict form: per-node attributes
    bgp.as: 65001              # dotted keys are the same as nested dicts
  r2:
    device: frr
  h1:
    device: linux              # linux with role host: no loopback, static default route

links:
- r1-r2                        # string form: point-to-point, no attributes
- [ r1, r2, r3 ]               # list form: LAN
- r1:                          # dict form: attributes on the link or per interface
  r2:
    ospf.cost: 10
  bandwidth: 100000
  pool: core                   # or prefix: 10.9.9.0/24
```

Key facts to keep straight (each one has bitten LLM-written topologies):

- **Nodes are a list of names or a dict.** A list cannot carry attributes. Node, group, VLAN and VRF names must be identifiers: alphanumeric plus hyphen and underscore, at most 16 characters (raise the limit with `defaults.const.MAX_NODE_ID_LENGTH`). Do not use hyphens in node names if you also use the `r1-r2` link shorthand (it splits on `-`); use the dict/list link form instead. Underscores are legal, but some devices reject them as hostnames, so netlab rewrites them for those platforms. Names reserved by containerlab are rejected.
- **Link dict format:** node names are keys at the same level as link attributes. `r1: { r2: {} }` (nesting one node under another) is wrong and yields `Invalid interface attribute 'r2'`. For clarity you can also write `interfaces: [ { node: r1 }, { node: r2 } ]`.
- **Where an attribute lives matters.** Module attributes can be global, per group, per node, per link or per interface (`ospf.area`, `ospf.cost`, `bgp.as`...). `ospf.area` at node or global level applies to every interface; `defaults.links.*` / `defaults.interfaces.*` do not exist (an LLM hallucination that netlab silently accepts because `defaults` is not validated). Only put things under `defaults:` that are documented there (device, addressing pools, device images, tools, const).
- **Modules and hosts.** The top-level `module:` list is inherited by routers, bridges and daemons but not by `role: host`/`linux` nodes. A per-node `module:` **replaces** the global list, it does not add to it.
- **EVPN needs a global AS**: `bgp.as` (or `evpn.as` / `vrf.as`) at the top level; per-node/per-group `bgp.as` is not enough. IBGP-only fabrics use `bgp.as` globally and route reflectors via `bgp.rr: True`.
- **Automatic groups:** netlab creates a group per device type (`eos`, `frr`) and per AS (`as65000`), useful for `netlab config --limit`. Custom groups can set `device`, `module`, `config`, and any node attribute; `_auto_create: True` lets groups reference nodes that plugins (e.g. `fabric`) create later.
- **Addressing:** pools are `loopback` (10.0.0.0/24), `p2p` (10.1.0.0/16, /30), `lan` (172.16.0.0/16), `mgmt` (192.168.121.0/24), `l2only`, `vrf_loopback`. Point-to-point between two routers uses `p2p`; hosts on a link make it a LAN with the stub role; single-node links are stubs. Override per link with `pool:` or `prefix:` (`prefix: false` gives an L2-only link). Node IDs (1..250) become the last octet on LANs and loopbacks.
- **Interface names come from the device**, not from you. Use `ifindex` to place a link on a specific port; use `ifname` only for virtual interfaces. Do not guess `eth1` vs `Ethernet1`: the device definition decides.
- **Hosts:** `device: linux` gets a `role: host` behaviour: no loopback, static routes via the link gateway. Attach a host to a router LAN link and the router interface becomes passive automatically.

## Choosing provider and device

- **Providers.** `clab` (containerlab) is the best default for new labs: fast, light, and most platforms are containers. **`libvirt` (KVM + Vagrant) is also fully usable** and is the right choice for VM-only images or when the user asks for it; note that as of release 26.09 it is in maintenance mode (bug fixes only, no new features, no integration tests). Why it is in maintenance mode (ipSpace blog, Sept 2026): the vagrant-libvirt plugin has had no release since June 2023, and HashiCorp is shutting down the public Vagrant Cloud box repository by the end of 2026, so users must build or keep their own Vagrant boxes. netlab keeps the provider, fixes bugs, and still runs libvirt in its platform integration tests; its author encourages building vrnetlab containers for the devices you use. **VirtualBox was removed** (use release 26.06 or earlier if truly needed). If the user names a provider, use it. containerlab needs the user in the `clab_admins` and `docker` groups (`netlab install containerlab` on Ubuntu sets that up); libvirt needs `libvirt` and `vagrant`.
- **Mixing libvirt and clab in one lab: libvirt is always the primary (default) provider; clab can only be secondary.** Set `provider: libvirt` at the top level and `provider: clab` on the nodes that should be containers (typically Linux hosts or FRR). The only supported combination is libvirt primary + clab secondary. If you write `provider: clab` at the top and `provider: libvirt` on a node, netlab warns `Topology provider changed from clab to libvirt` and makes libvirt the primary anyway, so write it the right way round. Always use `netlab up` / `netlab down` for mixed labs (not `vagrant` or `containerlab` directly). Set `uplink` only on the primary provider. The `provider:` attribute works on nodes **and groups** (for example a `hosts` group with `provider: clab`). Behind the scenes VMs and containers share one management subnet (the libvirt management bridge), and VM-to-VM point-to-point links that touch a container become Linux-bridge links, which is why a hand-started `vagrant up` or `containerlab deploy` makes a mess. Example: `assets/examples/07-multi-provider-libvirt-clab.yml`.
- **Zero-friction devices** (image pulls automatically): `frr`, `linux`, `srlinux` (Nokia SR Linux), `vyos`. **Needs a manually obtained image:** Arista cEOS (download from Arista, `docker import`), Cisco IOS XRd, Cisco 8000v; **vrnetlab-built VM-in-container images** (CSR, Cat8000v, IOSv, IOL, NX-OS, vJunos, ArubaCX, FortiOS, SR OS...) need nested virtualization and a self-built image whose tag may differ from netlab's default: override with `defaults.devices.<device>.clab.image: <tag>`.
- Support levels differ: `full` (integration-tested), `best-effort`, `minimal`, `end-of-life`. Cisco IOSv is deprecated as of 26.09 (support level minimal). Cumulus Linux 4/5 (non-NVUE) is end of life. Run `netlab show devices` for the current list and `netlab show modules` to check that the device supports every module in the lab (netlab errors out if not).
- If the user does not have a Linux box: netlab runs in GitHub Codespaces (the netlab-examples repo has a devcontainer; FRR/SR Linux/cEOS containers work), in an Ubuntu VM, and on Apple Silicon inside a Multipass VM (containers only).
- Full device/image table and platform notes: `references/platforms-and-install.md`.

## Running the lab (what to tell the user)

```bash
netlab up                  # create + start + configure (netlab up --snapshot restarts after reboot)
netlab status              # running instances (add --all)
netlab connect r1          # SSH / docker exec;  netlab connect r1 --show ip route  (vtysh handled for FRR)
netlab exec r1,r2 ip route # same command on several nodes; nodes may be names, groups, device types or globs (add --header)
netlab validate            # run the topology's validate: tests (exit code 0 = all passed)
netlab collect             # save running configs into ./config (before netlab down)
netlab down --cleanup      # destroy lab and remove generated files
```

Other useful commands: `netlab config <template>` (deploy a custom Jinja2 template, `--limit` to a group), `netlab initial -m ospf -l r1` (redeploy one module on one node), `netlab capture r1 eth1` (packet capture), `netlab tc` (link impairment), `netlab graph`/`netlab report` (topology diagrams and reports), `netlab inspect --node r1` (all data netlab holds for a node), `netlab restart`. Full CLI notes in `references/cli-and-workflow.md`.

Adding tools: `tools: { graphite: , suzieq: }` starts Graphite GUI or SuzieQ as Docker containers after the lab is configured. Running several labs on one server needs the `multilab` plugin.

## Modules and plugins in one screen

Modules (top-level `module:` or per node): `initial` is implicit; `ospf`, `isis`, `bgp`, `eigrp`, `ripv2`, `bfd`, `vlan`, `vrf`, `vxlan`, `evpn`, `mpls` (LDP, BGP-LU, MPLS/VPN, 6PE), `sr-mpls`, `srv6`, `lag` (incl. MLAG), `stp`, `gateway` (VRRP, anycast gateway), `dhcp`, `routing` (static routes, prefix lists, ACLs, route maps, AS-path and community lists), `services` (DNS client/server settings and, since 26.09, syslog clients/servers). Attribute tables per module: `references/modules-cheatsheet.md`.

Built-in plugins (`plugin: [ ... ]`): `fabric` (leaf-and-spine generator), `files` (embed templates/files in the topology: `configlets`, `files`, `config.inline`), `bgp.session`, `bgp.policy`, `bgp.domain`, `bgp.originate`, `ebgp.multihop`, `ospf.areas`, `vrrp.version`, `bonding`, `mlag.vtep`, `evpn.multihoming`, `tunnel.gre`, `tunnel.wireguard`, `firewall.zonebased`, `node.clone`, `multilab`, `multiserver`, `check.config`, `kind`.

Anything netlab does not model yet: custom Jinja2 configuration templates via a `config:` attribute on nodes/groups (device-specific files in a directory named after the template), applied at `netlab up` or later with `netlab config`. Use the `files` plugin to keep those templates inside the single topology file.

## Automated lab validation

Add a `validate:` dictionary to check the lab or grade an exercise. Each test has `nodes`, an action (`show` for JSON output, `exec` for text, `config` to push a change, or just `wait`), and a Python-expression `valid:` that may use Jinja2 over the node's netlab data (for example `bgp.neighbors`). Use `wait:` together with `show`/`exec` to retry until the protocol converges instead of a fixed sleep. See the worked examples in `references/topology-cookbook.md` and `assets/examples/02-ebgp-ibgp.yml`. Run with `netlab validate`; `--list`, `-e` (errors only) and `-v` help while developing. Linting cannot execute these tests, so tell the user which show command/JSON path you assumed per platform.

## Common mistakes checklist (review before delivering)

1. Every node named in `links`, `groups`, `vlans.*.links` exists (or the group has `_auto_create: True`).
2. Every device in the lab supports every module it uses (`netlab show modules`), and the topology sets a device for every node (`defaults.device` or `device:`).
3. Hosts that need a module (for example DHCP client behaviour) have it in their own `module:`; routers that need extra modules list *all* of them.
4. Global AS for EVPN/VRF-RD; `bgp.as` differs between nodes intended as EBGP peers; IBGP peers share it.
5. VLAN links: `vlan.access`, `vlan.trunk` on the link/interface, `vlans:` defined, `vlan` module on the switches, and `vlan.mode: bridge|irb|route` chosen deliberately.
6. Link `type`: leave it alone unless making loopbacks, tunnels or LAGs. To force address pools use `pool:`, not `type:`.
7. LAG/LACP over containerlab: netlab links containers with Linux bridges that can block LACP; check `references/modules-cheatsheet.md` LAG notes before promising LACP on containers.
8. Names: no duplicate node names, no >16 characters, no reserved containerlab names, no hyphen if using string links.
9. Images: state which images the user must pull/build (cEOS, XRd, vrnetlab) so `netlab up` does not fail on a missing image.
10. `netlab create` printed no `[ERRORS]` and no unexpected `[WARNING]`.

## Looking things up

Order of preference when this skill lacks a detail:

1. The installed tool itself: `netlab show attributes -m <module>`, `netlab show modules`, `netlab show devices`, `netlab show images`, `netlab show defaults <path>`, `netlab inspect`.
2. Raw markdown docs, which are fetchable from the sandbox: `https://raw.githubusercontent.com/ipspace/netlab/dev/docs/<path>.md` (for example `docs/module/bgp.md`, `docs/links.md`, `docs/platforms.md`, `docs/labs/clab.md`, `docs/plugins/fabric.md`). Or `git clone --depth 1 https://github.com/ipspace/netlab.git`.
3. https://netlab.tools/ (the rendered docs) and https://blog.ipspace.net/tag/netlab/ (worked examples, release notes, quirks per vendor).
4. Sample topologies: https://github.com/ipspace/netlab-examples (BGP, EVPN, VLAN, VRF, MPLS, DHCP, routing, plugins, multi-platform). `references/docs-map.md` lists what is where.

## Bundled resources

- `scripts/lint_topology.sh`: validate a topology offline (`--report` addressing plan, `--configs` generated configs).
- `assets/examples/`: seven lint-verified starting points (OSPF triangle, EBGP+IBGP with validation, VLAN trunk, EVPN/VXLAN fabric, MPLS/VPN with VRFs, static addressing + configlets + link impairment, libvirt+clab mixed providers).
- `references/topology-cookbook.md`: more patterns (groups, custom config, validation tests, tools, multi-provider, hosts, unnumbered, stub networks).
- `references/modules-cheatsheet.md`: attribute cheat sheet per module and the common routing-protocol knobs.
- `references/platforms-and-install.md`: supported devices, clab images, install paths, provider caveats.
- `references/cli-and-workflow.md`: every command with the flags that matter, debugging.
- `references/docs-map.md`: where to find deeper documentation, examples repo layout, and blog posts by topic.
