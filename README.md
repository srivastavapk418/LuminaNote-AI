⭐ LuminoNote AI

Your all-in-one AI assistant for understanding PDFs, images, handwritten notes, DOCX files, and code files.
Upload → Extract → Summarize → Practice.

🚀 Features

Supports PDF, scanned PDFs, images, DOCX, TXT, code files

OCR support for handwritten & scanned notes (Tesseract + preprocessing)

Full summaries powered by Groq LLM (free)

Topic-based summaries

AI-generated MCQs with answers + explanations

Semantic vector search using Nomic embeddings (free)

Auto-cleanup: documents older than 3 days are deleted

Modern React + Vite UI

🧠 Tech Stack
Frontend

React, Vite, JavaScript

Backend

FastAPI, Python

Groq LLM (Mixtral / Gemma)

Nomic embeddings

LangGraph pipelines

Tesseract OCR

PyMuPDF, python-docx

Database

MongoDB Atlas

📁 Project Structure
LuminoNote-AI/
├── frontend/
├── backend/
│   ├── app/
│   ├── services/
│   ├── routers/
│   └── requirements.txt
└── README.md

⚙️ Local Setup
Backend
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install python-docx


Create .env inside backend (or export env variables):

GROQ_API_KEY=xxx
NOMIC_API_KEY=xxx
MONGODB_URI=xxx
MONGODB_DB=ai_pdf_tutor


Run backend:

uvicorn app.main:app --host 0.0.0.0 --port 8000

Frontend
cd frontend
npm install


Create .env:

VITE_BACKEND_URL=http://localhost:8000


Run frontend:

npm run dev

🌐 Deployment
Frontend → Vercel

Upload /frontend folder

Set env variable:

VITE_BACKEND_URL=https://your-backend-url

Backend → Railway/Render

Upload /backend folder

Add env variables:

GROQ_API_KEY=
NOMIC_API_KEY=
MONGODB_URI=
MONGODB_DB=ai_pdf_tutor


Start command:

uvicorn app.main:app --host 0.0.0.0 --port $PORT

🧪 API Endpoints

POST /api/documents/upload

POST /api/summaries/full

POST /api/summaries/topic

POST /api/questions

🎯 Why LuminoNote AI?

Free LLMs & embeddings (Groq + Nomic)

Understands multiple file types

Accurate summaries

MCQs for exam prep

Handles handwriting + scanned notes

Lightweight, fast, modern UI
