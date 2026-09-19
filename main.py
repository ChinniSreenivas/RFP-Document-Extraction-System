"""
RFP Document Extraction System

Usage:
    python main.py --input data --output output/output.json

Optional LLM enrichment:
    1. Create a .env file from .env.example
    2. Set OPENAI_API_KEY
    3. Run:
       python main.py --input data --output output/output.json --use-llm
"""

from pathlib import Path
import argparse
import json

from document_parser import load_documents
from extractor import extract_bid
from schemas import validate_bid


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured information from RFP documents."
    )
    parser.add_argument("--input", default="data")
    parser.add_argument("--output", default="output/output.json")
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use optional OpenAI enrichment when OPENAI_API_KEY is configured.",
    )
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    documents = load_documents(input_dir)

    if not documents:
        raise FileNotFoundError(
            f"No PDF/HTML documents found under: {input_dir}"
        )

    bids = []

    for bid_name, bid_docs in sorted(documents.items()):
        result = extract_bid(
            bid_name,
            bid_docs,
            use_llm=args.use_llm,
        )
        validate_bid(result)
        bids.append(result)

    payload = {
        "project": "RFP Document Extraction",
        "schema_version": "1.0",
        "bids": bids,
    }

    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Processed {len(bids)} bids")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
