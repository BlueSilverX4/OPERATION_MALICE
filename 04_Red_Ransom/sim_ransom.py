#!/usr/bin/env python3
import os
import time
from pathlib import Path

# Target strictly the local test_vault sandbox
VAULT_DIR = Path.home() / "Operation_MALICE/04_Red_Ransom/test_vault"

def simulate_encryption():
    print(f"[*] Executing M∀LICE Ransomware Simulation targeting: {VAULT_DIR}")
    if not VAULT_DIR.exists():
        print(f"[!] Error: Target directory {VAULT_DIR} does not exist!")
        return

    for file_path in VAULT_DIR.glob("*"):
        if file_path.is_file() and not file_path.name.endswith(".locked"):
            print(f"[+] Encrypting/Renaming: {file_path.name}")
            
            # Append payload marker without touching system files
            with open(file_path, "a") as f:
                f.write("\n[ENCRYPTED_HEADER_MALICE_TEST_PAYLOAD]")
            
            # Change extension to trigger Sysmon/Auditd FileRename telemetry
            new_name = file_path.with_suffix(file_path.suffix + ".locked")
            file_path.rename(new_name)
            time.sleep(0.5)

    print("[*] Simulation complete. Test vault payload modifications applied.")

if __name__ == "__main__":
    simulate_encryption()
