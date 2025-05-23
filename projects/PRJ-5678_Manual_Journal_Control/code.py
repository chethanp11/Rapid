# === Post-Facto MJE Review Logic ===

journal_entries = [
    {"id": "JE-001", "status": "Approved", "reviewed_by": "Anita Rao"},
    {"id": "JE-003", "status": "Pending", "reviewed_by": ""},
    {"id": "JE-005", "status": "Pending", "reviewed_by": ""}
]

# Flag entries without review or with delayed status
def identify_pending_reviews(entries):
    return [e["id"] for e in entries if e["status"] == "Pending" or not e["reviewed_by"]]

flagged = identify_pending_reviews(journal_entries)

print("🔍 Entries requiring review:", flagged)
