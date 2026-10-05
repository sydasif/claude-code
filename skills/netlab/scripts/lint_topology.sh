#!/usr/bin/env bash
# Validate a netlab lab topology WITHOUT starting any containers or VMs.
#
# What it does
#   1. Installs the `networklab` PyPI package if `netlab` is missing.
#   2. Copies the topology (and its sibling files) to a scratch directory so the
#      user's directory is not littered with generated files.
#   3. Runs `netlab create`, which performs the full data-model transformation:
#      attribute validation, addressing, module checks, device-feature checks.
#   4. Optionally prints the addressing report and generated device configs.
#
# Usage
#   lint_topology.sh topology.yml            # validate only (exit code = netlab's)
#   lint_topology.sh topology.yml --report   # + addressing plan
#   lint_topology.sh topology.yml --configs  # + generated initial/module configs
#   lint_topology.sh topology.yml --keep     # keep scratch dir, print its path
#   Extra arguments after `--` go to `netlab create` (e.g. -- -d frr -p clab).
#
# A clean run proves the topology is *valid netlab input*. It does not prove the
# lab boots or converges: that needs `netlab up` on a host with containerlab.

set -uo pipefail

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi

TOPO="$1"; shift
REPORT=0; CONFIGS=0; KEEP=0; EXTRA=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --report)  REPORT=1 ;;
    --configs) CONFIGS=1 ;;
    --keep)    KEEP=1 ;;
    --)        shift; EXTRA=("$@"); break ;;
    *) echo "Unknown option: $1" >&2; exit 64 ;;
  esac
  shift
done

if [[ ! -f "$TOPO" ]]; then
  echo "Topology file not found: $TOPO" >&2
  exit 66
fi

if ! command -v netlab >/dev/null 2>&1; then
  echo "[lint] netlab not found; installing networklab from PyPI..." >&2
  pip install networklab --break-system-packages -q 2>&1 | tail -2 >&2
  command -v netlab >/dev/null 2>&1 || { echo "[lint] could not install netlab" >&2; exit 69; }
fi

SRC_DIR="$(cd "$(dirname "$TOPO")" && pwd)"
TOPO_NAME="$(basename "$TOPO")"
WORK="$(mktemp -d /tmp/netlab-lint.XXXXXX)/lab"
mkdir -p "$WORK"
# Copy sibling files (custom templates, defaults) but skip generated artefacts.
( cd "$SRC_DIR" && tar cf - --exclude='netlab.snapshot.pickle' --exclude='node_files' \
    --exclude='host_vars' --exclude='group_vars' --exclude='clab.yml' \
    --exclude='hosts.yml' --exclude='ansible.cfg' --exclude='Vagrantfile' . ) | ( cd "$WORK" && tar xf - )

cd "$WORK" || exit 70
echo "[lint] $(netlab version 2>&1 | head -1)"
echo "[lint] netlab create $TOPO_NAME ${EXTRA[*]:-}"
netlab create "$TOPO_NAME" "${EXTRA[@]}" 2>&1 | grep -v '^Created ' 
RC=${PIPESTATUS[0]}

if [[ $RC -eq 0 ]]; then
  echo "[lint] OK: topology is valid netlab input"
  if [[ $REPORT -eq 1 ]]; then
    echo; echo "[lint] ---- addressing plan ----"
    netlab report addressing 2>&1
  fi
  if [[ $CONFIGS -eq 1 ]]; then
    echo; echo "[lint] ---- generated device configurations ----"
    netlab initial -o cfg --clean >/dev/null 2>&1
    for f in cfg/*; do
      [[ -f "$f" ]] || continue
      case "$f" in *.daemons.cfg|*.hosts.cfg) continue ;; esac   # boilerplate, not interesting
      echo; echo "##### $f"; cat "$f"
    done
  fi
else
  echo "[lint] FAILED (exit $RC). Fix the errors above; use 'netlab show attributes' for valid attributes." >&2
fi

if [[ $KEEP -eq 1 ]]; then
  echo "[lint] scratch directory kept: $WORK"
else
  rm -rf "$(dirname "$WORK")"
fi
exit $RC
