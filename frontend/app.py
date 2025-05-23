# --- 📁 Path Setup ---
import sys, os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RAPID_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# Ensure correct Rapid paths
if RAPID_ROOT not in sys.path:
    sys.path.append(RAPID_ROOT)

# --- 🔁 Imports ---
import streamlit as st
import json
from datetime import datetime
from core.rfi_manager import load_rfis, filter_rfis_by_project
from core.response_engine import generate_rfi_response
from config.pyenv import get_path  # ✅ This now refers to rapid/config/pyenv.py

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

# --- 📥 Load and Display RFIs ---
all_rfis = load_rfis()
if not all_rfis:
    st.info("📭 No RFIs available.")
else:
    project_filter = st.selectbox("📁 Filter by Project", sorted(set(r["project_id"] for r in all_rfis)))
    filtered = filter_rfis_by_project(project_filter)

    response_path = os.path.join(get_path("RAPID_DATA_PATH"), "response_history.json")
    try:
        with open(response_path, "r") as f:
            history = json.load(f)
    except:
        history = []

    for rfi in filtered:
        rfi_id = rfi["rfi_id"]
        st.markdown(f"---\n### 🔖 `{rfi_id}` — {rfi['title']}")
        st.markdown(f"**📌 Project:** `{rfi['project_id']}`")
        st.markdown(f"**📝 Description:** {rfi['description']}")
        st.markdown(f"**👤 Submitted by:** `{rfi['submitted_by']}` | **🎯 Priority:** `{rfi.get('priority', 'Medium')}`")

        output_key = f"out_{rfi_id}"
        if output_key not in st.session_state:
            from_history = next((item for item in history if item.get("rfi_id") == rfi_id), None)
            if from_history:
                st.session_state[output_key] = from_history

        output = st.session_state.get(output_key)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🧠 Generate Response", key=f"gen_{rfi_id}"):
                with st.spinner("💬 Generating..."):
                    response = generate_rfi_response(rfi)
                st.session_state[output_key] = response
                response["rfi_id"] = rfi_id
                response["timestamp"] = datetime.utcnow().isoformat() + "Z"
                save_response_history(response)
                st.success("✅ Response generated and saved!")

        with col2:
            if output:
                if st.button("📄 View Saved Response", key=f"view_{rfi_id}"):
                    st.markdown("#### 💬 Suggested Response")
                    st.code(output["response"], language="markdown")
                    if st.checkbox("📚 Show Context", key=f"ctx_{rfi_id}"):
                        st.code(output.get("context_used", "No context available"))