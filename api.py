import requests

response = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={
        'Authorization': 'Bearer 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',
        'HTTP-Referer': '<YOUR_SITE_URL>',
        'X-Title': '<YOUR_SITE_NAME>',
        'Content-Type': 'application/json',
    },
    json={
        'model': 'openai/gpt-4o',
        'messages': [
            {
                'role': 'user',
                'content': 'What is the meaning of life?',
            }
        ],
    },
    timeout=30,
)

response.raise_for_status()
print(response.json())