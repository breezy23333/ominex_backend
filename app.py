import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------- HEALTH ----------
@app.get("/api/ping")
def ping():
    return jsonify({
        "ok": True,
        "service": "ominex-backend",
        "mode": "alive"
    })
    
@app.get("/")
def home():
    return jsonify({"service": "OMINEX backend online"})

# ---------- CHAT ----------
def _handle_chat(user_msg: str, demo=False):
    from core.brain import think  # 🔥 MOVED HERE

    user_msg = (user_msg or "").strip()
    if not user_msg:
        return jsonify({"reply": "Say something to begin."}), 400

    result = think(user_msg)
    return jsonify({
        "reply": result.get("reply"),
        "mood": result.get("mood", "Neutral"),
        "mode": "demo" if demo else "live"
    })

@app.post("/api/chat")
def chat():
    data = request.get_json(force=True) or {}
    return _handle_chat(data.get("message"), demo=False)

@app.post("/api/demo")
def demo_chat():
    data = request.get_json(force=True) or {}
    return _handle_chat(data.get("message"), demo=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
