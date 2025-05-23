# 🛡️ RAPID – Risk & Audit Partner for Insights & Documentation

**RAPID** is a smart assistant built for **Controls Development and Risk Oversight teams** to streamline the **RFI (Request for Information)** response process during audits.

Designed for banking environments, RAPID connects control documentation, project artifacts, and institutional knowledge to create audit-ready responses with speed, structure, and evidence.

---

## 🎯 Why RAPID?

Audit cycles are frequent, and RFIs often require context from multiple systems and teams. RAPID reduces this burden by:

- Connecting project-specific evidence (emails, logs, SOPs, design docs)
- Interpreting RFIs using proven reasoning templates
- Producing clear, defensible responses — ready for audit review
- Maintaining a traceable history of responses for governance

---

## 💼 Who It's For

- **Controls Development Teams**  
- **Operational Risk Officers**  
- **Internal Audit Liaisons**  
- **Technology Control Owners**  

Whether it's proving a control was executed or justifying its design logic, RAPID brings clarity and structure to every response.

---

## 🔍 How It Works

1. **Audit submits an RFI**, linked to a specific control project  
2. RAPID **scans relevant project artifacts** like `.csv`, `.py`, `.docx`, and email logs  
3. It **matches the RFI** against control categories (design gap, evidence gap, ownership, etc.)  
4. A structured response is **auto-generated** using OpenAI GPT-4o — citing real evidence  
5. Control owners can **review, submit, return, or revise** responses within the tool

---

## 🧪 Sample Use Case

> **Audit RFI:**  
> _"Please provide evidence of how daily Nostro breaks are reviewed and escalated."_  

RAPID automatically references:
- `recon_log.csv` → showing daily break entries  
- `notes.txt` → outlining escalation policy  
- `email.txt` → confirming a review delay and approval  
- `requirement.docx` → stating the expected control behavior  

And generates a clear, factual response with citations.

---

## 📁 Folder Overview

Rapid/
├── config/                 # Runtime paths and secrets
├── core/                  # Context indexer, response engine, RFI manager
├── data/                  # RFI storage and response audit trail
├── frontend/              # Streamlit UIs for Audit & Respond users
├── knowledge_base/        # SOPs, glossary, QA checklists, templates
├── projects/              # Uploaded project artifacts
├── utils/                 # File/LLM helpers
└── README.md

## ⚙️ How to Run
Add your OpenAI key to .env in FinanceAI/config/
Install dependencies:
pip install -r requirements.txt

# You can also run dedicated UIs:

---
    •	Audit Portal:
streamlit run Rapid/frontend/audit_ui_app.py

---
	•	Response App:
streamlit run Rapid/frontend/respond_ui_app.py


## ✅ What’s Working Now
	•	✅ End-to-end RFI intake to response generation
	•	✅ Project-based file indexing (code, logs, docs, notes)
	•	✅ Pattern-matched reasoning template (design, execution, ownership)
	•	✅ LLM prompt assembly with real context
	•	✅ Response visibility and audit trail
	•	✅ Status markers: pending, accepted, returned

## 🔮 What’s Coming Next
	•	🔁 Reviewer workflows (approval/return escalation)
	•	📥 Upload interface for new artifacts
	•	📄 PDF preview support
	•	📊 RFI dashboard and audit summary exports

## 🏦 Why This Matters

Controls and risk teams often spend hours finding scattered evidence to justify control behavior. RAPID compresses that into minutes — while improving traceability, audit defensibility, and internal confidence.

“If you’ve ever scrambled during an audit to find that one email or escalation note — RAPID is built for you.”
— Controls Lead, Global Bank

## 🧪 Sample Use Case
RFI: "Please provide evidence of how daily Nostro breaks are reviewed and escalated."

RAPID loads:

recon_log.csv
notes.txt
email.txt
requirement.docx
...and generates a traceable, formatted response citing the SOP and attached files.


Built with ❤️ for high-integrity financial environments.
---

Let me know if you'd like a one-liner badge (e.g. ✅ Audit-Ready | 🔁 LLM-Based | 📂 Traceable) or demo screenshot block.
