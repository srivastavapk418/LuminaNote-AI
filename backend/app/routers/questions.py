from fastapi import APIRouter
from pydantic import BaseModel
from ..services.langgraph_flows import question_graph

router = APIRouter()

class QuestionRequest(BaseModel):
    doc_id: str
    num_questions: int = 5

@router.post("/")
async def generate_questions(req: QuestionRequest):
    state = {
        "doc_id": req.doc_id,
        "num_questions": req.num_questions,
        "mode": "questions",
        "questions": [],
        "answers": [],
    }
    result = question_graph.invoke(state)
    return {
        "questions": result.get("questions", []),
        "answers": result.get("answers", []),
    }
