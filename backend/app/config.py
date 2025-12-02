import os
from pymongo import MongoClient

from langchain_groq import ChatGroq
from langchain_nomic import NomicEmbeddings


# ========= MongoDB =========

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "ai_pdf_tutor")

mongo_client = MongoClient(MONGODB_URI)
db = mongo_client[MONGODB_DB]


# ========= Groq LLM (for summaries + MCQs) =========
# Get your key from https://console.groq.com

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. Please export it before running the backend."
    )

# ChatGroq reads GROQ_API_KEY from env automatically
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # You can change to "llama-3.2-3b-preview" etc.
    temperature=0.3,
    max_tokens=None,
)


# ========= Nomic Embeddings (for vector search) =========
# Get your key from https://atlas.nomic.ai

NOMIC_API_KEY = os.getenv("NOMIC_API_KEY")
if not NOMIC_API_KEY:
    raise ValueError(
        "NOMIC_API_KEY is not set. Please export it before running the backend."
    )

# LangChain-Nomic uses NOMIC_API_KEY env var internally
embeddings = NomicEmbeddings(
    model="nomic-embed-text-v1.5",  # long-context, high-quality embeddings
)
