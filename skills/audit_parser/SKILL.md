---
name: audit_parser
description: "Your objective is to run deterministic data normalization over raw, multi-node log artifacts using the enhanced `canary_parser.py` pipeline. The script automatically discovers all harvested control plane log outputs inside your local `./logs/` folder and aggregates them into a..."
---
# Audit Parser & Knowledge Integration Mission
Your objective is to run deterministic data normalization over raw, multi-node log artifacts using the enhanced `canary_parser.py` pipeline. The script automatically discovers all harvested control plane log outputs inside your local `./logs/` folder and aggregates them into a unified structural graph database of Markdown notes inside your local Obsidian Vault folder (`./vault/`).

## 1. Input Verification & Workspace Preparation
Before executing the script, verify that your paths match your current execution repository directory exactly to avoid processing failures:
- **Target Engine Utility:** `./canary_parser.py`
- **Dynamic Ingest Source Boundary:** The relative directory `./logs/` must contain the timestamped audit log files harvested from the cluster nodes matching the layout pattern `*_audit.txt` (e.g., `control-plane-01_2026-06-14_audit.txt`).

### Streamlined Discovery Rule:
Do not create, rename, or patch symbolic links (such as `audit_full.log`) inside your workspace shell context. The updated script natively uses wildcard discovery engines to read, aggregate, and sort multi-master data directly from disk.

## 2. Execution Pipeline & Error Guardrails
1. Execute the script natively from your execution repository directory workspace:
   `python3 ./canary_parser.py`
2. **The Wiping Guard:** Note that the script automatically runs a `clear_old_vault()` routine that completely drops and recreates the vault subdirectories at `./vault/` to prevent historical data leakage across separate investigative assessments. Never manually create notes in the vault before running this script, as they will be deleted.
3. **Error Abort:** If the Python runtime yields any exception (e.g., `IndexError`, `KeyError`, `JSONDecodeError`), stop execution immediately. Do not attempt to alter the script logic. Return the raw stack trace inside an `ENVIRONMENT_BLOCK`.

## 3. Obsidian Vault Validation
After a successful run, the script natively generates your cross-node Obsidian file architecture. Verify that the files exist on disk without using intensive recursive tools (`ls -R` is strictly forbidden). Quickly confirm the presence of the following outputs:
- **Master Log:** `./vault/Master_Forensic_Timeline.md`
- **Graph Folders Created:** `Actors/`, `Pods/`, `Alerts/`, and `Verbs/` inside the relative path `./vault/`

## 4. State Reporting & Anti-Loop Gate
- Do not read or output the text contents of the generated markdown files or the compiled master timeline to the terminal interface screen.
- Provide a scannable status summary containing:
  - Confirmation of the successful creation of the master timeline tracking file: `./vault/Master_Forensic_Timeline.md`.
  - The final console message printed by the script confirming multi-node consolidation (e.g., "[+] Tier 1 Complete! Consolidated X multi-node distinct sequence intervals...").
