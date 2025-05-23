# --- 📁 Path Setup ---
import sys, os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FINANCEAI_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if FINANCEAI_ROOT not in sys.path:
    sys.path.insert(0, FINANCEAI_ROOT)

# --- 🔁 Imports ---
import streamlit as st
import json
from datetime import datetime
from core.rfi_manager import load_rfis, filter_rfis_by_project
from core.response_engine import generate_rfi_response
from config.pyenv import get_path  # ✅ Refers to FinanceAI/config/pyenv.py

# --- 💾 Save Response History ---
def save_response_history(new_entry: dict):
    path = os.path.join(get_path("RAPID_DATA_PATH"), "response_history.json")
    try:
        with open(path, "r") as f:
            existing = json.load(f)
    except:
        existing = []

    updated = False
    for idx, item in enumerate(existing):
        if item.get("rfi_id") == new_entry.get("rfi_id"):
            existing[idx] = new_entry
            updated = True
            break
    if not updated:
        existing.append(new_entry)

    with open(path, "w") as f:
        json.dump(existing, f, indent=2)

# --- 🎨 UI Setup ---
st.set_page_config(page_title="RAPID – Respond to RFIs", page_icon="🛠️", layout="wide")
st.markdown("<h1 style='color:#4CAF50;'>🛠️ RAPID – Respond to RFIs</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-style: italic; color: gray;'>RAPID = RFI Assistant for Projects, Insights & Documents</p>", unsafe_allow_html=True)

# --- Load Data ---
all_rfis = load_rfis()
if not all_rfis:
    st.info("📭 No RFIs available.")
else:
    project_filter = st.selectbox("📁 Filter by Project", sorted(set(r["project_id"] for r in all_rfis)))
    filtered = filter_rfis_by_project(project_filter)

    # Load response history
    response_path = os.path.join(get_path("RAPID_DATA_PATH"), "response_history.json")
    try:
        with open(response_path, "r") as f:
            response_history = json.load(f)
    except:
        response_history = []

    for rfi in filtered:
        rfi_id = rfi["rfi_id"]
        st.markdown(f"---\n### 🔖 `{rfi_id}` — {rfi['title']}")
        st.markdown(f"**📌 Project:** `{rfi['project_id']}`")
        st.markdown(f"**📝 Description:** {rfi['description']}")
        st.markdown(f"**👤 Submitted by:** `{rfi['submitted_by']}` | **🎯 Priority:** `{rfi.get('priority', 'Medium')}`")

        output_key = f"output_{rfi_id}"
        show_key = f"show_{rfi_id}"
        ctx_key = f"ctx_{rfi_id}"
        submitted_key = f"submitted_{rfi_id}"

        # Load from history if not already loaded
        if output_key not in st.session_state:
            from_history = next((item for item in response_history if item.get("rfi_id") == rfi_id), None)
            if from_history:
                st.session_state[output_key] = from_history
                st.session_state[submitted_key] = True
            else:
                st.session_state[submitted_key] = False

        output = st.session_state.get(output_key)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🧠 Generate Response", key=f"gen_{rfi_id}"):
                with st.spinner("💬 Thinking..."):
                    output = generate_rfi_response(rfi)
                st.session_state[output_key] = {
                    "rfi_id": rfi_id,
                    "response": output["response"],
                    "context_used": output.get("context_used", ""),
                    "template_used": output.get("template_used", ""),
                    "category": output.get("category", ""),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
                st.session_state[show_key] = True
                st.session_state[submitted_key] = False
                st.success("✅ Draft response generated. Submit when ready.")

        with col2:
            if st.button("📄 View Response", key=f"view_{rfi_id}"):
                st.session_state[show_key] = True
            if st.button("🙈 Hide Response", key=f"hide_{rfi_id}"):
                st.session_state[show_key] = False

        if st.session_state.get(show_key, False):
            output = st.session_state.get(output_key)
            if output:
                st.markdown("#### 💬 Suggested Response")
                st.code(output["response"], language="markdown")

                if st.checkbox("📚 Show Context", key=ctx_key):
                    st.code(output.get("context_used", "No context available"))

                if not st.session_state.get(submitted_key):
                    if st.button("🚀 Submit Final Response", key=f"submit_{rfi_id}"):
                        save_response_history(output)
                        st.session_state[submitted_key] = True
                        st.success("📥 Response submitted and visible to audit team.")
            else:
                st.warning("⚠️ No response generated yet.")