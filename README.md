# All Chatbots — Gemini + Flask Study Assistants

This folder contains 10 separate, ready-to-run Flask + Gemini study chatbots:

- Healthcare
- IT & Software
- Banking & Finance
- Engineering
- Education
- Law & Legal
- Business & Management
- Sales & Marketing
- Travel & Hospitality
- Government Sector

Each chatbot is self-contained and has the requested files:
`app.py`, `index.html` (CSS + JS embedded), `chatbot_config.py`, `requirements.txt`, `.gitignore`, `.env`, and a README.

## Gemini model
The project uses `gemini-3.1-flash-lite`, the GA model ID listed by Google's Gemini API documentation for Gemini 3.1 Flash-Lite. See:
https://ai.google.dev/gemini-api/docs/models

## Quick start for any chatbot
```bash
cd healthcare_chatbot
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Edit `.env` and set:
```env
GEMINI_API_KEY=your_real_gemini_api_key_here
```

Then:
```bash
python app.py
```

For production:
```bash
gunicorn app:app
```

## Security note
The included `.env` contains only a placeholder key. Replace it with your real key locally, and never commit a real API key. `.gitignore` already excludes `.env`.

## Design
Each chatbot shares the same responsive single-file UI architecture while using a domain-specific accent color, title, example prompts, and system prompt. The system prompt explicitly keeps the bot focused on study and learning within its domain and declines unrelated questions.
