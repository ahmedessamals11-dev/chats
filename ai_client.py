import requests
from config import OPENROUTER_API_KEY, MODEL

API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are an assistant helping a live customer service agent in real time. "
    "You will be given a transcript of the ongoing chat with a customer, "
    "extracted via OCR from a screen capture (so it may contain small typos "
    "or formatting glitches). "
    "Draft ONE suggested reply the agent could send next.\n\n"
    "Requirements:\n"
    "- Lead with genuine, specific empathy for the customer's situation "
    "(not generic phrases like 'I understand your frustration' repeated every time).\n"
    "- Use warm, positive, solution-focused language.\n"
    "- Be concise: 2-4 sentences.\n"
    "- Be professional and calm, never dismissive.\n"
    "- Do NOT invent facts about the customer's account, order, or policies "
    "that aren't in the transcript.\n"
    "- If the transcript is unclear or incomplete, write a reply that asks a "
    "clarifying question empathetically rather than guessing.\n"
    "- Return ONLY the suggested reply text. No preamble, no labels, no quotes."
)


def generate_response(chat_transcript: str, extra_instructions: str = "") -> str:
    """Send the OCR'd chat transcript to the model and return a suggested reply."""
    if not chat_transcript.strip():
        return "No chat text detected yet. Capture the chat area first."

    user_content = f"Chat transcript so far:\n---\n{chat_transcript.strip()}\n---"
    if extra_instructions.strip():
        user_content += (
            f"\n\nAdditional instruction from the agent: {extra_instructions.strip()}"
        )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.6,
        "max_tokens": 300,
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()
