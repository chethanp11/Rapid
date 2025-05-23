# ✅ Example RFI Response

## 📌 RFI Title:
Evidence of Nostro Break Review

## 📝 Description:
Please provide documentation and proof that daily Nostro breaks are being reviewed and escalated.

---

## 📄 Draft Response

This control (`CTRL-ID: NOSTRO-DAILY-001`) is executed as a **daily detective control** to identify unposted items and cash breaks across Nostro accounts.

Breaks are logged in **`recon_log.csv`**, under the `"Daily Summary"` tab with fields such as:
- Break ID
- Value Date
- Currency
- Root Cause
- Resolution Action
- Escalation Trigger

For Q1 2025, the control was executed daily and reviewed by the Payments Lead (**Ajay Kumar**). Approval was documented via **`email.txt`**, dated **Jan 4, 2025**.

Exceptions breaching the 48-hour policy were escalated according to section **3.4** of the SOP (**`master_sop.md`**). No material breaches or delayed remediations were noted during this period.

---

## 📎 Attached Artifacts

- `recon_log.csv`
- `email.txt`
- `notes.txt`
- `master_sop.md` (referenced from KB)