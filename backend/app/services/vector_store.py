from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..config import embeddings
from ..db import db


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    """
    Split raw text into overlapping chunks for embedding & retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )
    return splitter.split_text(text or "")


def index_document(doc_id: str, text: str) -> int:
    """
    - Split the document text into chunks
    - Embed each chunk with the configured embeddings model (Nomic)
    - Store chunks + embeddings in MongoDB (collection: chunks)
    """
    chunks = chunk_text(text)
    if not chunks:
        return 0

    # embeddings: NomicEmbeddings from config.py
    vecs = embeddings.embed_documents(chunks)

    docs = []
    for i, (chunk, emb) in enumerate(zip(chunks, vecs)):
        docs.append(
            {
                "doc_id": doc_id,
                "chunk_index": i,
                "text": chunk,
                "embedding": emb,
            }
        )

    if docs:
        db.chunks.insert_many(docs)

    return len(docs)


def _cosine_similarity(a, b) -> float:
    """
    Simple cosine similarity between two embedding vectors.
    """
    import math

    length = min(len(a), len(b))
    dot = 0.0
    na = 0.0
    nb = 0.0
    for i in range(length):
        dot += a[i] * b[i]
        na += a[i] * a[i]
        nb += b[i] * b[i]
    if na == 0 or nb == 0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


def search_document(doc_id: str, query: str, n_results: int = 8):
    """
    Semantic search:
    - Embed the query
    - Compute cosine similarity with all chunks for this doc_id
    - Return top-N chunks sorted by relevance
    """
    if not query:
        query = "key points"

    query_emb = embeddings.embed_query(query)

    all_chunks = list(db.chunks.find({"doc_id": doc_id}))
    if not all_chunks:
        return []

    for c in all_chunks:
        c["score"] = _cosine_similarity(query_emb, c.get("embedding", []))

    all_chunks.sort(key=lambda x: x.get("score", 0), reverse=True)
    top = all_chunks[:n_results]
    return top
