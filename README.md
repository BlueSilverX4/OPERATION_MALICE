# 🛡️ Operation M∀LICE: Cyberse Triage & SecOps Response Framework

**Author:** Brandon Lawrence Gregg (BlueSilverX4)  
**Framework Alignment:** NIST Cybersecurity Framework (CSF) 2.0 · MITRE ATT&CK  
**Platform:** Kali Linux · Wazuh SIEM · Zeek · Python · Optional Ollama LLM  
**Thematic Foundation:** Inspired by the Yu-Gi-Oh! *M∀LICE* archetype, blending *Alice in Wonderland* imagery with malicious Cyberse code.

---

## 📋 Executive Overview

**Operation M∀LICE** is a modular Security Operations Center (SOC) lab simulation designed to demonstrate threat investigation, security telemetry analysis, incident triage, and controlled response orchestration.

Built around Kali Linux and Wazuh SIEM, the framework models a threat lifecycle spanning encoded stager analysis, command-and-control (C2) network investigation, simulated ransomware detection, containment workflows, and AI-assisted alert triage.

The **Red Queen Agent** serves as the central triage component, combining rule-based analysis with optional local Large Language Model (LLM) assistance through Ollama. A human-in-the-loop (HITL) authorization gate keeps consequential response actions under analyst control.

### Core Capabilities

- **Threat Analysis:** Base64 extraction, stager deobfuscation, and CyberChef-assisted investigation.
- **Network Detection:** PCAP analysis, Zeek telemetry, DNS investigation, and custom Wazuh rules.
- **Endpoint Monitoring:** File Integrity Monitoring (FIM) and controlled ransomware simulation.
- **Incident Containment:** Isolation workflows, socket termination, and webhook-based communication.
- **AI-Assisted Triage:** Rule-based findings with optional local LLM enrichment and fallback behavior.
- **Human-Approved Response:** Analyst authorization before simulated recovery or containment actions.

---

## 🧭 Laboratory Phase Architecture

### Phase 01 — White Binder
**Directory:** `01_White_Binder/`  
**Theme:** M∀LICE White Rabbit — Initial Trace

**Objectives:**
- Extract and inspect encoded threat artifacts.
- Deobfuscate PowerShell stagers for defensive analysis.
- Develop CyberChef recipes to document repeatable decoding workflows.

**Key Assets:**
- `decoded_stager_01.ps1`
- Base64 extraction and analysis workflows.

### Phase 02 — Environment Baseline
**Directory:** `02_Environment/`

**Objectives:**
- Establish a consistent lab baseline.
- Configure directory permissions and telemetry paths.
- Prepare Wazuh agent registration and log collection.
- Validate prerequisites before executing subsequent phases.

### Phase 03 — March Hare
**Directory:** `03_March_Hare/`  
**Theme:** M∀LICE March Hare — C2 Network Telemetry

**Objectives:**
- Analyze packet captures for suspicious network behavior.
- Investigate Zeek connection and DNS records.
- Correlate network indicators with Wazuh alerts.
- Develop custom DNS detection rules.

**Key Assets:**
- `march_hare_c2.pcap`
- `wazuh_march_hare_dns.xml`
- Zeek telemetry: `conn.log` and `dns.log`

### Phase 04 — Red Ransom
**Directory:** `04_Red_Ransom/`  
**Theme:** M∀LICE RED RANSOM — File-Encryption Simulation

**Objectives:**
- Simulate file-encryption activity in a controlled test environment.
- Detect suspicious file changes through Wazuh File Integrity Monitoring.
- Validate custom detection rule `100081`.
- Exercise recovery procedures against designated test artifacts.

**Key Assets:**
- `sim_ransom.py`
- `sim_rollback.py`
- `wazuh_red_ransom.xml`
- `INCIDENT_REPORT.md`

**Safety Boundary:** Ransomware behavior is intended for isolated lab testing against designated test files, not production systems or real user data.

### Phase 05 — Underground Isolation
**Directory:** `05_Underground_Isolation/`  
**Theme:** Down the Rabbit Hole — Containment Realm

**Objectives:**
- Exercise active-response and network-isolation workflows.
- Investigate socket termination as a containment mechanism.
- Implement webhook receivers for response notifications.
- Validate containment behavior before considering operational deployment.

**Key Assets:**
- `active_isolate.py`
- `webhook_receiver.py`

**Operational Guardrail:** Network isolation and socket termination can disrupt connectivity. Validate these actions in the lab and require appropriate authorization before use.

### Phase 06 — Red Queen Agent
**Directory:** `06_Red_Queen_Agent/`  
**Theme:** M∀LICE RED QUEEN — SecOps Intelligence & Orchestration

**Objectives:**
- Ingest Wazuh JSON alert payloads.
- Generate rule-based triage findings.
- Support optional local Ollama LLM analysis.
- Preserve fallback behavior when the LLM is unavailable.
- Require explicit analyst authorization before consequential response actions.

**Key Assets:**

| Component | Responsibility |
|---|---|
| `red_queen_listener.py` | Receives and processes Wazuh alert JSON payloads. |
| `ai_engine.py` | Performs rule-based triage with optional LLM assistance and fallback support. |
| `response_orchestrator.py` | Presents response options and requests explicit analyst authorization. |

**Human-in-the-Loop (HITL):** The analyst remains the decision-maker. AI-generated findings are advisory and should be validated against the available evidence before a response is authorized.

---

## 🧪 Execution & Verification

Run these commands from the project root:

```bash
cd ~/Operation_MALICE
```

### 1. Validate Python Syntax

```bash
python3 -m py_compile \
  06_Red_Queen_Agent/ai_engine.py \
  06_Red_Queen_Agent/red_queen_listener.py \
  06_Red_Queen_Agent/response_orchestrator.py

echo "Exit code: $?"
```

An exit code of `0` indicates that the listed Python files passed syntax compilation.

### 2. Test Red Queen Alert Ingestion

Pipe a representative Wazuh-style JSON alert into the listener:

```bash
printf '%s\n' '{
  "rule": {
    "id": "100081",
    "level": 12,
    "description": "MALICE - Red Queen Ransomware Activity Detected in Vault"
  },
  "agent": {
    "name": "kali"
  },
  "full_log": "File ~/Operation_MALICE/04_Red_Ransom/test_vault/data.docx.locked created"
}' | python3 06_Red_Queen_Agent/red_queen_listener.py
```

**Verification goal:** Confirm that the listener accepts the JSON payload and passes the alert into the intended triage workflow.

Actual results depend on the listener implementation and its configured inputs.

### 3. Launch the Response Orchestrator

```bash
python3 06_Red_Queen_Agent/response_orchestrator.py
```

**Verification goal:**
- Confirm that the orchestrator presents the available response choices.
- Verify that the analyst must explicitly authorize a consequential action.
- Confirm that an unapproved action is not executed.
- Validate containment and rollback behavior only against designated lab resources.

### 4. Verify the Local AI Integration

If Ollama integration is enabled, check whether the local service responds:

```bash
ollama list
```

If the service is unavailable or a model request times out, verify the configured model name, service availability, and timeout settings. Confirm that the rule-based fallback remains functional when LLM assistance cannot complete.

---

## 🛡️ Security & Operational Boundaries

Operation M∀LICE is a defensive lab and portfolio project.

- Use isolated, authorized test environments for all simulations.
- Keep test data separate from personal or production files.
- Validate detection results against logs and other available evidence.
- Treat AI-generated analysis as advisory rather than authoritative.
- Require explicit human approval for disruptive containment or recovery actions.
- Document test conditions, observed alerts, response decisions, and recovery outcomes.
- Do not interpret a successful syntax check as proof that runtime behavior or security controls are working correctly.

---

## 📚 Framework Alignment

The lab supports practical learning objectives associated with:

- **NIST CSF 2.0 — Detect:** Analyze security events and identify potentially malicious activity.
- **NIST CSF 2.0 — Respond:** Investigate alerts, coordinate response decisions, and exercise containment workflows.
- **NIST CSF 2.0 — Recover:** Test restoration procedures and document recovery outcomes.
- **MITRE ATT&CK:** Organize observed behaviors and detection logic around relevant adversary techniques when supported by the evidence.

These are project-level alignment goals, not a claim of formal framework certification or complete control coverage.

---

## 🚀 Project Goals

Operation M∀LICE demonstrates a practical progression from raw security artifacts to analyst-reviewed response:

**Analyze → Detect → Triage → Authorize → Respond → Validate Recovery**

The objective is to connect detection engineering, SIEM telemetry, Python automation, local AI assistance, and disciplined human decision-making in a single modular SOC lab.

---

*Maintained by Brandon Lawrence Gregg (BlueSilverX4).*
```
