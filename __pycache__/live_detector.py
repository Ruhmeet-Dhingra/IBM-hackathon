import numpy as np
import sounddevice as sd
from openwakeword import Model

model = Model(wakeword_models=["hey_jarvis"])

print("🎤 Listening... Say 'Hey Jarvis'")

THRESHOLD = 0.5

def audio_callback(indata, frames, time, status):
    if status:
        print(status)

    audio = (indata[:, 0] * 32767).astype(np.int16)

    prediction = model.predict(audio)

    print(repr(prediction))

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="float32",
    blocksize=1280,
    callback=audio_callback,
):
    print("Microphone stream started.")
    input("Press Enter to stop...\n")