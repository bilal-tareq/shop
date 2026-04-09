from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_ai(request: ChatRequest):
    # Mock AI Service
    return {
        "answer": f"AI Response to: {request.question} - We recommend checking out our latest summer collection!"
    }
