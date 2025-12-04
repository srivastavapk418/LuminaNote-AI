# app/services/text_extraction.py

from __future__ import annotations

import io
import os
import mimetypes
from typing import Optional

from PIL import Image
import pytesseract
import pdfplumber
from docx import Document

# --------------------------------------------------------------------
# Tesseract configuration
# --------------------------------------------------------------------

# On Windows, tell pytesseract where Tesseract is installed.
# This is ONLY for your local machine; Render (Linux) will ignore this.
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Enable OCR only on Windows by default.
# On Render (Linux), OCR will be disabled automatically.
OCR_ENABLED = os.getenv("ENABLE_OCR", "1" if os.name == "nt" else "0") == "1"


# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------

def _safe_decode_text(raw: bytes) -> str:
    """Try a few encodings to decode plain text / code files."""
    for enc in ("utf-8", "latin-1", "windows-1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return ""


def _extract_from_pdf(raw: bytes) -> str:
    """Extract text from a PDF using its text layer (no OCR)."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            txt = txt.strip()
            if txt:
                text_parts.append(txt)
    return "\n\n".join(text_parts)


def _ocr_image_bytes(raw: bytes) -> str:
    """Run OCR on an image (only if OCR_ENABLED and Tesseract is available)."""
    if not OCR_ENABLED:
        return ""

    try:
        img = Image.open(io.BytesIO(raw))
        img = img.convert("L")  # grayscale
        text = pytesseract.image_to_string(img, config="--psm 6")
        return text or ""
    except pytesseract.TesseractNotFoundError:
        # Tesseract is not installed on this system (e.g., Render) – fail gracefully
        return ""
    except Exception:
        return ""


def _ocr_pdf_pages(raw: bytes) -> str:
    """
    Convert each PDF page to an image and OCR it.
    NOTE: This is disabled on Render (Linux) by OCR_ENABLED flag.
    """
    if not OCR_ENABLED:
        return ""

    try:
        from pdf2image import convert_from_bytes
    except ImportError:
        # pdf2image not installed
        return ""

    try:
        pages = convert_from_bytes(raw)
    except Exception:
        return ""

    texts = []
    for page in pages:
        try:
            page = page.convert("L")
            txt = pytesseract.image_to_string(page, config="--psm 6")
            if txt.strip():
                texts.append(txt)
        except pytesseract.TesseractNotFoundError:
            return ""
        except Exception:
            continue

    return "\n\n".join(texts)


def _extract_from_docx(raw: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        file_like = io.BytesIO(raw)
        doc = Document(file_like)
        paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paras)
    except Exception:
        return ""


def _guess_mime(filename: Optional[str], content_type: Optional[str]) -> str:
    if content_type:
        return content_type
    if filename:
        mime, _ = mimetypes.guess_type(filename)
        if mime:
            return mime
    return "application/octet-stream"


# --------------------------------------------------------------------
# Public function used by documents.py
# --------------------------------------------------------------------

def extract_text_from_bytes(
    raw_bytes: bytes,
    filename: Optional[str] = None,
    content_type: Optional[str] = None,
) -> str:
    """
    Unified text extractor:
    - PDFs (text layer; OCR fallback only when OCR_ENABLED)
    - Images (OCR when OCR_ENABLED)
    - DOCX
    - Text / code files
    """
    if not raw_bytes:
        return ""

    mime = _guess_mime(filename, content_type)
    fname_lower = (filename or "").lower()

    # ---- PDF ----
    if mime == "application/pdf" or fname_lower.endswith(".pdf"):
        text = _extract_from_pdf(raw_bytes)
        if text.strip():
            return text

        # Fallback to OCR ONLY on local (Windows) where OCR_ENABLED = True
        ocr_text = _ocr_pdf_pages(raw_bytes)
        return ocr_text or text

    # ---- Images (PNG, JPG, etc.) ----
    if mime.startswith("image/") or fname_lower.endswith(
        (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")
    ):
        return _ocr_image_bytes(raw_bytes)

    # ---- DOCX ----
    if fname_lower.endswith(".docx") or mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        txt = _extract_from_docx(raw_bytes)
        if txt.strip():
            return txt

    # ---- Default: treat as plain text / code ----
    txt = _safe_decode_text(raw_bytes)
    return txt

