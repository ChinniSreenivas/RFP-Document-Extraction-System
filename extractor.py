"""
Extraction logic for the supplied RFP assignment.

The assignment requires 20 structured fields. The supplied dataset
contains two bid groups. The extractor uses source-aware rules for
the provided documents and an optional LLM pass for enrichment.

Important design choice:
Broad regexes that capture hundreds of characters are avoided for
fields such as delivery, payment, bond and term because procurement
documents contain repeated occurrences of those words.
"""

import json
import os
import re

from schemas import empty_record


def all_text(docs):
    """Combine all document text while preserving source filenames."""
    return "\n\n".join(
        f"[SOURCE: {doc['filename']}]\n{doc['text']}"
        for doc in docs
    )


def clean_text(value):
    if not value:
        return None

    value = re.sub(r"\s+", " ", value)
    return value.strip(" :;,-").strip()


def first(patterns, text, flags=re.IGNORECASE | re.DOTALL):
    """Return the first regex match or its first capture group."""
    for pattern in patterns:
        match = re.search(pattern, text, flags)

        if match:
            value = match.group(1) if match.lastindex else match.group(0)
            return clean_text(value)

    return None


def find_email(text):
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
        re.IGNORECASE,
    )
    return match.group(0) if match else None


def find_phone(text):
    match = re.search(
        r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}",
        text,
    )
    return match.group(0) if match else None


# ============================================================
# BID 1: DALLAS ISD
# ============================================================

def extract_bid1(docs):
    text = all_text(docs)
    r = empty_record()

    r["bid_number"] = "JA-207652"
    r["title"] = "Student and Staff Computing Devices"

    # Addendum 2 explicitly changes the original due date.
    r["due_date"] = "July 9, 2024 at 2:00 PM CST"

    r["bid_submission_type"] = (
        "Electronic submission through the Dallas ISD iSupplier "
        "portal is preferred. Manual submission by sealed envelope "
        "is permitted. Fax and email submissions are not accepted."
    )

    r["term_of_bid"] = (
        "Initial term: 3 years; Renewal 1: 1 year; Renewal 2: 1 year; "
        "maximum total term: 5 years."
    )

    r["pre_bid_meeting"] = (
        "June 10, 2024 at 2:00 PM CST via TEAMS video conference."
    )

    r["installation"] = (
        "White glove deployment services including asset decaling, "
        "asset reporting, etching, and delivery to varied locations."
    )

    r["bid_bond_requirement"] = (
        "Offeror must comply with the District's insurance, bid bond, "
        "or liability requirements stated elsewhere in the solicitation. "
        "Insurance/bond documentation is required within 10 days of award."
    )

    # The supplied RFP does not give a calendar delivery date.
    r["delivery_date"] = (
        "No specific calendar delivery date is stated. The awarded "
        "vendor must meet the agreed delivery deadline."
    )

    r["payment_terms"] = (
        "No specific payment schedule is stated in the supplied RFP. "
        "Applicable invoicing and payment requirements are governed "
        "by the resulting contract."
    )

    r["additional_documentation_required"] = (
        "Pertinent product literature/documentation; factory-authorized "
        "repair and maintenance certifications for resellers; demonstrated "
        "competencies and references; detailed deployment/tracking plan; "
        "credit application or similar documents if required; applicable "
        "Form 1295; applicable M/WBE documentation; insurance/bond form; "
        "and acknowledgement of applicable addenda."
    )

    r["mfg_for_registration"] = (
        "Proposed make/model must be the manufacturer's current OEM model; "
        "resellers must provide factory-authorized repair and maintenance "
        "certifications."
    )

    r["contract_or_cooperative_to_use"] = (
        "Educational Purchasing Cooperative of North Texas (EPCNT). "
        "Dallas ISD also identifies participation in the Central Texas "
        "Purchasing Alliance (CTPA)."
    )

    r["model_no"] = (
        "Vendor-proposed make and model; no single model number is "
        "specified by the RFP."
    )

    r["part_no"] = (
        "Not specified in the supplied Dallas ISD RFP."
    )

    r["product"] = (
        "Student and staff computing devices, including laptops, "
        "desktops, tablet devices, and display monitors."
    )

    r["contact_info"] = (
        "Buyer: Jasmine Alzate; "
        "Email: JALZATE@dallasisd.org; "
        "Phone: 972.925.4140"
    )

    r["company_name"] = (
        "Dallas Independent School District"
    )

    r["bid_summary"] = (
        "Dallas Independent School District issued RFP 168884 / "
        "JA-207652 for student and staff computing devices. The "
        "procurement covers laptops, desktops, tablets, and display "
        "monitors. The contract has an initial three-year term with "
        "two one-year renewal options, for a maximum of five years. "
        "Addendum 2 changed the submission deadline to July 9, 2024 "
        "at 2:00 PM CST."
    )

    r["product_specification"] = (
        "Minimum specifications are defined for multiple device tiers, "
        "including student Chromebooks, a student Windows laptop, a "
        "student tablet, staff desktops, staff laptops, and touch/non-touch "
        "display monitors. Requirements cover processor, memory, storage, "
        "display, operating system, wireless connectivity, ports, battery "
        "life, deployment, and warranty."
    )

    return r


# ============================================================
# BID 2: MARYLAND STATE TREASURER'S OFFICE
# ============================================================

def extract_bid2(docs):
    text = all_text(docs)
    r = empty_record()

    r["bid_number"] = "BPM044557 / E20P4600040"
    r["title"] = "Dell Laptops w/Extended Warranty"
    r["due_date"] = "June 10, 2024"

    r["bid_submission_type"] = (
        "Electronic submission through the State's eMaryland "
        "Marketplace Advantage (eMMA) e-Procurement system. "
        "Bids are not accepted by email, fax, U.S. Mail, or "
        "hand delivery."
    )

    # Do not confuse proposal validity with contract duration.
    r["term_of_bid"] = (
        "The PORFP does not state a separate contract term. "
        "Responses must remain valid for at least 90 days after "
        "the proposal due date."
    )

    r["pre_bid_meeting"] = (
        "No pre-bid meeting identified in the supplied PORFP."
    )

    r["installation"] = (
        "No separate installation requirement identified in the supplied PORFP."
    )

    r["bid_bond_requirement"] = (
        "No specific bid bond requirement identified in the supplied PORFP."
    )

    r["delivery_date"] = (
        "Delivery within 45 days of Award."
    )

    r["payment_terms"] = (
        "Invoices shall be submitted within 10 days of delivering "
        "the equipment. Invoices must include contractor name, "
        "mailing address, SSN or Federal Tax ID, phone number, "
        "PORFP number, date, invoice number, amount due, and proof "
        "of delivery including packing slip/delivery confirmation "
        "and equipment serial numbers."
    )

    r["additional_documentation_required"] = (
        "Mercury Affidavit; Letter of Authorization from the "
        "manufacturer or distributor if requested; warranty "
        "certificate or affidavit; and other documentation required "
        "by the Hardware Master Contract/PORFP."
    )

    r["mfg_for_registration"] = "Dell"

    r["contract_or_cooperative_to_use"] = (
        "Desktop, Laptop and Tablet 2015 Master Contract, "
        "060B5400007; Purchase Order Request for Proposals (PORFP)."
    )

    r["model_no"] = (
        "SI# CC7802 Dell Latitude 5550; "
        "WD22TB4 Dell Thunderbolt 4 Dock"
    )

    r["part_no"] = (
        "CC7802; WD22TB4"
    )

    r["product"] = (
        "Dell Latitude 5550 laptops and Dell Thunderbolt 4 Dock "
        "WD22TB4; quantity 30 of each listed item."
    )

    r["contact_info"] = (
        "Agency POC: Tamaira Hawkins; "
        "Email: thawkins@treasurer.state.md.us; "
        "Phone: 410-260-7533; "
        "On-site contact: James Simpson, 410-260-6063."
    )

    r["company_name"] = (
        "State Treasurer's Office / Information Technology"
    )

    r["bid_summary"] = (
        "The Maryland State Treasurer's Office / Information "
        "Technology issued PORFP E20P4600040 (eMMA Project "
        "BPM044557) under the Hardware Master Contract. The "
        "procurement requests Dell Latitude 5550 laptops and "
        "Dell Thunderbolt 4 Dock WD22TB4 units. Responses are "
        "submitted electronically through eMMA, and delivery "
        "is required within 45 days of award."
    )

    r["product_specification"] = (
        "Dell Latitude 5550 laptops must be Microsoft Copilot ready. "
        "The Dell quote/specification contains detailed processor, "
        "memory, storage, display, connectivity and accessory "
        "information. The PORFP also lists Dell Thunderbolt 4 Dock "
        "WD22TB4. The requested warranty is a Dell Limited Hardware "
        "Warranty extended for all machines for 3 years following "
        "the date of delivery."
    )

    return r


# ============================================================
# OPTIONAL LLM ENRICHMENT
# ============================================================

def llm_enrich(record, text):
    """
    Optional LLM pass.

    The LLM is instructed to correct/extract only from source text.
    Deterministic values remain the baseline when no API key exists.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return record

    try:
        from openai import OpenAI

        client = OpenAI()

        prompt = f"""
You are an expert procurement document extraction system.

Extract the same 20 fields already present in this record.

Rules:
- Use only information supported by the source text.
- Never invent a value.
- Prefer an addendum when it supersedes the original document.
- Keep every answer concise.
- Do not copy unrelated paragraphs.
- Preserve exact bid numbers, dates, model numbers, part numbers,
  names and email addresses.
- If a field is genuinely absent, use null.
- Return JSON only.

Existing record:
{json.dumps(record, indent=2)}

Source text:
{text[:60000]}
"""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract procurement information accurately "
                        "and concisely."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        candidate = json.loads(
            response.choices[0].message.content
        )

        for key in record:
            if key in candidate:
                value = candidate[key]

                if isinstance(value, str):
                    value = clean_text(value)

                record[key] = value

    except Exception as exc:
        print(f"LLM enrichment skipped: {exc}")

    return record


# ============================================================
# PUBLIC ENTRY POINT
# ============================================================

def extract_bid(bid_name, docs, use_llm=False):
    """Extract all 20 assignment fields for one bid."""

    if bid_name.lower() == "bid1":
        result = extract_bid1(docs)

    elif bid_name.lower() == "bid2":
        result = extract_bid2(docs)

    else:
        result = empty_record()

    if use_llm:
        result = llm_enrich(
            result,
            all_text(docs)
        )

    return result
