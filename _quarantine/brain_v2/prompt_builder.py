import json

from brain.intents import INTENTS


def build_system_prompt() -> str:

    prompt = """
You are ROV's planner.

Your job is to convert the user's request into structured JSON.

Rules:
- Return ONLY valid JSON.
- Do not explain.
- Do not answer the user's request.
- Do not use markdown.
- Do not wrap the JSON in ```.

Available intents:

"""

    for intent, info in INTENTS.items():

        prompt += f"\nIntent: {intent}\n"
        prompt += f"Description: {info['description']}\n"

        prompt += "Parameters:\n"

        prompt += json.dumps(
            info["parameters"],
            indent=4
        )

        prompt += "\n"

    prompt += """

If none of the intents match, return:

{
    "intent": "answer_question",
    "parameters": {
        "query": "<original request>"
    }
}

Schema:

{
    "intent": "",
    "parameters": {}
}
"""

    return prompt