import time

from brain_v2.gemini_provider import ask
from voice import speaker, transcribe

start = time.time()
command = transcribe()
print(f"Whisper: {time.time() - start:.2f}s")

start = time.time()
reply = ask(command)
print(f"Gemini: {time.time() - start:.2f}s")

start = time.time()
speaker.speak(reply)
print(f"TTS: {time.time() - start:.2f}s")