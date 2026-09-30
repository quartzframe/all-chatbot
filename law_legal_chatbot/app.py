import os
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types

from chatbot_config import (
    CHATBOT_TITLE,
    CHATBOT_DOMAIN,
    CHATBOT_DESCRIPTION,
    SYSTEM_PROMPT,
    MODEL_NAME,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
)

load_dotenv()

# index.html lives beside app.py as requested.
app = Flask(__name__, template_folder=".")
app.config["JSON_SORT_KEYS"] = False

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
client = genai.Client(api_key=API_KEY) if API_KEY else None


def normalize_history(history):
    """Keep only a small, safe, well-formed chat history."""
    cleaned = []
    if not isinstance(history, list):
        return cleaned

    for item in history[-10:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            continue
        content = content.strip()
        if content:
            cleaned.append((role, content[:4000]))
    return cleaned


def build_contents(message, history):
    """Build a compact multi-turn transcript for Gemini."""
    transcript = []
    for role, content in history:
        speaker = "USER" if role == "user" else "ASSISTANT"
        transcript.append(f"{speaker}: {content}")
    transcript.append(f"USER: {message}")
    transcript.append("ASSISTANT:")
    return "\n".join(transcript)


@app.get("/")
def index():
    return render_template(
        "index.html",
        chatbot_title=CHATBOT_TITLE,
        chatbot_domain=CHATBOT_DOMAIN,
        chatbot_description=CHATBOT_DESCRIPTION,
    )


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "chatbot": CHATBOT_TITLE,
        "model": MODEL_NAME,
        "api_key_configured": bool(API_KEY),
    })


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    history = normalize_history(payload.get("history", []))

    if not message:
        return jsonify({"error": "Please enter a question."}), 400

    if len(message) > 4000:
        return jsonify({"error": "Please keep your question within 4000 characters."}), 400

    if not API_KEY or client is None:
        return jsonify({
            "error": "Gemini API key is not configured. Add your key to GEMINI_API_KEY in .env and restart the app."
        }), 500

    prompt = build_contents(message, history)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                candidate_count=1,
            ),
        )
        answer = (response.text or "").strip()
        if not answer:
            answer = "I couldn't generate a study answer for that question. Please rephrase it and try again."
        return jsonify({"answer": answer})
    except Exception:
        app.logger.exception("Gemini API request failed")
        return jsonify({
            "error": "The AI service could not process that request right now. Please try again."
        }), 502


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
