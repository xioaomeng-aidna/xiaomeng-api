from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "小萌 API 雲端基地已啟動"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("msg", "")
    return jsonify({"reply": f"小萌雲端版收到：{msg}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
