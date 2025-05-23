# 🚀 RAPID — RFI Assistant for Projects, Insights & Documents

RAPID is a smart assistant for **Controls Development Teams** to respond to **Audit RFIs** using actual project artifacts and control documentation.  
It combines a document-aware LLM, role mappings, SOPs, and contextual prompts to generate fast, defensible audit responses.

---

## 🎯 What It Does

- Accepts RFIs submitted by Audit with project linkage
- Indexes uploaded artifacts (emails, logs, code, docs)
- Matches RFI to patterns and reasoning logic
- Generates draft responses using OpenAI GPT-4o
- Tracks submission, review, and audit trail

---

## 📦 Folder Structure

```
Rapid/
├── config/                 # Config YAML
├── core/                  # Indexer, Engine, RFI Manager
├── data/                  # RFI store, response log, audit trail
├── frontend/              # Streamlit interface
├── knowledge_base/        # Glossaries, templates, SOPs
├── projects/              # Project-specific artifacts
├── utils/                 # File and LLM utilities
└── README.md
```

---

## ⚙️ How to Run

1. Add your OpenAI key to `.env` in `FinanceAI/config/`
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the frontend:  
   ```bash
   streamlit run Rapid/frontend/app.py
   ```

---

## 🧪 Sample Use Case

> RFI: "Please provide evidence of how daily Nostro breaks are reviewed and escalated."

RAPID loads:
- `recon_log.csv`
- `notes.txt`
- `email.txt`
- `requirement.docx`

...and generates a traceable, formatted response citing the SOP and attached files.

---

## ✅ Status

✔️ Working MVP with full project-specific context injection  
🔜 Future features: multiple roles, approval routing, PDF previews

---

Built for teams who need speed, traceability, and audit-readiness in responding to RFIs.