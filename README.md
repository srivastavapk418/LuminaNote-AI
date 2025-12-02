# AI PDF Tutor (Full Stack)

This zip includes:

- `backend/` – Python FastAPI + LangGraph backend
- `frontend/` – React (Vite) frontend

## Backend

Features:

- Upload PDF or image
- Extract text (pdfplumber / pytesseract)
- Store original file in MongoDB
- Chunk text + store embeddings
- LangGraph flows for:
  - MCQ generation
  - Full summary
  - Topic-based summary

Run locally:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
export MONGODB_URI=your_mongodb_uri
export MONGODB_DB=ai_pdf_tutor
bash run.sh
```

Backend runs on `http://localhost:8000`.

## Frontend

React app that talks to the backend.

```bash
cd frontend
npm install
echo "VITE_BACKEND_URL=http://localhost:8000" > .env
npm run dev
```

Open `http://localhost:5173`.

For Vercel, deploy the `frontend` folder and set `VITE_BACKEND_URL` env var to your deployed backend URL.
