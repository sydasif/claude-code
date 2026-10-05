# Platforms, images and installation

Checked against netlab 26.09 (`netlab show devices`, `netlab show images`, `docs/platforms.md`, `docs/labs/clab.md`, `docs/install/*`).

Contents: providers, device support, default images, getting images, install paths, running without a Linux box, permissions.

## Providers

| Provider | Status | Use for |
|---|---|---|
| `clab` (containerlab) | Recommended; default going forward | Containers and vrnetlab VM-in-container images; fast start, low RAM |
| `libvirt` (KVM + Vagrant) | Fully usable; in maintenance mode in 26.09 (bug fixes only, no new features, no integration tests) | VM-only images; labs that need real VMs. **Primary provider when combined with clab** |
| `external` | Supported | Configure already-running or physical devices (`mgmt.ipv4` per node, `unmanaged: true` to skip a node) |
| VirtualBox | **Removed**; use 26.06 or earlier | n/a |

Set with top-level `provider:` (or per node); `netlab up -p clab` overrides it. **Combining providers:** libvirt is primary and clab secondary (the only supported combination); per-node `provider: clab` under a top-level `provider: libvirt`. Use `netlab up`/`netlab down` for such labs.

### libvirt background (as of Sept 2026)

- netlab is moving to containerlab as its main orchestrator because the vagrant-libvirt plugin is effectively abandoned (last release June 2023) and HashiCorp is retiring Vagrant Cloud, the public box repository, by the end of 2026. Boxes you already built keep working; plan to build and host your own.
- Nothing is removed yet. Bug fixes continue, libvirt stays in the platform integration tests, and a code cleanup is expected a year or two out. Building vrnetlab containers for your devices is the suggested migration path.
- Mixed labs (libvirt primary, clab secondary) put VMs and containers on one management subnet via the libvirt management bridge; start and stop them only with `netlab up` and `netlab down`.

## Device support (26.09)

Full support (integration-tested): `arubacx`, `cat8000v`, `crpd`, `csr`, `csrx`, `dellos10`, `eos`, `frr`, `iol`, `ioll2`, `iosxr`, `linux`, `srlinux`, `srsim`, `vjunos-router`, `vjunos-switch`, `vptx`, `vyos`. Best-effort: `arcos`, `nxos`, `openbsd`, `vmx`, `vsrx`. Minimal: `asav`, `cisco8000v`, `cumulus_nvue`, `exos`, `fortios`, `iosv`, `iosvl2`, `netscaler`, `routeros7`, `sonic`, `sros`, `vpp`. Obsolete: `cumulus` (4.x / 5.x without NVUE), `routeros`. Daemons: `bird`, `dnsmasq`, `kind`.

Always confirm with `netlab show devices` and `netlab show modules`; the list moves every month.

## Default container images (clab)

| Device | Image | Availability |
|---|---|---|
| `frr` | `quay.io/frrouting/frr:10.7.1` | pulled automatically |
| `linux` | `python:3.13-alpine` | pulled automatically |
| `srlinux` | `ghcr.io/nokia/srlinux:26.7.2` | pulled automatically |
| `vyos` | `ghcr.io/sysoleg/vyos-container...` | pulled automatically |
| `bird`, `dnsmasq`, `vpp` | `netlab/<name>:latest` | pulled automatically |
| `eos` | `ceos:4.34.2F` | **you import it** (download cEOS from Arista, `docker import`, tag as shown) |
| `iosxr` | `ios-xr/xrd-control-plane:...` | you obtain/import it |
| `crpd`, `csrx`, `vmx`, `vsrx`, `arcos`, `srsim` | vendor-supplied | you obtain/import it |
| `csr`, `cat8000v`, `iosv`, `iol`, `nxos`, `arubacx`, `fortios`, `vjunos-*`, `vptx`, `sros`, ... | `vrnetlab/...` | **you build it with vrnetlab** (needs KVM/nested virtualization for VM-based ones) |

Override the image for one device type with `defaults.devices.<device>.clab.image: <tag>` (top-level defaults) or per node with `image:`. `netlab show images` prints the current defaults for both providers. Vendor images are licensed by the vendors: netlab cannot download them for the user.

## Installation

- Ubuntu server or VM (simplest): `sudo python3 -m pip install networklab` (or `pip3 install networklab`; add `--break-system-packages` on recent Ubuntu if pip refuses), then `netlab install ubuntu ansible containerlab` (add `libvirt` only if needed). If chained installs fail on some Ubuntu releases, run one `netlab install` per component.
- Groups: for containerlab the user must be in `docker` and `clab_admins`; for libvirt in `vagrant` and `libvirt`. Log out and back in after `netlab install`; check with `groups`.
- Manual/other Linux: `docs/install/linux.md`; Ansible 2.9.1 or later (latest 11.x recommended) plus networking collections (`ansible-galaxy collection` via `netlab install ansible`).
- From source: `git clone https://github.com/ipspace/netlab`, `python3 -m pip install -r requirements.txt`, `source setup.sh` (or `pip3 install -e .`).
- Cloud/VM guidance: `docs/install/cloud.md`, `docs/install/ubuntu-vm.md`, and the devcontainer in netlab-examples for GitHub Codespaces.

## No Linux server?

- **GitHub Codespaces**: netlab-examples ships a devcontainer; containers such as FRR, SR Linux and cEOS work, VM-based images do not.
- **Windows**: an Ubuntu VM (or WSL virtual machine) with `netlab install`.
- **macOS / Apple Silicon**: run netlab in a Linux VM (for example Multipass); only ARM-capable container images work.
- Claude's own sandbox: can lint (`netlab create`, `netlab initial -o cfg`) but cannot start containers.

## Lab hygiene

Check for stale labs with `netlab status --all`; `netlab down --cleanup` removes generated files; run several labs on one host with the `multilab` plugin; ports for tools like Graphite are shown at `netlab up`.
