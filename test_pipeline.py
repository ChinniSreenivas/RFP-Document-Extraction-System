import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "output.json"

subprocess.run(
    [
        sys.executable,
        str(ROOT / "main.py"),
        "--input", str(ROOT / "data"),
        "--output", str(OUTPUT),
    ],
    check=True,
)

payload = json.loads(OUTPUT.read_text(encoding="utf-8"))

assert len(payload["bids"]) == 2

for bid in payload["bids"]:
    assert len(bid) == 20
    assert all(key in bid for key in [
        "bid_number", "title", "due_date",
        "bid_submission_type", "term_of_bid",
        "pre_bid_meeting", "installation",
        "bid_bond_requirement", "delivery_date",
        "payment_terms", "additional_documentation_required",
        "mfg_for_registration", "contract_or_cooperative_to_use",
        "model_no", "part_no", "product", "contact_info",
        "company_name", "bid_summary", "product_specification",
    ])

print("All tests passed.")
