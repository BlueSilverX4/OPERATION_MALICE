#!/usr/bin/env python3
"""
Operation M∀LICE - Phase 6: Response Orchestrator (Human-in-the-Loop)
Author: Brandon Lawrence Gregg (BlueSilverX4)
Function: Manages operator approval workflows for active containment and simulation rollbacks.
"""

import sys
import os
import subprocess
import logging

LOG_FILE = os.path.expanduser("~/Operation_MALICE/06_Red_Queen_Agent/orchestrator.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] Orchestrator: %(message)s"
)

def prompt_operator_action(rule_id, description):
    """Presents an interactive CLI prompt requiring explicit analyst authorization."""
    print("\n" + "="*60)
    print(" SECURITY ORCHESTRATION & AUTOMATION (SOAR) - GATEKEEPER")
    print("="*60)
    print(f" Alert Rule ID : {rule_id}")
    print(f" Description   : {description}")
    print("-" * 60)
    print(" Recommended Action: Isolate affected host / trigger containment.")
    print(" [1] APPROVE Containment (Isolate Network / Trigger Active Response)")
    print(" [2] EXECUTE Simulation Rollback (Restore Vault Files)")
    print(" [3] DENIED / ABORT (Log audit trail and exit)")
    print("="*60)

    choice = input("Enter operator decision [1/2/3]: ").strip()
    return choice

def execute_response(choice):
    """Executes corresponding operational defense scripts based on analyst choice."""
    if choice == "1":
        print("[+] Operator APPROVED containment protocol.")
        logging.info("Authorized containment execution.")
        # Path to previous phase containment script (adjust path if needed)
        target_script = os.path.expanduser("~/Operation_MALICE/04_Red_Ransom/active_isolate.py")
        if os.path.exists(target_script):
            subprocess.run(["python3", target_script])
        else:
            print("[*] Simulating network isolation: iptables rules applied to drop outbound C2.")
            logging.info("Simulated network isolation executed.")

    elif choice == "2":
        print("[+] Operator requested simulation rollback.")
        logging.info("Authorized simulation rollback execution.")
        target_script = os.path.expanduser("~/Operation_MALICE/04_Red_Ransom/sim_rollback.py")
        if os.path.exists(target_script):
            subprocess.run(["python3", target_script])
        else:
            print("[*] Simulating vault file restoration from secure snapshot.")
            logging.info("Simulated vault rollback executed.")

    else:
        print("[-] Action DENIED or aborted by security operator. No changes made.")
        logging.info("Operator denied or aborted containment action.")

if __name__ == "__main__":
    # Example standalone execution or hook entry point
    rule = sys.argv[1] if len(sys.argv) > 1 else "100081"
    desc = sys.argv[2] if len(sys.argv) > 2 else "MALLICE - Red Queen Ransomware Activity Detected"
    
    decision = prompt_operator_action(rule, desc)
    execute_response(decision)
