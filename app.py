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

# ---------- REAL CHAT ----------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.post("/api/chat")
def chat():
    data = request.get_json(force=True) or {}
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"reply": "Say something to begin."}), 400

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "You are OMINEX — calm, intelligent, precise, and professional."
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

    except Exception as e:
        return jsonify({
            "reply": f"AI error: {str(e)}",
            "mode": "error"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
