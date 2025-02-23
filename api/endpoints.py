from fastapi import APIRouter
from services.chatbot import process_query
from models.schemas import QueryRequest, QueryResponse

router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    response_text = process_query(request.user_id,request.query)
    return QueryResponse(response=response_text)
