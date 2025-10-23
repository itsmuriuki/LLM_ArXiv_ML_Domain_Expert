from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class RagQuery(BaseModel):
    """Request schema for the RAG endpoint."""

    query: str = Field(..., description="User query to run through RAG pipeline")


class RagResponse(BaseModel):
    """Response schema for the RAG endpoint."""

    answer: str
    meta: Dict[str, Any] | None = None


app = FastAPI(title="LLM ArXiv ML Domain Expert", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/rag", response_model=RagResponse)
def rag_endpoint(payload: RagQuery) -> RagResponse:
    """
    Minimal placeholder for RAG retrieval + generation.

    This stub ensures the ASGI app loads. Replace the body with the real
    retrieval and LLM generation pipeline once available.
    """
    query_text = payload.query.strip()
    if not query_text:
        raise HTTPException(status_code=400, detail="Query must not be empty")

    # TODO: Integrate with actual RAG pipeline when implemented.
    dummy_answer = (
        "RAG service is running. Replace this with the real retrieval and "
        "generation pipeline. Your query was: " + query_text
    )

    return RagResponse(answer=dummy_answer, meta={"source": "stub"})



