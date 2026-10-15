#!/usr/bin/env python3
"""
Operation M∀LICE - Unified Attack Simulation Harness (2026 SOC Lab)
Simulates end-to-end kill chain telemetry across all 5 operational phases.
"""

import time
import os
import sys
import json
import urllib.request
import datetime

# Directory Paths
BASE_DIR = os.path.expanduser("~/Operation_MALICE")
SECTOR_01_DIR = os.path.join(BASE_DIR, "01_White_Binder/samples")
SECTOR_03_DIR = os.path.join(BASE_DIR, "03_March_Hare/zeek_logs")
SECTOR_04_DIR = os.path.join(BASE_DIR, "04_Red_Ransom/logs")
SECTOR_05_DIR = os.path.join(BASE_DIR, "05_Underground_Isolation")

def print_status(phase, msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\031[1;36m[{timestamp}] [{phase}]\033[0m {msg}")

def run_simulation():
    print("\n========================================================")
    print("      OPERATION M∀LICE - KILL CHAIN SIMULATOR           ")
    print("========================================================\n")

    # Phase 1: White Binder (Stager Ingestion)
    print_status("01_White_Binder", "Deploying obfuscated PowerShell stager artifact...")
    os.makedirs(SECTOR_01_DIR, exist_ok=True)
    stager_path = os.path.join(SECTOR_01_DIR, "simulated_stager.ps1")
    with open(stager_path, "w") as f:
        f.write("# M∀LICE Stager Payload\n$b = [System.Convert]::FromBase64String('aHR0cDovL21hbGljZS1jMi5pbnRlcm5hbC9zdGFnZXI=')\n")
    print_status("01_White_Binder", f"Artifact created at: {stager_path}")
    time.sleep(1)

    # Phase 2: Environment (Telemetry Baseline)
    print_status("02_Environment", "Verifying baseline telemetry directories and active bindings...")
    time.sleep(1)

    # Phase 3: March Hare (C2 DNS Beaconing)
    print_status("03_March_Hare", "Simulating malicious DNS queries in Zeek dns.log...")
    os.makedirs(SECTOR_03_DIR, exist_ok=True)
    zeek_dns = os.path.join(SECTOR_03_DIR, "dns.log")
    ts = time.time()
    dns_entry = f"{ts}\tC123456789\t192.168.56.100\t5353\t8.8.8.8\t53\tudp\t1234\tc2.malice-network.internal\t1\tC_INTERNET\t1\tA\t0\tNOERROR\tF\tF\tF\tF\t0\t192.168.56.10\n"
    with open(zeek_dns, "a") as f:
        f.write(dns_entry)
    print_status("03_March_Hare", "Logged C2 query: 'c2.malice-network.internal' from 192.168.56.100")
    time.sleep(1)

    # Phase 4: Red Ransom (Volume Shadow Copy Deletion)
    print_status("04_Red_Ransom", "Simulating T1490 (Inhibit System Recovery / Vssadmin Deletion)...")
    os.makedirs(SECTOR_04_DIR, exist_ok=True)
    ransom_log = os.path.join(SECTOR_04_DIR, "sysmon_events.log")
    sysmon_entry = f"{datetime.datetime.now().isoformat()} WinEvtLog: Sysmon Event ID 1: Process Create: CommandLine: vssadmin.exe delete shadows /all /quiet\n"
    with open(ransom_log, "a") as f:
        f.write(sysmon_entry)
    print_status("04_Red_Ransom", "Logged process creation: 'vssadmin.exe delete shadows'")
    time.sleep(1)

    # Phase 5: Underground Isolation (Active Response & Webhook Alerting)
    print_status("05_Underground_Isolation", "Triggering host isolation script for 192.168.56.100...")
    isolate_script = os.path.join(SECTOR_05_DIR, "scripts/active_isolate.py")
    if os.path.exists(isolate_script):
        os.system(f"python3 {isolate_script} 192.168.56.100")
    else:
        print_status("05_Underground_Isolation", "[!] active_isolate.py not found, skipping local iptables step.")

    print_status("05_Underground_Isolation", "Dispatching alert payload to Webhook listener (Port 5000)...")
    payload = {
        "rule_id": 100051,
        "severity": 12,
        "description": "MALLICE - Red Ransom Shadow Copy Deletion Detected",
        "src_ip": "192.168.56.100",
        "mitre_id": "T1490",
        "action": "HOST_ISOLATED"
    }
    
    try:
        req = urllib.request.Request(
            "http://localhost:5000/alert",
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print_status("05_Underground_Isolation", "Webhook alert delivered successfully (HTTP 200).")
    except Exception as e:
        print_status("05_Underground_Isolation", f"[!] Webhook delivery failed (Is listener running?): {e}")

    print("\n========================================================")
    print("      SIMULATION COMPLETE - KILL CHAIN LOGGED          ")
    print("========================================================\n")

if __name__ == "__main__":
    run_simulation()
