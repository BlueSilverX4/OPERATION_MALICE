cat << 'EOF' > ~/Operation_MALICE/04_Red_Ransom/AUTOMATION_TECH_SPEC.md
# Operation M∀LICE: Custom SOC Automation Architecture

This document outlines the technical design, operational execution flow, and safety mechanics of the custom Python automation suite deployed during **Operation M∀LICE**. These scripts interface directly with the Wazuh Active Response engine and local Linux kernel utilities (`iptables`, `syscheck`) to achieve real-time boundary containment and zero-data-loss recovery.

---

## 1. Active Isolation Engine (`active_isolate.py`)

### Purpose & SOC Context
`active_isolate.py` serves as the automated containment arm of the SOC. When Wazuh File Integrity Monitoring (FIM) detects rapid `.locked` file creations (Rule `100081`), the manager triggers this script via Active Response to sever all non-essential socket connections, halting ransomware Command & Control (C2) exfiltration and lateral movement.

### Operational Mechanics

[ FIM Alert: Rule 100081 ]│▼[ Wazuh Active Response ] ─────> Runs: active_isolate.py│├─► Parses STDIN JSON payload├─► Flushes non-essential iptables rules├─► Enforces DROP policy on inbound/outbound└─► Appends audit log to active-responses.log
### Key Python Implementation

```python
#!/usr/bin/env python3
"""
Operation M∀LICE - Automated Boundary Containment Engine
Author: Brandon Lawrence Gregg (BlueSilverX4)
Function: Enforces immediate network isolation via iptables upon FIM ransomware alert.
"""

import sys
import json
import subprocess
import logging

LOG_FILE = "/var/ossec/logs/active-responses.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] M∀LICE-ActiveIsolate: %(message)s"
)

def apply_network_isolation():
    """Applies kernel-level socket block using iptables while maintaining loopback."""
    try:
        # Flush existing rules to prevent conflicts
        subprocess.run(["sudo", "iptables", "-F"], check=True)
        
        # Ensure loopback traffic remains open for local log collection
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], check=True)
        subprocess.run(["sudo", "iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], check=True)

        # Drop all standard external IPv4 egress/ingress traffic
        subprocess.run(["sudo", "iptables", "-P", "INPUT", "DROP"], check=True)
        subprocess.run(["sudo", "iptables", "-P", "OUTPUT", "DROP"], check=True)

        logging.info("CONTAINMENT SUCCESS: Boundary isolation enforced via iptables.")
        print("[+] Operation M∀LICE: Active Boundary Containment Deployed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"CONTAINMENT FAILURE: Failed to apply iptables rules - {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Standard Active Response STDIN handling
    try:
        input_str = sys.stdin.read()
        if input_str:
            alert_data = json.loads(input_str)
            rule_id = alert_data.get("parameters", {}).get("alert", {}).get("rule", {}).get("id")
            logging.info(f"Triggered by Rule ID: {rule_id}")
    except Exception as err:
        logging.warning(f"Could not parse STDIN JSON (Manual execution mode): {err}")

    apply_network_isolation()
Forensic Features & ResilienceLoopback Exemption (-i lo): Keeps local IPC (Inter-Process Communication) alive so the local Wazuh agent can continue reading system telemetry while external network sockets are blocked.Audit Trail Synchronization: Logs execution timestamps and triggered Rule IDs directly into /var/ossec/logs/active-responses.log for forensic correlation.2. Vault Automated Rollback Engine (sim_rollback.py)Purpose & SOC ContextFollowing an active ransomware simulation, sim_rollback.py handles post-incident remediation. It scans target directories (test_vault) for host files appended with simulated encryption extensions (.locked) and restores original file handles safely without damaging file header metadata.Operational Mechanics           [ Directory: ~/test_vault/ ]
                        │
                        ▼
            [ Execute: sim_rollback.py ]
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
 [ Found: *.locked ]           [ No .locked Files ]
       │                                 │
       ├─► Strip extension               └─► Log: Vault Pristine
       ├─► os.rename()
       └─► Restore original state
Key Python ImplementationPython#!/usr/bin/env python3
"""
Operation M∀LICE - Vault Automated Cryptographic Rollback & Restoration
Author: Brandon Lawrence Gregg (BlueSilverX4)
Function: Reverts ransomware extension modifications within test_vault to restore baseline.
"""

import os
import glob
import sys

VAULT_DIR = os.path.expanduser("~/Operation_MALICE/04_Red_Ransom/test_vault")

def execute_vault_rollback():
    """Identifies .locked files in target directory and restores original extensions."""
    print(f"[*] Starting M∀LICE Automated Rollback in target vault: {VAULT_DIR}")
    
    if not os.path.exists(VAULT_DIR):
        print(f"[!] Target vault path '{VAULT_DIR}' does not exist.")
        sys.exit(1)

    locked_files = glob.glob(os.path.join(VAULT_DIR, "*.locked"))
    
    if not locked_files:
        print("[-] No .locked files detected. Vault is in baseline pristine state.")
        return

    restored_count = 0
    for filepath in locked_files:
        # Strip the trailing .locked extension safely from the right
        original_path = filepath.rsplit(".locked", 1)[0]
        try:
            os.rename(filepath, original_path)
            print(f"[+] Restored: {os.path.basename(filepath)} -> {os.path.basename(original_path)}")
            restored_count += 1
        except OSError as err:
            print(f"[!] Error restoring {filepath}: {err}")

    print(f"[*] Rollback complete. Total files restored: {restored_count}/{len(locked_files)}")

if __name__ == "__main__":
    execute_vault_rollback()
Safety Mechanics & DefensesNon-Destructive In-Place Rename: Uses os.rename() at the atomic system-call level to preserve file inode metadata and access permissions.Target Path Isolation: Hardcoded scope limits operations exclusively to ~/Operation_MALICE/04_Red_Ransom/test_vault, eliminating risk to system-critical user directories.3. Automation Integration MatrixTool / ScriptTrigger MechanismTarget / ScopeOperational Outputactive_isolate.pyWazuh Active Response (FIM Rule 100081)Kernel Network Stack (iptables)Enforces DROP policy on external interface socketstriage_harvest.shManual / SOC Analyst Post-IncidentNetwork state, syslog, JSON alertsBundles timestamped triage_YYYYMMDD_HHMMSS evidencesim_rollback.pyManual Remediation Sequencetest_vault/*.lockedRestores original filenames & clears ransomware status
