from fastapi import APIRouter
from pydantic import BaseModel
from ..services.langgraph_flows import summary_graph

router = APIRouter()

class FullSummaryRequest(BaseModel):
    doc_id: str

class TopicSummaryRequest(BaseModel):
    doc_id: str
    topic: str

@router.post("/full")
async def full_summary(req: FullSummaryRequest):
    state = {
        "doc_id": req.doc_id,
        "mode": "full_summary",
        "topic": None,
        "summary": "",
    }
    result = summary_graph.invoke(state)
    return {"summary": result.get("summary", "")}

@router.post("/topic")
async def topic_summary(req: TopicSummaryRequest):
    state = {
        "doc_id": req.doc_id,
        "mode": "topic_summary",
        "topic": req.topic,
        "summary": "",
    }
    result = summary_graph.invoke(state)
    return {"summary": result.get("summary", "")}
