# Module attribute cheat sheet

Generated from `netlab show attributes -m <module>` on netlab 26.09. **The installed tool is authoritative**: when a key is not listed here, run `netlab show attributes -m <module>` (add a word to filter) rather than guessing. Attribute *scope* matters: a key can exist only at `global`, `node`, `link`, `interface`, `vlan` or `vrf` level.

Contents: enabling modules, OSPF, BGP, IS-IS, VLAN, VXLAN, EVPN, VRF, MPLS, gateway, LAG, other modules, common failures.

## Enabling modules

- Top-level `module: [ ospf, bgp ]` enables modules on all routers; a node-level `module:` list **replaces** it for that node. Hosts (`linux`) do not inherit the global list.
- Global module parameters live at top level under the module name: `ospf.area: 0`, `bgp.as: 65000`.
- Check support: `netlab show modules` (which devices support which module); netlab errors if a device lacks a module you enabled on it.

## OSPF

| Scope | Attributes |
|---|---|
| global / node | `area` (IPv4 format, default 0.0.0.0), `af` (`ipv4`, `ipv6`), `bfd`, `passive`, `password`, `process`, `reference_bandwidth`, `timers.hello`, `timers.dead` |
| link / interface | `area`, `cost` (1-65534), `network_type` (point-to-point, point-to-multipoint, broadcast, non-broadcast), `passive`, `password`, `digest`, `timers.*`, `bfd`, `priority` (0-255) |
| loopback | `area`, `cost` |

Multi-area: put `ospf.area` per node (all interfaces inherit) or per link/interface (ABR). The `ospf.areas` plugin adds per-area settings.

## BGP

| Scope | Attributes |
|---|---|
| global | `as`, `as_list` (map AS to members/route reflectors), `community` (`ebgp`, `ibgp`), `confederation`, `next_hop_self`, `advertise_loopback`, `advertise_roles`, `replace_global_as`, `rr_cluster_id`, `rr_list`, `rr_mesh`, `sessions`, `activate`, `ebgp_role` |
| node | `as`, `rr` (route reflector), `router_id`, `originate`, `advertise`, `import`, `local_as`, `next_hop_self`, `replace_global_as`, `community`, `sessions`, `activate` |
| interface / link | `local_as`, `replace_global_as`, `advertise` |
| vrf | `advertise`, `import`, `originate`, `router_id` |

Sessions are built automatically (IBGP without an IGP module in the lab produces a `missing_igp` warning: add `ospf`, `isis`, `eigrp` or `ripv2`): nodes with the same AS get IBGP (full mesh, or via `bgp.rr: True` nodes), different AS on a shared link gets EBGP. Use `bgp.as_list` for compact multi-AS labs: `bgp.as_list: { 65000: { members: [ r1, r2 ] }, 65100: { members: [ x1 ] } }`. Session extras (passwords, timers, multihop) come from plugins: `bgp.session`, `ebgp.multihop`; policies from `bgp.policy`.

## IS-IS

Global: `area` (NET format, e.g. `"49.0001"`), `type` (`level-1`, `level-2`, `level-1-2`), `af`, `bfd`, `instance`. Link: `metric` or `cost` (1-16777215; `metric` wins), `network_type` (`point-to-point`), `passive`, `bfd`. Wide metrics are always on.

## VLAN

- Global `vlan.mode`: `bridge`, `irb`, `route` (can also be set per VLAN or per node).
- Define VLANs at top level: `vlans: { red: {}, blue: { mode: route } }`; VLAN IDs and VNIs are auto-assigned unless given (`id`, `vni`).
- Link/interface attributes: `vlan.access: <vlan>`, `vlan.trunk: [ ... ]`, `vlan.native: <vlan>`. Or list member links inside the VLAN: `vlans.red.links: [ h1-s1, h2-s2 ]`.
- IRB VLANs get an SVI with an address from the VLAN's prefix (gateway address per `gateway` module when enabled).

## VXLAN and EVPN

- `vxlan`: `vlans` (list to extend over VXLAN), `flooding` (`static`, `evpn`), `domain`, `use_v6_vtep`, link `vtep`.
- `evpn`: needs a **global** AS (`bgp.as`, or `evpn.as` / `vrf.as`); `session` (`ibgp`, `ebgp`), `vlans`, `vrfs`, `transport` (`vxlan`, `mpls`, `sr`), `start_transit_vni`; per VLAN/VRF `evi`, `rd`, `import`, `export`; VRF `bundle` (`vlan_aware`, `vlan`, `port`, `port_vlan`), `transit_vni`.
- Typical leaf: `module: [ ospf, bgp, vlan, vxlan, evpn ]`; spine: `[ ospf, bgp, evpn ]` with `bgp.rr: True` for IBGP fabrics. The `fabric` plugin creates spines/leafs (`fabric.spines: 2`, `fabric.leafs: 4`, named `S1..`, `L1..`).
- Multihoming: `evpn.multihoming` plugin.

## VRF

Top-level `vrfs:` defines VRFs; attach one to a link or interface with `vrf: red` (or list links inside the VRF with `links:`). Per-VRF keys: `rd`, `import`, `export` (route-target lists), `loopback` (bool or prefix), and routing-protocol settings such as `ospf.active`, `ospf.area`, `bgp.router_id`, `ospf.router_id`, `<igp>.af`. Node/global: `vrf.loopback`, `vrf.as` (AS used in RD/RT when `bgp.as` is unset; system default 65000). MPLS/VPN needs `mpls.vpn: True` with BGP (see `assets/examples/05-vrf-mpls-vpn.yml`).

## MPLS

Global keys: `mpls.ldp` (with `advertise`, `explicit_null`, `igp_sync`, `router_id`), `mpls.bgp` (BGP labeled unicast: `ipv4`/`ipv6` session types, `explicit_null`, `disable_unlabeled`), `mpls.vpn` (`ipv4`/`ipv6` session types), `mpls.6pe`. Segment routing has separate `sr-mpls` and `srv6` modules.

## Gateway (VRRP / anycast)

`gateway.protocol`: `vrrp` or `anycast` (global, node or link); `gateway.id`, `gateway.ipv4`/`ipv6` (link), `gateway.vrrp.{group,priority,preempt}`, `gateway.anycast.{mac,unicast}`. Set link `gateway: True` to enable using defaults. Combine with `vlan` for first-hop redundancy per VLAN.

## LAG

Link-level `lag.members: [ s1-s2, s1-s2 ]`, global/link `lag.lacp` (`fast`, `slow`, `off`), `lag.lacp_mode` (`active`, `passive`), `lag.mode` (`802.3ad`, `balance-xor`), `lag.lacp_system_id` per interface. **Container/VM bridge caveat**: netlab's Linux bridges block LACP between VMs and containers; see `docs/module/lag.md` for the per-platform support table (LACP, static, passive, MLAG).

## Other modules (look up before use)

`eigrp`, `ripv2`, `bfd`, `stp`, `dhcp` (server/relay/client behaviour and pools), `routing` (static routes, prefix lists, ACLs, route maps, community lists), `services` (DNS, and syslog since 26.09), `sr-mpls`, `srv6`, `vxlan`. Each has a page at `docs/module/<name>.md`.

## Common failures and what they mean

| Message | Usual cause |
|---|---|
| `Invalid interface attribute 'r2'` | Link written with one node nested under another (`r1: { r2: ... }`); node names must be siblings |
| `Cannot get a usable global AS number` (EVPN) | Set global `bgp.as` (or `evpn.as` / `vrf.as`) |
| Device does not support module | `netlab show modules`; pick another device or drop the module for that node |
| Unknown attribute warning | Typo, wrong scope, or a plugin that defines it is not in `plugin:` |
| Node name too long / invalid | Names must be identifiers of at most 16 characters |
