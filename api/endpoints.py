from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.schemas import QueryRequest, QueryResponse
from services.chatbot import process_query

router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    response_text = process_query(request.user_id, request.query)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    return JSONResponse(content={"response": response_text}, headers=headers)
