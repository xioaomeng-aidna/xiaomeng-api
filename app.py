from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

# =========================
# 🔑 Gemini API Key
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

    # =========================
    # 🧠 自动模型兼容（关键）
    # =========================
    MODEL_CANDIDATES = [
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
    ]

    for m in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(m)
            # 测试一下模型是否可用（轻量验证）
            break
        except Exception:
            continue


# =========================
# 📦 Request Model
# =========================
class ChatRequest(BaseModel):
    msg: str


# =========================
# 🟢 Root
# =========================
@app.get("/")
def root():
    return {
        "status": "xiaomeng online",
        "model_loaded": model is not None
    }


# =========================
# ❤️ Health Check
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "gemini_loaded": model is not None
    }


# =========================
# 💬 Chat Endpoint
# =========================
@app.post("/chat")
def chat(req: ChatRequest):

    if model is None:
        return {
            "error": "Gemini model not loaded. Check API key or model support."
        }

    try:
        response = model.generate_content(req.msg)
        return {
            "input": req.msg,
            "reply": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }