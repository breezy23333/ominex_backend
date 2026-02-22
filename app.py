# demo/app.py — OMINEX Demo Backend (SAFE / RESTRICTED)
from flask import Flask, request, jsonify, render_template

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# 🔧 Make sure demo can see the real core/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.brain import think

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

app = Flask(__name__)
CORS(app)


@app.get("/api/ping")
def ping():
    return {"ok": True, "mode": "demo"}

@app.get("/")
def demo_home():
    return render_template("index.html")


@app.post("/api/demo")
def demo_chat():
    data = request.get_json(force=True) or {}
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({
            "reply": "Say something to begin.",
            "mode": "demo"
        }), 400

    # 🔒 HARD BLOCKED FEATURES (INTERVIEW SAFE)
    blocked = ["trade", "alert", "learn", "backtest", "delete", "memory", "portfolio save"]
    if any(word in user_msg.lower() for word in blocked):
        return jsonify({
            "reply": "This feature is disabled in demo mode.",
            "mode": "demo"
        })

    # ✅ REAL BRAIN, SAFE MODE
    result = think(user_msg)

    return jsonify({
        "reply": result.get("reply"),
        "mood": result.get("mood", "Neutral"),
        "mode": "demo"
    })


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
