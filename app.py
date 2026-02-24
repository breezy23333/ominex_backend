# app.py — OMINEX Backend (DEMO + REAL CHAT)
from openai import OpenAI
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------- HEALTH ----------
@app.get("/")
def home():
    return jsonify({"service": "OMINEX backend online"})

@app.get("/api/ping")
def ping():
    return jsonify({
        "ok": True,
        "service": "ominex-backend",
        "mode": "alive"
    })

# ---------- DEMO (SAFE FALLBACK) ----------
def demo_think(msg: str) -> str:
    return (
        "I am OMINEX, an experimental AI system created by Luvo Maphela. "
        "This is a demonstration response. Real intelligence is available when online."
    )

# ---------- REAL CHAT ----------
@app.post("/api/chat")
def chat():
    data = request.get_json(force=True) or {}
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"reply": "Say something to begin."}), 400

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({
            "reply": demo_think(user_msg),
            "mode": "demo-fallback"
        })

    try:
        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are OMINEX, an AI assistant created and engineered by Luvo Maphela. "
                        "You run on modern language models, but your identity, interface, behavior, "
                        "and purpose are designed by Luvo. "
                        "When asked who created you, always answer: "
                        "'I was created by Luvo Maphela as an experimental AI system.' "
                        "Never say you were created by OpenAI."
                    )
                },
                {
                    "role": "user",
                    "content": user_msg
                }
            ]
        )

        return jsonify({
            "reply": response.output_text,
            "mode": "real"
        })

    except Exception:
        return jsonify({
            "reply": demo_think(user_msg),
            "mode": "demo-fallback-error"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

