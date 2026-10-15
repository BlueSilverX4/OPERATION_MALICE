# Operation M∀LICE: Strategic Incident Report & Case Study
**Environment:** Hybrid Linux SOC / Bare-Metal Kali Telemetry Lab  
**Incident Classification:** Multi-Stage Ransomware & C2 Tunneling Simulation  
**Lead Security Analyst:** Brandon Lawrence Gregg (BlueSilverX4)  

---

## 1. Executive Summary

During a simulated breach scenario designated **Operation M∀LICE**, an advanced threat actor leveraging the **Red Queen** framework launched a multi-vector attack against local host infrastructure. The incident encompassed unauthorized privilege escalation, DNS-based Command & Control (C2) beaconing, automated ransomware deployment targeting critical data stores (`test_vault`), and an attempted infrastructure-level payload strike.

Defensive capabilities were validated using custom Wazuh SIEM detection rules, automated Python containment scripts (`active_isolate.py`), and post-incident forensic extraction (`triage_harvest.sh`). Full system recovery was achieved via automated cryptographic rollback (`sim_rollback.py`).

---

## 2. Attack Lifecycle & Detection Matrix

### Phase 1: Privilege Escalation — DigiPolice Detection (Rule 100001)
* **Activity:** Threat actor executed unauthorized `sudo` commands across terminal `pts/0` to enumerate system paths.
* **SIEM Trigger:** Wazuh Rule `100001` (Level 7) intercepted authentication logs in `/var/log/auth.log`, flagging elevated root access patterns under the `digipolice` group.

### Phase 2: DNS Tunneling — March Hare Beaconing (Rule 100050)
* **Activity:** Outbound egress queries were generated targeting synthetic C2 domain `malice-underground.local`.
* **SIEM Trigger:** Wazuh Rule `100050` (Level 10) matched DNS query pre-decoder strings, classifying the activity under `c2_beaconing` and `malice` threat categories.

### Phase 3: Automated Containment — FIM & Active Isolation (Rule 100081)
* **Activity:** Ransomware payloads attempted rapid file modification within `~/Operation_MALICE/04_Red_Ransom/test_vault`, appending `.locked` extensions.
* **Response Trigger:** File Integrity Monitoring (FIM) fired Rule `100081`, triggering `active_isolate.py` to immediately drop active socket connections via `iptables` boundary isolation.

### Phase 4: Forensics & Recovery — Triage & Vault Restoration
* **Activity:** Executed `triage_harvest.sh` to collect network state, system logs, and alert dumps. Automated restoration script `sim_rollback.py` decrypted and restored target files within `test_vault` to baseline operational state.

---

## 3. SIEM Detection Rule Architecture

```xml
<!-- Custom Wazuh Ruleset for Operation M∀LICE -->
<group name="malice,digipolice,c2_beaconing,">

  <!-- Phase 1: DigiPolice Root Execution -->
  <rule id="100001" level="7">
    <if_sid>5402</if_sid>
    <description>DigiPolice: Privileged root command execution detected</description>
    <group>digipolice,sudo,privilege_escalation</group>
  </rule>

  <!-- Phase 2: March Hare DNS C2 Tunneling -->
  <rule id="100050" level="10">
    <field name="full_log">malice-underground.local</field>
    <description>MALLICE - March Hare DNS Tunneling / C2 Beaconing Activity Detected</description>
    <mitre>
      <id>T1071.004</id>
    </mitre>
    <group>dns,malice,c2_beaconing</group>
  </rule>

  <!-- Phase 3: Red Queen Ransomware FIM Burst -->
  <rule id="100081" level="12">
    <field name="full_log">\.locked$</field>
    <description>MALLICE - Red Queen Ransomware Activity Detected in Vault</description>
    <group>fim,malice,ransomware</group>
  </rule>

</group>

4. Operational Climax: Narrative Case Study
Incident Climax File: 04_Red_Ransom/climax_log.txt

Status: RESOLVED — Final Threat Eradication
