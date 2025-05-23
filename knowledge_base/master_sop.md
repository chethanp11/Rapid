# 📘 Master SOP – Controls Development COE

This SOP defines the standard for designing, documenting, executing, and reviewing operational risk controls.

---

## Section 1: Control Design

- Each control must have a **Control ID**, description, owner, frequency, and intended risk mitigation.
- All design decisions must be supported by:
  - A requirement document
  - Supporting data flows or architecture
  - Approval from business and 2LoD

---

## Section 2: Control Execution

- Execution logs must be retained for a **minimum of 6 months**.
- Manual controls should be logged in spreadsheets or tools that can track:
  - Date
  - Executor
  - Break or exception
  - Outcome
- Automated controls should output logs or reconciliation results daily.

---

## Section 3: Control Review and Signoff

- Controls must be reviewed by an assigned reviewer weekly/monthly/quarterly (as defined).
- Reviewer must:
  - Validate completeness
  - Sign off via email or control portal
  - Escalate unresolved exceptions

---

## Section 4: Exception Handling & Escalation

- Any control deviation (missed execution, unresolved break) must be escalated as per the severity:
  - **48-hour unresolved break** → Escalate to Ops Head
  - **3+ repeated exceptions** → Notify Risk COE
- All escalations should be documented via email and attached to the audit log.

---

## Section 5: Evidence Guidelines

- Artifacts required for each audit cycle include:
  - `recon_log.csv` or equivalent log file
  - Approval emails (`email.txt`)
  - Notes or comments from `notes.txt`
  - Any SOP references used during response (`master_sop.md`)