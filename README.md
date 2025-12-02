# ⭐ LuminoNote AI:
Your smart study assistant that understands PDFs, images, handwritten notes, DOCX files, and code files — and turns them into summaries, topic explanations, and MCQs.
### 🔗 Project Link: 
- Click here ⬅️[https://lumina-note-ai.vercel.app/]

---

## 🚀 Features:
- 📄 Supports PDF, scanned PDFs, images, DOCX, TXT, and code files
- 🔍 OCR (handwritten & scanned notes) using Tesseract
- 🧠 Full & topic summaries using Groq LLM (free)
- 🎯 MCQs with answers & explanations
- 🗂️ Semantic search using Nomic embeddings (free)
- 🧹 Auto-delete documents older than 3 days
- 🎨 Modern React + Vite frontend

---

## 🧠 Tech Stack:
### Frontend:
- React
- Vite
- JavaScript

### Backend:
- FastAPI (Python)
- Groq LLM (Mixtral / Gemma)
- Nomic Embeddings
- LangGraph
- Tesseract OCR
- PyMuPDF, python-docx

### Database
- MongoDB Atlas

---

## 📁 Project Structure:
```
LuminoNote-AI/
├── frontend/
│   ├── src/
│   └── package.json
├── backend/
│   ├── app/
│   ├── routers/
│   ├── services/
│   └── main.py
└── README.md
```

---

## ⚙️ Local Setup:
### 🔧 Backend Setup:
- cd backend
- python -m venv .venv
- .\.venv\Scripts\activate
- pip install -r requirements.txt
- pip install python-docx
#### Create a .env inside backend:
- GROQ_API_KEY=your_key
- NOMIC_API_KEY=your_key
- MONGODB_URI=your_mongodb_uri
- MONGODB_DB=ai_pdf_tutor
#### Run backend:
- uvicorn app.main:app --host 0.0.0.0 --port 8000

### 💻 Frontend :
- cd frontend
- npm install
#### Create /frontend/.env:
- VITE_BACKEND_URL=http://localhost:8000
#### Run frontend:
- npm run dev

--- 

## 📡 API Endpoints:
- POST /api/documents/upload
- POST /api/summaries/full
- POST /api/summaries/topic
- POST /api/questions

---

## 🎯 Why LuminoNote AI?
- Free, fast, and powerful (Groq + Nomic)
- Works on handwritten notes
- Converts study material into knowledge
- Clean UI, responsive, modern
- Perfect for students, teachers, self-learners

---

## 🧑‍💻 Author:
- Prateek Kumar Srivastava
- AI Developer • MERN Developer • CS Student

