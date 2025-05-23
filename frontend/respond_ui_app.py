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
from config.pyenv import get_path

# --- 💾 Save Final Response to History ---
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
st.markdown("""
<h1 style='color:#4CAF50; font-size: 40px;'>🛠️ RAPID – Respond to RFIs</h1>
<p style='font-size: 25px; font-style: italic; color: blue;'>
RAPID = <b>Response Assistant for Project Issues & Disclosures</b>
</p>
""", unsafe_allow_html=True)

# --- 📥 Load RFIs and Existing Responses ---
all_rfis = load_rfis()
if not all_rfis:
    st.info("📭 No RFIs available.")
else:
    project_filter = st.selectbox("📁 Filter by Project", sorted(set(r["project_id"] for r in all_rfis)))
    filtered = filter_rfis_by_project(project_filter)

    response_path = os.path.join(get_path("RAPID_DATA_PATH"), "response_history.json")
    try:
        with open(response_path, "r") as f:
            response_history = json.load(f)
    except:
        response_history = []

    for rfi in filtered:
        rfi_id = rfi["rfi_id"]
        project_id = rfi["project_id"]

        st.markdown(f"---\n### 🔖 `{rfi_id}` — {rfi['title']}")
        st.markdown(f"**📌 Project:** `{project_id}`")
        st.markdown(f"**📝 Description:** {rfi['description']}")
        st.markdown(f"**👤 Submitted by:** `{rfi['submitted_by']}` | **🎯 Priority:** `{rfi.get('priority', 'Medium')}`")

        output_key = f"out_{rfi_id}"
        show_key = f"show_resp_{rfi_id}"
        context_key = f"ctx_{rfi_id}"

        # Load from history if not in session
        if output_key not in st.session_state:
            from_history = next((item for item in response_history if item.get("rfi_id") == rfi_id), None)
            if from_history:
                st.session_state[output_key] = from_history
                st.session_state[show_key] = False

        output = st.session_state.get(output_key, None)

        # Get status from existing response
        current_status = output.get("status") if output else None
        if not current_status:
            current_status = next(
                (item.get("status", "Pending Review") for item in response_history if item.get("rfi_id") == rfi_id),
                "Pending Review"
            )
        st.markdown(f"**📌 Status:** `{current_status}`")

        # --- Action Buttons ---
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🧠 Generate Response", key=f"gen_{rfi_id}"):
                with st.spinner("💬 Thinking..."):
                    response = generate_rfi_response(rfi)
                response["rfi_id"] = rfi_id
                response["project_id"] = project_id
                response["status"] = "Pending Review"
                response["timestamp"] = datetime.utcnow().isoformat() + "Z"
                st.session_state[output_key] = response
                st.session_state[show_key] = True
                st.success("✅ Response generated. Review before submitting.")

        with col2:
            if st.button("📄 View Response", key=f"view_{rfi_id}"):
                st.session_state[show_key] = True
            if st.button("🙈 Hide Response", key=f"hide_{rfi_id}"):
                st.session_state[show_key] = False

        # --- Display Response Block ---
        if st.session_state.get(show_key, False):
            output = st.session_state.get(output_key)
            if output and output.get("response"):
                st.markdown("#### 💬 Suggested Response")
                st.code(output["response"], language="markdown")

                if st.checkbox("📚 Show Context", key=context_key):
                    st.code(output.get("context_used", "No context available"))

                if st.button("✅ Submit Final Response", key=f"submit_{rfi_id}"):
                    output["status"] = "Pending Review"
                    save_response_history(output)
                    st.success("📬 Final response submitted and status set to 'Pending Review'.")
            else:
                st.warning("⚠️ No response available. Please generate it first.")