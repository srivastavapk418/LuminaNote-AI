from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import documents, questions, summaries

app = FastAPI(title="AI PDF Tutor Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
app.include_router(summaries.router, prefix="/api/summaries", tags=["summaries"])

@app.get("/health")
def health():
    return {"status": "ok"}
