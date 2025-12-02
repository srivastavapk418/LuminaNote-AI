from typing import TypedDict, List, Literal, Optional
from langgraph.graph import StateGraph, END

from ..config import llm
from .vector_store import search_document

import json


# ========= State Types =========


class QuestionState(TypedDict, total=False):
    doc_id: str
    num_questions: int
    mode: Literal["questions"]
    questions: List[str]
    answers: List[str]


class SummaryState(TypedDict, total=False):
    doc_id: str
    mode: Literal["full_summary", "topic_summary"]
    topic: Optional[str]
    summary: str


# ========= Helpers =========


def _extract_json_array(text: str) -> str:
    """
    Try to pull out the JSON array from a model response.
    Handles cases where the JSON is wrapped in markdown code fences
    or has some explanation text around it.
    """
    text = text.strip()

    # If there are markdown code fences, keep only the inside
    if "```" in text:
        parts = text.split("```")
        # typically: ['', 'json', '[ ... ]', '']
        for part in parts:
            part = part.strip()
            if part.startswith("[") and part.endswith("]"):
                return part

    # Fallback: take from first '[' to last ']'
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]

    return text


# ========= Nodes =========


def generate_mcqs_node(state: QuestionState) -> QuestionState:
    """
    Use semantic search to pull the most important chunks, then ask the LLM
    (Groq) to generate MCQs in JSON form, then post-process into
    plain-text Q&A lists for the frontend.
    """
    chunks = search_document(state["doc_id"], "important key points", n_results=10)
    context = "\n\n".join(c["text"] for c in chunks)

    if not context.strip():
        # No text available for this document
        state["questions"] = []
        state["answers"] = []
        return state

    num_q = state.get("num_questions", 5)

    prompt = f"""You are a teacher. Based ONLY on the following study material, create {num_q} objective MCQ questions.

Material:
{context}

Return ONLY a JSON array with this exact structure, no extra text:

[
  {{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "B",
    "explanation": "Short explanation of why this is correct."
  }}
]
"""

    resp = llm.invoke(prompt)
    content = getattr(resp, "content", str(resp))

    data = []
    try:
        json_str = _extract_json_array(content)
        data = json.loads(json_str)
    except Exception:
        # As a last-ditch attempt, ask the model to fix it
        fix_prompt = f"""You previously tried to return MCQs but the JSON was invalid.

Now return ONLY a valid JSON array of MCQs in this format, no explanation text outside the JSON:

[
  {{
    "question": "Question text here",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "B",
    "explanation": "Short explanation of why this is correct."
  }}
]

Here is your previous output, fix it to valid JSON:
```text
{content}
```"""
        fixed = llm.invoke(fix_prompt)
        try:
            fixed_content = getattr(fixed, "content", str(fixed))
            json_str = _extract_json_array(fixed_content)
            data = json.loads(json_str)
        except Exception:
            data = []

    questions: List[str] = []
    answers: List[str] = []

    for item in data:
        q_text = item.get("question", "").strip()
        opts = item.get("options") or []
        ans = item.get("answer", "").strip()
        expl = item.get("explanation", "").strip()

        # Build question block
        q_block = q_text + "\n"
        for i, opt in enumerate(opts):
            q_block += f"  {chr(65 + i)}. {opt}\n"
        questions.append(q_block)

        # Build answer block
        answers.append(f"Correct: {ans} - {expl}")

    state["questions"] = questions
    state["answers"] = answers
    return state


def full_summary_node(state: SummaryState) -> SummaryState:
    """
    Summarize the entire document using the most relevant chunks.
    """
    chunks = search_document(state["doc_id"], "overall content of document", n_results=15)
    context = "\n\n".join(c["text"] for c in chunks)

    if not context.strip():
        state["summary"] = (
            "There is no text to summarize for this document. "
            "It may be an image-only or empty file."
        )
        return state

    prompt = """Summarize the following document in a clear, concise way for a student.
Focus on the main ideas, important definitions, and any key formulas.

Text:
""" + context

    resp = llm.invoke(prompt)
    state["summary"] = getattr(resp, "content", str(resp))
    return state


def topic_summary_node(state: SummaryState) -> SummaryState:
    """
    Summarize only the parts of the document related to a specific topic.
    """
    topic = state.get("topic") or ""
    chunks = search_document(state["doc_id"], topic, n_results=8)
    context = "\n\n".join(c["text"] for c in chunks)

    if not context.strip():
        state["summary"] = (
            f'There is no text related to the topic "{topic}" in this document '
            "or the document contains no extractable text."
        )
        return state

    prompt = f"""You are an AI tutor. Summarize ONLY the parts of this text relevant to the topic: "{topic}".

Text:
{context}
"""

    resp = llm.invoke(prompt)
    state["summary"] = getattr(resp, "content", str(resp))
    return state


# ========= Graph Builders =========


def build_question_graph():
    graph = StateGraph(QuestionState)
    graph.add_node("generate_mcqs", generate_mcqs_node)
    graph.set_entry_point("generate_mcqs")
    graph.add_edge("generate_mcqs", END)
    return graph.compile()


def build_summary_graph():
    graph = StateGraph(SummaryState)
    graph.add_node("full_summary", full_summary_node)
    graph.add_node("topic_summary", topic_summary_node)

    def router(state: SummaryState):
        return "topic_summary" if state.get("mode") == "topic_summary" else "full_summary"

    graph.set_conditional_entry_point(router)
    graph.add_edge("full_summary", END)
    graph.add_edge("topic_summary", END)
    return graph.compile()


# ========= Compiled Graphs =========

question_graph = build_question_graph()
summary_graph = build_summary_graph()
