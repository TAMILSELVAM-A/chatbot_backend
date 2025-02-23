from fastapi import FastAPI
from api import endpoints
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mobile Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)

@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}
