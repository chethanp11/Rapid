# === Simplified Nostro Break Matcher ===

breaks = [
    {"id": "BRK-1001", "currency": "USD", "amount": 1500.25},
    {"id": "BRK-1002", "currency": "EUR", "amount": -820.00},
    {"id": "BRK-1003", "currency": "INR", "amount": 130.50}
]

# Reconciliation logic: flag if break exceeds absolute threshold
def flag_significant_break(break_entry, threshold=500):
    return abs(break_entry["amount"]) > threshold

flagged = [b["id"] for b in breaks if flag_significant_break(b)]

print("Flagged breaks:", flagged)
