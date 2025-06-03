from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    question: str
    sql: str
    feedback: str
    correct: bool

@router.post("/")
def submit_feedback(request: FeedbackRequest):
    # TODO: Store feedback for future model improvement
    return {"status": "success"} 