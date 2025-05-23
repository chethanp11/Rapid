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
from core.rfi_manager import load_rfis, add_rfi
from config.pyenv import get_path

# --- ⚙️ Setup ---
st.set_page_config(page_title="Controls COE – RFI Submission Portal", page_icon="📨", layout="wide")
st.markdown("<h1 style='color:#1E88E5;'>📨 Controls COE – RFI Submission Portal</h1>", unsafe_allow_html=True)

# --- 📝 Submit New RFI ---
st.subheader("📝 Submit New RFI")

all_rfis = load_rfis()
existing_ids = [int(r["rfi_id"].split("-")[1]) for r in all_rfis if r["rfi_id"].startswith("RFI-")]
next_rfi_id = f"RFI-{(max(existing_ids, default=0) + 1):04d}"

projects_path = get_path("RAPID_PROJECTS_PATH")
available_projects = sorted([p for p in os.listdir(projects_path) if os.path.isdir(os.path.join(projects_path, p))])

with st.form("submit_rfi_form"):
    st.text_input("RFI ID (Auto-generated)", value=next_rfi_id, disabled=True)
    title = st.text_input("RFI Title")
    description = st.text_area("RFI Description")
    project_id = st.selectbox("Project ID", available_projects, key="submit_project")
    submitted_by = st.text_input("Submitted By (e.g., audit_jane)")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("✅ Submit RFI")

    if submitted:
        if not all([title, description, project_id, submitted_by]):
            st.error("⚠️ All fields are required.")
        else:
            new_rfi = {
                "rfi_id": next_rfi_id,
                "title": title,
                "description": description,
                "project_id": project_id,
                "project_name": project_id,
                "submitted_by": submitted_by,
                "priority": priority
            }
            add_rfi(new_rfi)
            st.success(f"✅ RFI `{next_rfi_id}` submitted successfully.")

# --- 📄 View Finalized Responses ---
st.subheader("📋 View Finalized RFI Responses")

response_path = os.path.join(get_path("RAPID_DATA_PATH"), "response_history.json")
try:
    with open(response_path, "r") as f:
        response_history = json.load(f)
except:
    response_history = []

valid_responses = [item for item in response_history if item.get("project_id") and item.get("rfi_id")]

if not valid_responses:
    st.warning("⚠️ No valid responses with project and RFI ID found.")
else:
    all_projects = sorted(set(item["project_id"] for item in valid_responses))
    selected_project = st.selectbox("📁 Select Project", all_projects, key="project_filter")

    rfis_in_project = [r for r in valid_responses if r["project_id"] == selected_project]
    rfi_options = sorted([r["rfi_id"] for r in rfis_in_project])
    selected_rfi_id = st.selectbox("📌 Select RFI", rfi_options, key="rfi_filter")

    selected_response = next((r for r in rfis_in_project if r["rfi_id"] == selected_rfi_id), None)
    response_key = f"show_resp_{selected_rfi_id}"

    if response_key not in st.session_state:
        st.session_state[response_key] = True

    if st.button("📄 View Response", key=f"view_{selected_rfi_id}"):
        st.session_state[response_key] = True
    if st.button("🙈 Hide Response", key=f"hide_{selected_rfi_id}"):
        st.session_state[response_key] = False

    if selected_response and st.session_state.get(response_key, False):
        st.markdown("---")
        st.markdown(f"### 🔖 RFI ID: `{selected_response['rfi_id']}`")
        st.markdown(f"**📂 Project:** `{selected_response['project_id']}`")
        st.markdown(f"**🕒 Generated On:** {selected_response.get('timestamp', '-')}")
        st.markdown(f"**🏷️ Category:** {selected_response.get('category', '-')}")
        st.markdown(f"**📌 Status:** `{selected_response.get('status', 'Pending')}`")
        st.markdown("#### 💬 Final Response")
        st.code(selected_response["response"], language="markdown")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Accept Response", key=f"accept_{selected_rfi_id}"):
                selected_response["status"] = "Accepted"
                with open(response_path, "w") as f:
                    json.dump(response_history, f, indent=2)
                st.success("✅ Response marked as accepted.")

        with col2:
            if st.button("↩️ Return for Revision", key=f"return_{selected_rfi_id}"):
                selected_response["status"] = "Returned"
                with open(response_path, "w") as f:
                    json.dump(response_history, f, indent=2)
                st.warning("🔁 Response marked for revision.")