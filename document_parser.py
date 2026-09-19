from pathlib import Path
from collections import defaultdict
import re


SUPPORTED_EXTENSIONS = {".pdf", ".html", ".htm"}


def clean_text(text: str) -> str:
    """Normalize extracted document text while preserving paragraphs."""
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_pdf(path: Path) -> str:
    """Extract text from a PDF using PyMuPDF."""
    import pymupdf

    doc = pymupdf.open(path)
    pages = []

    for page_number, page in enumerate(doc, start=1):
        pages.append(
            f"\n--- PAGE {page_number} ---\n"
            f"{page.get_text('text')}"
        )

    return clean_text("\n".join(pages))


def read_html(path: Path) -> str:
    """Extract visible text from an HTML document."""
    from bs4 import BeautifulSoup

    html = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return clean_text(
        soup.get_text("\n")
    )


def load_documents(input_dir: Path):
    """
    Load all supported PDF/HTML documents and group them by
    Bid1/Bid2 directory.
    """
    grouped = defaultdict(list)

    for path in sorted(input_dir.rglob("*")):
        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        bid = next(
            (
                parent.name
                for parent in path.parents
                if re.fullmatch(r"Bid\d+", parent.name, re.I)
            ),
            "Ungrouped",
        )

        if path.suffix.lower() == ".pdf":
            text = read_pdf(path)
        else:
            text = read_html(path)

        grouped[bid].append(
            {
                "filename": path.name,
                "path": str(path),
                "text": text,
            }
        )

    return dict(grouped)
