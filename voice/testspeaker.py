import time

from brain.gemini import ask
from voice import recorder, speaker
from voice.wisper_engine import transcribe

audio = recorder.record()

start = time.time()
command = transcribe(audio)
print(f"Whisper took: {time.time() - start:.2f} seconds")

start = time.time()
reply = ask(command)
print(f"Gemini took: {time.time() - start:.2f} seconds")

start = time.time()
speaker.speak(reply)
print(f"TTS took: {time.time() - start:.2f} seconds")