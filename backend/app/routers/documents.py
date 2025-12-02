from __future__ import annotations

import datetime
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from ..db import db
from ..services.vector_store import index_document
from ..services.text_extraction import extract_text_from_bytes

router = APIRouter()  # prefix added in main.py

# Auto-delete documents older than 3 days
RETENTION_DAYS = 3


def cleanup_expired_documents() -> int:
    """
    Delete documents (and related chunks) older than RETENTION_DAYS.
    Uses the stored `created_at` field (your old system already has it).
    """
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=RETENTION_DAYS)

    # Find expired docs
    expired = list(db.documents.find({"created_at": {"$lt": cutoff}}))
    if not expired:
        return 0

    removed = 0
    for doc in expired:
        doc_id = doc.get("doc_id")
        if not doc_id:
            continue

        # Delete vector chunks for this document
        db.chunks.delete_many({"doc_id": doc_id})

        # Delete the document record
        db.documents.delete_one({"doc_id": doc_id})
        removed += 1

    return removed


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload any study file (PDF, image, DOCX, text/code).
    - Before doing anything: auto-delete expired documents (> 3 days)
    - Extract text (OCR friendly)
    - Store only metadata in MongoDB
    - Index embeddings for semantic search
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    # ⚡ Auto-clean old documents every upload
    cleanup_expired_documents()

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    text = extract_text_from_bytes(
        raw_bytes,
        filename=file.filename,
        content_type=file.content_type,
    ) or ""

    # UUID doc_id (same as your old system)
    doc_id = str(uuid.uuid4())

    # Store ONLY metadata (no large binary)
    db.documents.insert_one(
        {
            "doc_id": doc_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "created_at": datetime.datetime.utcnow(),
            "has_text": bool(text.strip()),
        }
    )

    # Index chunks into vector store (GROQ + Nomic)
    num_chunks = 0
    if text.strip():
        num_chunks = index_document(doc_id, text)

    return {
        "doc_id": doc_id,
        "chunks_indexed": num_chunks,
        "has_text": bool(text.strip()),
    }
