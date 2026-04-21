from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

# Request model
class ChatRequest(BaseModel):
    msg: str

# Root
@app.get("/")
def root():
    return {"status": "xiaomeng online"}

# Health
@app.get("/health")
def health():
    return {"status": "ok", "gemini": model is not None}

# Chat
@app.post("/chat")
def chat(req: ChatRequest):
    if model is None:
        return {"error": "No API key"}

    try:
        res = model.generate_content(req.msg)
        return {"reply": res.text}
    except Exception as e:
        return {"error": str(e)}
