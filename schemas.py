FIELDS = [
    "bid_number",
    "title",
    "due_date",
    "bid_submission_type",
    "term_of_bid",
    "pre_bid_meeting",
    "installation",
    "bid_bond_requirement",
    "delivery_date",
    "payment_terms",
    "additional_documentation_required",
    "mfg_for_registration",
    "contract_or_cooperative_to_use",
    "model_no",
    "part_no",
    "product",
    "contact_info",
    "company_name",
    "bid_summary",
    "product_specification",
]


def empty_record():
    """Return an empty record containing all required fields."""
    return {field: None for field in FIELDS}


def validate_bid(record):
    """Validate that every required assignment field exists."""
    missing = [field for field in FIELDS if field not in record]

    if missing:
        raise ValueError(
            f"Missing required fields: {missing}"
        )

    return True
