import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.brain import think

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response
# ---------- HEALTH ----------

@app.get("/")
def home():
    return jsonify({
        "status": "OMINEX backend online",
        "message": "Use /api/chat, /api/demo, or /api/ping"
    })

@app.get("/api/ping")
def ping():
    return {"ok": True, "mode": "demo"}

# ---------- DEMO UI ----------
@app.get("/demo")
def demo_home():
    return render_template("index.html")

# ---------- CHAT ----------
def _handle_chat(user_msg: str, demo=False):
    user_msg = (user_msg or "").strip()

    if not user_msg:
        return jsonify({"reply": "Say something to begin."}), 400

    if demo:
        blocked = ["trade", "alert", "learn", "backtest", "delete", "memory", "portfolio save"]
        if any(word in user_msg.lower() for word in blocked):
            return jsonify({"reply": "This feature is disabled in demo mode.", "mode": "demo"})

    result = think(user_msg)

    return jsonify({
        "reply": result.get("reply"),
        "mood": result.get("mood", "Neutral"),
        "mode": "live" if not demo else "demo"
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
