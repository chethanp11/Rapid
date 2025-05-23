# ✅ rfi_manager.py — Manages RFI Storage and Filtering
# -----------------------------------------------------
# Handles loading, adding, and filtering RFIs tied to specific control projects.

import os
import json
from datetime import datetime
from config.pyenv import get_path  # ✅ ensure Rapid/config/pyenv.py is used

# 🔁 Path to RFI store JSON file
RFI_STORE_PATH = os.path.join(get_path("RAPID_DATA_PATH"), "rfi_store.json")

def load_rfis():
    """
    Load all RFIs from the JSON file.

    Returns:
        List[dict]: List of RFI entries.
    """
    if not os.path.exists(RFI_STORE_PATH):
        return []
    with open(RFI_STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_rfis(data):
    """
    Overwrite the RFI store with updated data.

    Args:
        data (List[dict]): Full list of RFIs to write to file.
    """
    with open(RFI_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_rfi(new_rfi: dict) -> dict:
    """
    Add a new RFI to the store after validating and enriching fields.

    Args:
        new_rfi (dict): Partial RFI object from UI submission.

    Returns:
        dict: Fully populated RFI entry.
    """
    required_fields = ["rfi_id", "title", "description", "project_id", "submitted_by"]
    for field in required_fields:
        if field not in new_rfi:
            raise ValueError(f"Missing required field: {field}")

    rfis = load_rfis()
    timestamp = datetime.utcnow().isoformat() + "Z"

    enriched_rfi = {
        **new_rfi,
        "status": "Pending",
        "submitted_on": timestamp,
        "last_updated_on": timestamp,
        "priority": new_rfi.get("priority", "Medium"),
        "tags": new_rfi.get("tags", []),
        "assigned_to": new_rfi.get("assigned_to", ""),
        "attachments": new_rfi.get("attachments", []),
        "project_name": new_rfi.get("project_name", new_rfi["project_id"]),
    }

    rfis.append(enriched_rfi)
    save_rfis(rfis)
    return enriched_rfi

def filter_rfis_by_project(project_id: str):
    """
    Filter all RFIs belonging to a given project.

    Args:
        project_id (str): Project identifier (folder/project ID)

    Returns:
        List[dict]: Filtered RFIs for that project.
    """
    return [rfi for rfi in load_rfis() if rfi.get("project_id") == project_id]