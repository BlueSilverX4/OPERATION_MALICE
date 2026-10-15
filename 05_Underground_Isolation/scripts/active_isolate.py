#!/usr/bin/env python3
import sys
import subprocess
import datetime

LOG_FILE = "/home/brandongregg/Operation_MALICE/05_Underground_Isolation/logs/active_response.log"

def log_message(msg):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def block_ip(ip):
    cmd = f"sudo iptables -A INPUT -s {ip} -j DROP"
    try:
        subprocess.run(cmd, shell=True, check=True)
        log_message(f"[SUCCESS] Isolated malicious host IP: {ip} via iptables.")
    except Exception as e:
        log_message(f"[ERROR] Failed to isolate {ip}: {str(e)}")

if __name__ == "__main__":
    log_message("[INIT] M∀LICE Active Response Executed by Wazuh Manager.")

    if len(sys.argv) > 1:
        target_ip = sys.argv[1]
        block_ip(target_ip)
    else:
        target_ip = "192.168.56.10"
        block_ip(target_ip)
