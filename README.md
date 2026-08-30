# Customer Service Copilot

A small desktop tool for live-chat customer service agents. You select the
area of your screen where the chat window is; the tool reads the chat text
(OCR) and asks an AI model to draft an empathetic, positive-toned reply,
shown in a panel on the right.

## ⚠️ Security note

An API key was shared in the chat that generated this tool. **That key
should be treated as compromised — revoke/regenerate it in your OpenRouter
dashboard before using this app.** Put your *new* key only in a local `.env`
file (see below), never in the source code, and never paste it into a chat
or commit it to version control.

## 1. Install system dependency: Tesseract OCR

The OCR step needs the Tesseract binary installed separately from the
Python package.

- **Windows**: install from https://github.com/UB-Mannheim/tesseract/wiki,
  then make sure `tesseract.exe` is on your PATH (or set
  `pytesseract.pytesseract.tesseract_cmd` in `screen_capture.py` to its
  full path).
- **macOS**: `brew install tesseract`
- **Linux (Debian/Ubuntu)**: `sudo apt install tesseract-ocr`

## 2. Install Python dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Add your API key

```bash
cp .env.example .env
```

Edit `.env` and paste your (new, rotated) OpenRouter key:

```
OPENROUTER_API_KEY=sk-or-v1-...your-new-key...
```

## 4. Run it

```bash
python main.py
```

## How to use it while sharing your screen

1. Click **"1. Select Chat Area"**. The screen dims — drag a rectangle
   around just the chat window/conversation you're responding to, then
   release the mouse.
2. Whenever a new customer message comes in, click
   **"2. Capture & Suggest Reply"**. The tool screenshots that region,
   reads the text with OCR (shown/editable in the left box), and asks the
   AI to draft an empathetic reply in the right-hand panel.
3. Review and edit the suggested reply, then click **"Copy to Clipboard"**
   and paste it into your chat tool.
4. You can add a short note in the "Extra note for AI" field (e.g. "keep it
   very brief" or "customer is asking for a refund") before generating.

The AI is prompted to lead with empathy, use warm/positive language, stay
concise, and avoid inventing account or policy details it wasn't given —
but always review its suggestion before sending, since OCR can introduce
errors and the model doesn't know your company's actual policies unless
you paste them into the transcript.

## Notes / limitations

- OCR quality depends on font size and contrast in the chat window — a
  clean, reasonably large chat font works best.
- This only reads text on your own screen; it does not integrate directly
  with any chat platform's API.
- The selected region stays fixed until you re-select it, so keep the chat
  window in the same place on screen.
