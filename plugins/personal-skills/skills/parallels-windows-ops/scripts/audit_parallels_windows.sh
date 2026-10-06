#!/usr/bin/env bash
set -euo pipefail

vm_name="${1:-Windows 11}"

section() {
  printf '\n## %s\n' "$1"
}

run_optional() {
  local label="$1"
  shift
  printf '\n### %s\n' "$label"
  if "$@"; then
    return 0
  fi
  local status=$?
  printf 'Command failed with exit %s: %q' "$status" "$1"
  shift || true
  for arg in "$@"; do
    printf ' %q' "$arg"
  done
  printf '\n'
  return 0
}

section "Host"
run_optional "hardware" system_profiler SPHardwareDataType SPPowerDataType

section "Parallels"
run_optional "prlctl version" prlctl --version
run_optional "prlsrvctl info" prlsrvctl info

section "VM"
run_optional "registered VMs" prlctl list --all --output name,status,ip,hostname
run_optional "VM info" prlctl list --all --info

state="$(prlctl list --all --no-header --output name,status | awk -v vm="$vm_name" '$0 ~ vm {print $NF; exit}')"
if [[ "${state:-}" != "running" ]]; then
  section "Guest"
  printf 'VM "%s" is "%s"; skipping guest command probes.\n' "$vm_name" "${state:-unknown}"
  exit 0
fi

section "Guest"
run_optional "current-user identity" prlctl exec "$vm_name" --current-user cmd /c whoami
run_optional "system identity" prlctl exec "$vm_name" cmd /c whoami
run_optional "Windows summary" prlctl exec "$vm_name" --current-user powershell -NoProfile -Command \
  'Get-ComputerInfo -Property CsName,WindowsProductName,WindowsVersion,OsArchitecture,CsTotalPhysicalMemory | ConvertTo-Json -Compress'
run_optional "volumes" prlctl exec "$vm_name" --current-user powershell -NoProfile -Command \
  'Get-Volume | Select-Object DriveLetter,FileSystemLabel,SizeRemaining,Size | ConvertTo-Json -Compress'
