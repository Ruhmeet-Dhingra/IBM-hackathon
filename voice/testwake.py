from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Supported models:\n")

for model in client.models.list():
    # Only show models that support generate_content
    if "generateContent" in getattr(model, "supported_actions", []):
        print(model.name)
        