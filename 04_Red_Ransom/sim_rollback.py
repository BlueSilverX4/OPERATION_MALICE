#!/usr/bin/env python3
import os
import glob
import sys

VAULT_DIR = os.path.expanduser("~/Operation_MALICE/04_Red_Ransom/test_vault")

def rollback():
    print(f"[*] Starting M∀LICE Automated Rollback in: {VAULT_DIR}")
    locked_files = glob.glob(os.path.join(VAULT_DIR, "*.locked"))
    
    if not locked_files:
        print("[-] No .locked files detected for restoration.")
        return

    for filepath in locked_files:
        original_path = filepath.rsplit(".locked", 1)[0]
        os.rename(filepath, original_path)
        print(f"[+] Restored: {os.path.basename(filepath)} -> {os.path.basename(original_path)}")

    print("[*] Rollback successful. Target vault restored to pristine state.")

if __name__ == "__main__":
    rollback()
