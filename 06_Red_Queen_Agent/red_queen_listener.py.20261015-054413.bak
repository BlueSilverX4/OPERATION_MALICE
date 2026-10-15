#!/usr/bin/env python3
"""
Operation M∀LICE - Phase 6: Red Queen AI SecOps Agent Listener
Author: Brandon Lawrence Gregg (BlueSilverX4)
Function: Listens for Wazuh SIEM JSON alerts and feeds them to local AI triage engine.
"""

import sys
import os
import json
import logging
from ai_engine import analyze_alert_with_llm

# Fall back to local module log file if /var/ossec/logs/ isn't writable
PRIMARY_LOG = "/var/ossec/logs/red_queen_agent.log"
LOCAL_LOG = os.path.expanduser("~/Operation_MALICE/06_Red_Queen_Agent/red_queen_agent.log")

LOG_FILE = PRIMARY_LOG if os.access("/var/ossec/logs", os.W_OK) else LOCAL_LOG

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] RedQueen-Agent: %(message)s"
)

def process_incoming_alert():
    """Reads JSON payload from stdin (Wazuh active response / integration runner)."""
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            logging.warning("Received empty alert payload.")
            return

        alert_data = json.loads(raw_input)
        
        # Extract key metadata fields
        rule_id = alert_data.get("rule", {}).get("id", "UNKNOWN")
        rule_desc = alert_data.get("rule", {}).get("description", "No description")
        level = alert_data.get("rule", {}).get("level", 0)
        full_log = alert_data.get("full_log", "")
        agent_name = alert_data.get("agent", {}).get("name", "kali")

        logging.info(f"Ingested Alert ID: {rule_id} | Level: {level} | Description: {rule_desc}")
        
        # Dispatch payload to local Ollama LLM engine
        triage_report = analyze_alert_with_llm(rule_id, level, rule_desc, full_log, agent_name)
        
        print("\n" + "="*60)
        print(" RED QUEEN AI AGENT: INCIDENT TRIAGE REPORT")
        print("="*60)
        print(triage_report)
        print("="*60 + "\n")

    except json.JSONDecodeError as err:
        logging.error(f"Failed to parse JSON alert input: {err}")
    except Exception as err:
        logging.error(f"Unexpected error during alert ingestion: {err}")

if __name__ == "__main__":
    process_incoming_alert()
