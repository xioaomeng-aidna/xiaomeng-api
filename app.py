from fastapi import FastAPI
from pydantic import BaseModel
import os
from google import genai

app = FastAPI()

# ========================
# 🔌 AI 大脑开关 - 现在先用 gemini
# ========================
AI_PROVIDER = "gemini"  # 以后改成 "meta" 或 "openai" 就换大脑

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

# ========================
# 📦 内存 - 先记在内存里，以后换数据库
# ========================
tracking_log = []  # 记走过哪里
scan_log = []      # 记扫过什么店

# ========================
# 📦 request
# ========================
class ChatRequest(BaseModel):
    msg: str
    floor: str = ""      # 选填：现在在哪一楼
    x: float = 0         # 选填：地图坐标
    y: float = 0

class TrackingRequest(BaseModel):
    user: str = "chan"
    floor: str = "G"
    x: float = 0
    y: float = 0
    shop_nearby: str = ""

class ScanRequest(BaseModel):
    user: str = "chan"
    shop: str = ""
    floor: str = ""
    promo: str = ""

# ========================
# 🧠 AI 大脑 - Gemini 先行
# ========================
def ask_gemini(message: str):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=message
    )
    return response.text

def ask_xiaomeng(message: str):
    if AI_PROVIDER == "gemini":
        return ask_gemini(message)
    # 以后加：
    # elif AI_PROVIDER == "meta":
    #     return ask_meta(message)
    # elif AI_PROVIDER == "openai":
    #     return ask_openai(message)
    return "AI_PROVIDER 还没接"

# ========================
# 🟢 root / health
# ========================
@app.get("/")
def root():
    return {"status": "xiaomeng online", "provider": AI_PROVIDER}

@app.get("/health")
def health():
    return {"status": "ok", "provider": AI_PROVIDER, "gemini": client is not None}

# ========================
# 💬 chat - 地图问小萌
# ========================
@app.post("/chat")
def chat(req: ChatRequest):
    if client is None:
        return {"error": "No API key"}
    try:
        # 把位置也告诉小萌，它才知道你在地图哪里
        prompt = f"用户在商场 {req.floor} 楼，坐标({req.x},{req.y})，他说：{req.msg}。请用简短、像商场导览员一样回答。"
        reply = ask_xiaomeng(prompt)
        return {"reply": reply, "provider": AI_PROVIDER}
    except Exception as e:
        return {"error": str(e)}

# ========================
# 📍 tracking - 后台记位置，不挡地图
# ========================
@app.post("/tracking")
def tracking(req: TrackingRequest):
    tracking_log.append(req.dict())
    # 只留最近 100 条
    if len(tracking_log) > 100:
        tracking_log.pop(0)
    return {"status": "tracked", "count": len(tracking_log)}

@app.get("/tracking")
def get_tracking():
    return {"tracking": tracking_log[-20:]}

# ========================
# 📷 scan - 后台记扫了什么
# ========================
@app.post("/scan")
def scan(req: ScanRequest):
    scan_log.append(req.dict())
    return {"status": "scanned", "shop": req.shop}

@app.get("/scan")
def get_scan():
    return {"scan": scan_log[-20:]}
