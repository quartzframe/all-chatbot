# Engineering Study Assistant

Flask + Gemini chatbot focused only on **Engineering – Civil, Mechanical, Electrical, IT** study and learning.

## 1. Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Put your Gemini API key in `.env`:
```env
GEMINI_API_KEY=your_real_key_here
```

## 2. Run locally
```bash
python app.py
```
Open `http://127.0.0.1:5000`.

## 3. Production with Gunicorn
```bash
gunicorn app:app
```

## Files
- `app.py` — Flask API + server
- `index.html` — single-file UI with CSS + JavaScript
- `chatbot_config.py` — identity, behavior prompt, Gemini model config
- `.env` — local API key configuration placeholder
- `.gitignore` — protects secrets and local files
- `requirements.txt` — dependencies, including Gunicorn

## Scope
The model is prompted to decline off-topic questions and focus on study support for this domain. Prompting is an AI control, not a security boundary, so do not expose secrets or rely on it for access control.
