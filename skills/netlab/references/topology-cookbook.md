# netlab topology cookbook

Every snippet below was run through `netlab create` on netlab 26.09 and produced no errors. Combine them freely; each is a complete `topology.yml`.

Contents: link formats, unnumbered links, hosts and gateways, VRRP, static routes, LAG, VLAN with IRB, mixed vendors, BGP session options, IS-IS, groups and custom config, external tools, validation tests, link impairment, multi-provider notes.

## Link formats

```yaml
provider: clab
defaults.device: frr
module: [ ospf ]
nodes: [ r1, r2, r3 ]
links:
- interfaces: [ r1, r2 ]            # explicit interface list
  ospf.cost: 5                      # link attribute (both ends)
- interfaces: [ { node: r2 }, { node: r3, ospf.cost: 7 } ]   # per-interface attribute
- r1:
    ifindex: 5                      # pin r1's side to port 5 (eth5 / Ethernet5 / ...)
  r3:
```

Other forms: `r1-r2` (string, p2p), `[ r1, r2, r3 ]` (list, LAN), and a dict of node names plus link attributes. `links` itself may be a dictionary of named subsets of links (only changes the presentation and error messages). All formats can be mixed in one topology.

## Unnumbered point-to-point links

```yaml
provider: clab
defaults.device: frr
module: [ ospf ]
addressing:
  p2p:
    unnumbered: true
nodes: [ r1, r2, r3 ]
links: [ r1-r2, r2-r3 ]
```

Check device support with `netlab show modules` and the device's caveats; not every platform supports unnumbered IPv4 for every protocol.

## Hosts and default gateways

```yaml
provider: clab
defaults.device: frr
module: [ ospf ]
nodes:
  r1:
  h1:
    device: linux
  h2:
    device: linux
links:
- r1:
  h1:
  h2:
```

A link with a host is a LAN; the router's interface becomes passive (role `stub`); hosts get a static default route to the first router's address. Override with link `gateway:` or `role: lan` to make the link transit.

## VRRP / first-hop redundancy

```yaml
provider: clab
defaults.device: eos
module: [ ospf, gateway ]
gateway.protocol: vrrp        # or anycast
nodes:
  r1:
  r2:
  h1:
    device: linux
links:
- r1-r2
- r1:
  r2:
  h1:
  gateway: True
```

## Static routes and other routing objects (`routing` module)

```yaml
provider: clab
defaults.device: frr
module: [ routing ]
nodes:
  r1:
    routing.static:
    - ipv4: 192.0.2.0/24
      nexthop.node: r2
  r2:
links: [ r1-r2 ]
```

The `routing` module also defines prefix lists, ACLs, AS-path/community lists and route-map style policies; list exact keys with `netlab show attributes -m routing`. Read `docs/module/routing.md` upstream before writing policies.

## LAG

```yaml
provider: clab
defaults.device: eos
module: [ lag ]
nodes: [ s1, s2 ]
links:
- lag.members: [ s1-s2, s1-s2 ]
```

Caveats from the docs:

- netlab connects containers and virtual machines with Linux bridges that block LACP frames. To link a VM to a pure container, package the VM into a vrnetlab container (`docs/labs/clab.md`, vrnetlab section).
- `lag.lacp` takes `fast` (default, 1 s timer), `slow` (30 s) or `off`; `lag.lacp_mode` is `active` (default) or `passive` (only one side may be passive). The docs warn against turning LACP off, because link-down is hard to detect in a virtual environment.
- Per-platform LACP/static/passive/MLAG support is a table in `docs/module/lag.md`; check it before promising a working LAG or MLAG lab on a given device.

## VLAN with IRB

```yaml
provider: clab
defaults.device: eos
module: [ vlan, ospf ]
vlans:
  red:
    mode: irb                 # route | bridge | irb
nodes:
  s1:
  h1:
    device: linux
    module: []                # hosts do not inherit modules; explicit is fine
links:
- s1:
  h1:
  vlan.access: red
```

VLAN forwarding modes: `bridge` (L2 only, use with VXLAN/EVPN bridging), `irb` (L2 + routed VLAN interface), `route` (routed subinterfaces). See `assets/examples/03-vlan-trunk.yml` for trunks.

## Mixed vendors

```yaml
provider: clab
defaults.device: frr
module: [ ospf ]
nodes:
  r1:
  r2:
    device: srlinux
  r3:
    device: eos
links: [ r1-r2, r2-r3 ]
```

Every device must support every module used. Container images must exist locally (cEOS) or be pullable (FRR, SR Linux).

## BGP session options via plugin

```yaml
provider: clab
defaults.device: frr
module: [ bgp ]
plugin: [ bgp.session ]
nodes:
  a:
    bgp.as: 65001
  b:
    bgp.as: 65002
links:
- a:
  b:
  bgp.password: Secret1
```

Related plugins: `bgp.policy` (route policies), `bgp.domain`, `bgp.originate`, `ebgp.multihop`. Plugin attributes only become valid after the plugin is listed.

## IS-IS

```yaml
provider: clab
defaults.device: eos
module: [ isis ]
isis.area: "49.0001"
nodes: [ r1, r2 ]
links: [ r1-r2 ]
```

Interface metric is `isis.metric` (`isis.cost` is accepted and normalised into it as of 26.09).

## Groups, custom configuration and embedded templates

```yaml
provider: clab
defaults.device: frr
module: [ ospf ]
plugin: [ files ]
groups:
  routers:
    members: [ r1, r2, r3 ]
    config: [ banner ]        # applied at netlab up; re-run later with: netlab config banner --limit routers
configlets:
  banner:
    frr: |
      hostname {{ inventory_hostname }}
nodes: [ r1, r2, r3 ]
links: [ r1-r2, r2-r3 ]
```

- `config:` on a node or group lists Jinja2 templates; the `.j2` suffix is optional. Node and group `config` lists merge across parent groups; `-name` removes one inherited template and `-` removes all of them.
- A directory of templates lets you ship per-device files (`eos.j2`, `frr.j2`, `r1.j2`, `x1.eos.j2`).
- Templates can use anything from `netlab inspect --node <n>` (e.g. `bgp.neighbors`, `interfaces`).
- netlab sorts custom templates in the order given in groups and nodes; `[a,b]` on one node and `[b,a]` on another is a sorting loop and a fatal error.
- Generic Linux and FRR/Cumulus templates are shell scripts / vtysh input rather than CLI config.

## External tools

```yaml
provider: clab
defaults.device: frr
module: [ ospf ]
nodes: [ r1, r2 ]
links: [ r1-r2 ]
tools:
  graphite:                   # also: suzieq, edgeshark, nso, nuts
```

Tools run as Docker containers after the lab is configured; `netlab up` prints the Graphite URL, and `netlab connect graphite` prints it again.

## Validation tests (`validate:`)

Grade or smoke-test a lab. Verified structure (see also `assets/examples/02-ebgp-ibgp.yml`):

```yaml
validate:
  ping:
    description: h1 can reach h2
    wait: 40                       # retry up to 40 s instead of a fixed sleep
    nodes: [ h1 ]
    devices: [ linux ]
    exec: ping -c 3 -W 1 h2
    valid: |
      "64 bytes" in stdout
  bgp:
    description: EBGP session is up
    nodes: [ x1 ]
    show:
      eos: ip bgp summary | json
    valid:
      eos: |
        {% for n in bgp.neighbors if n.name == 'r2' %}
        vrfs.default.peers["{{ n.ipv4 }}"].peerState == "Established"
        {% endfor %}
```

Rules: each test needs `nodes` and an action: `show` (a device command whose output must be JSON), `exec` (any command; output is in the `stdout` variable), `config` (deploy a template or `inline` change, needs the `files` plugin for inline), `suzieq`, `ansible`, `plugin`, or only `wait`; `valid` is a Python expression (Jinja2 allowed) that must be truthy; use per-device dicts for multi-vendor tests; add `pass:`/`fail:` messages for training labs; `level: warning` downgrades a failure; a test with only `wait` and `stop_on_error` is a failure barrier. `netlab validate` exit codes: 0 all passed, 1 at least one failed, 2 no usable test found, 3 some tests raised warnings. **Linting cannot execute these tests**; say which JSON paths you assumed.

## Link impairment

```yaml
links:
- r1:
  r3:
  tc.delay: 20ms              # also tc.jitter, tc.loss, tc.rate (kbps), tc.corrupt, tc.duplicate, tc.reorder
```

Applied at `netlab up` (unless `defaults.tc.enable: False`); change it later with `netlab tc disable|enable|show|set`. Works with containerlab containers and libvirt VMs; on libvirt, point-to-point links without `tc` attributes must become Linux bridges first (see `docs/netlab/tc.md`).

## Multi-provider and hardware

- **Mixing providers:** libvirt is the primary (default) provider and clab the secondary. Top-level `provider: libvirt`, and `provider: clab` on the nodes that should run as containers (see `assets/examples/07-multi-provider-libvirt-clab.yml`). libvirt primary + clab secondary is the only supported combination; if clab is written as primary with a libvirt node, netlab warns that the topology provider changed to libvirt. A link touching a node on a secondary provider is always treated as a LAN. Start and stop with `netlab up` / `netlab down` only. Details: `docs/labs/multi-provider.md`.
- `provider: external` configures existing physical or virtual devices; set `mgmt.ipv4` per node. Mark devices netlab must not touch with `unmanaged: true`.
- Several labs on one host: `multilab` plugin. Several hosts: `multiserver` plugin.
