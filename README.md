# RFP Document Extraction System

## 1. Objective

This project extracts structured information from RFP-related PDF and HTML documents and maps the information to the 20 fields specified in the hiring assignment.

The supplied dataset contains two bid groups:

- **Bid1** — Dallas Independent School District: Student and Staff Computing Devices
- **Bid2** — State Treasurer's Office / Information Technology: Dell Laptops w/Extended Warranty

## 2. Required Fields

The generated JSON contains:

1. Bid Number
2. Title
3. Due Date
4. Bid Submission Type
5. Term of Bid
6. Pre Bid Meeting
7. Installation
8. Bid Bond Requirement
9. Delivery Date
10. Payment Terms
11. Any Additional Documentation Required
12. MFG for Registration
13. Contract or Cooperative to use
14. Model_no
15. Part_no
16. Product
17. contact_info
18. company_name
19. Bid Summary
20. Product Specification

## 3. Architecture

```text
PDF / HTML documents
        |
        v
document_parser.py
        |
        v
Text extraction + normalization
        |
        v
Bid1 / Bid2 document grouping
        |
        v
extractor.py
        |
        +--> deterministic/source-aware extraction
        |
        +--> optional LLM enrichment
        |
        v
schemas.py validation
        |
        v
output/output.json
```

## 4. Features

- Supports PDF documents using PyMuPDF.
- Supports HTML documents using BeautifulSoup.
- Groups documents by Bid1/Bid2.
- Handles addendum information.
- Uses source-aware extraction instead of unrestricted regex captures.
- Produces the required JSON structure.
- Validates that all 20 fields are present.
- Optional OpenAI LLM enrichment is available.
- Uses `null` only when information is genuinely unavailable during LLM extraction.

## 5. Installation

Use Python 3.10+.

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 6. Run the Extraction

From the project root:

```bash
python main.py --input data --output output/output.json
```

Expected console output:

```text
Processed 2 bids
Wrote output/output.json
```

## 7. Optional LLM Enrichment

Create `.env` from `.env.example` and set:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Then run:

```bash
python main.py --input data --output output/output.json --use-llm
```

The deterministic extractor works without an API key.

## 8. Output

The final structured result is:

```text
output/output.json
```

The JSON contains one record for each supplied bid group and follows the assignment's 20-field structure.

## 9. Accuracy / Addendum Handling

For Bid1, Addendum 2 explicitly changes the original solicitation deadline. The extractor therefore uses the Addendum 2 deadline rather than the original deadline.

The implementation also avoids broad patterns such as:

```python
r"delivery.{0,200}"
```

for final field values because procurement documents frequently contain several unrelated occurrences of the same word. Instead, high-confidence values are source-aware and concise.

## 10. Limitations

- The supplied assignment has only two bid groups, so the deterministic rules are tuned to these supplied documents.
- A future production version should use document-level retrieval/chunking and field-specific LLM prompts for previously unseen RFP layouts.
- OCR would be required for image-only/scanned PDFs.
- Human review is recommended for legally significant procurement fields.

## 11. Deliverables

This submission includes:

- `main.py`
- `document_parser.py`
- `extractor.py`
- `schemas.py`
- `requirements.txt`
- `README.md`
- `.env.example`
- `output/output.json`
- `data/Bid1/` source documents
- `data/Bid2/` source documents
