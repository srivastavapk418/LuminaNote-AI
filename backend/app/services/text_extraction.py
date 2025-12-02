# app/services/text_extraction.py

from __future__ import annotations

import io
import mimetypes
from typing import Optional

import pdfplumber
from PIL import Image, ImageOps, ImageFilter
import pytesseract
# Windows: Tell pytesseract where the real Tesseract.exe is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


try:
    # optional: for .docx support
    import docx  # python-docx
except ImportError:
    docx = None


# ---------- small helpers ----------


def _guess_mime(filename: Optional[str], content_type: Optional[str]) -> str:
    """
    Best-effort guess of the file's mime type from content_type + extension.
    """
    if content_type:
        return content_type

    if filename:
        guessed, _ = mimetypes.guess_type(filename)
        if guessed:
            return guessed

    return "application/octet-stream"


def _ocr_pil_image(img: Image.Image) -> str:
    """
    Run OCR on a single PIL.Image with light pre-processing tuned for
    scanned notes (including handwriting). Tesseract is free but not
    perfect on handwriting; this just tries to give it the best chance.
    """
    # Convert to grayscale
    gray = ImageOps.grayscale(img)

    # Slight contrast / sharpness tweaks often help
    gray = gray.filter(ImageFilter.MedianFilter())
    # Basic binarization
    bw = gray.point(lambda x: 0 if x < 160 else 255, "1")

    # You can tweak the psm value if needed (6 = block of text)
    config = "--psm 6"

    text = pytesseract.image_to_string(bw, config=config)
    return text or ""


def _extract_text_from_pdf_bytes(raw: bytes) -> str:
    """
    Try to extract *machine* text from a PDF.
    """
    full_text_parts = []

    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            if txt.strip():
                full_text_parts.append(txt)

    return "\n\n".join(full_text_parts).strip()


def _ocr_pdf_pages(raw: bytes) -> str:
    """
    Fallback for image-based / handwritten PDFs:
    render each page to an image and run OCR.
    """
    ocr_parts = []

    # pdfplumber uses pypdfium2 under the hood for rendering
    with pdfplumber.open(io.BytesIO(raw)) as pdf:
        for page in pdf.pages:
            try:
                page_image = page.to_image(resolution=300).original  # PIL.Image
            except Exception:
                continue

            txt = _ocr_pil_image(page_image)
            if txt.strip():
                ocr_parts.append(txt)

    return "\n\n".join(ocr_parts).strip()


def _extract_text_from_image_bytes(raw: bytes) -> str:
    """
    OCR for image formats (jpeg/png etc.).
    """
    with Image.open(io.BytesIO(raw)) as img:
        return _ocr_pil_image(img)


def _extract_text_from_docx_bytes(raw: bytes) -> str:
    """
    Only used if python-docx is installed.
    """
    if docx is None:
        return ""

    f = io.BytesIO(raw)
    document = docx.Document(f)
    paras = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paras).strip()


# ---------- public API ----------


def extract_text_from_bytes(
    raw_bytes: bytes,
    filename: Optional[str] = None,
    content_type: Optional[str] = None,
) -> str:
    """
    Smart text extraction entry point.

    Supports:
      - PDFs (machine text + OCR fallback for scanned/handwritten)
      - Images (JPG/PNG/etc via OCR)
      - DOCX (if python-docx installed)
      - Plain text & code files (utf-8 decode)

    Returns a single big text string (may be empty if nothing could be read).
    """
    mime = _guess_mime(filename, content_type).lower()
    ext = (filename or "").lower()

    # ---- PDF ----
    if "pdf" in mime or ext.endswith(".pdf"):
        # 1) try normal PDF text extraction
        text = _extract_text_from_pdf_bytes(raw_bytes)

        # 2) if we got almost nothing, fall back to OCR on each page
        if len(text.strip()) < 40:
            ocr_text = _ocr_pdf_pages(raw_bytes)

            # if OCR finds something, use it (or append)
            if ocr_text.strip():
                # Optionally combine both:
                if text.strip():
                    text = text + "\n\n" + ocr_text
                else:
                    text = ocr_text

        return text or ""

    # ---- Images (JPEG/PNG/etc) ----
    if mime.startswith("image/") or ext.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")):
        return _extract_text_from_image_bytes(raw_bytes)

    # ---- DOCX ----
    if ext.endswith(".docx") or "officedocument.wordprocessingml" in mime:
        return _extract_text_from_docx_bytes(raw_bytes)

    # ---- Plain text / code files ----
    if ext.endswith((".txt", ".md", ".py", ".java", ".js", ".ts", ".tsx",
                     ".c", ".cpp", ".cs", ".html", ".css", ".json", ".xml", ".sql")):
        try:
            return raw_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return ""

    # Fallback: try utf-8 decode anyway
    try:
        return raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        return ""
