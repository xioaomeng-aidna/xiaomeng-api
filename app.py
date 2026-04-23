from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

# =========================
# 🔑 API KEY
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


# =========================
# 📦 request
# =========================
class ChatRequest(BaseModel):
    msg: str


# =========================
# 🟢 root
# =========================
@app.get("/")
def root():
    return {"status": "xiaomeng online"}


# =========================
# ❤️ health
# =========================
@app.get("/health")
def health():
    return {"status": "ok", "gemini": client is not None}


# =========================
# 💬 chat
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    if client is None:
        return {"error": "No API key"}

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=req.msg
        )

        return {"reply": response.text}

    except Exception as e:
        return {"error": str(e)}


