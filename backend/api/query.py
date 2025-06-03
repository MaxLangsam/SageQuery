from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.services.nl2sql import nl_to_sql_service
from backend.services.sql_executor import execute_sql_service
from backend.services.rag import rag_grounding_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    preview: bool = False

class QueryResponse(BaseModel):
    sql: str
    results: list = None
    grounded_examples: list = None

@router.post("/", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    # Retrieve relevant examples for grounding
    examples = rag_grounding_service(request.question)
    # Translate NL to SQL
    sql = nl_to_sql_service(request.question, examples)
    if request.preview:
        return QueryResponse(sql=sql, results=None, grounded_examples=examples)
    # Execute SQL securely
    try:
        results = execute_sql_service(sql)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return QueryResponse(sql=sql, results=results, grounded_examples=examples) 