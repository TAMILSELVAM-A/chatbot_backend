import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="Mobile Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
)

from api import endpoints
app.include_router(endpoints.router)

@app.get("/")
def home():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }
    return JSONResponse(content={"message": "Chatbot API is running!"}, headers=headers)

@app.options("/{full_path:path}")
async def preflight(full_path: str, request: Request):
    return JSONResponse(content={}, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
