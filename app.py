import openai
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
def real_think(user_msg: str):
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        return "OpenAI key not configured."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are OMINEX, a calm, intelligent AI assistant."},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7
        )
        return response.choices[0].message["content"]

    except Exception as e:
        return f"AI error: {str(e)}"

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
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"reply": "Say something to begin."}), 400

    reply = real_think(user_msg)

    return jsonify({
        "reply": reply,
        "mode": "real"
    })

@app.post("/api/demo")
def demo_chat():
    data = request.get_json(force=True) or {}
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"reply": "Say something to begin.", "mode": "demo"}), 400

    return jsonify({
        "reply": "OMINEX demo online. Real intelligence is disabled here.",
        "mode": "demo"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
