import json


def parse_json(text: str) -> dict:
    """
    Cleans Gemini's response and converts it to a Python dictionary.
    """

    text = text.strip()

    # Remove Markdown code fences if present
    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)