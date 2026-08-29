import threading
import time

import numpy as np
import sounddevice as sd
from openwakeword import Model

from config import WAKE_WORD_MODEL, WAKE_WORD_NAME, WAKE_WORD_PHRASE


class WakeWordDetector:
    def __init__(
        self,
        callback=None,
        threshold=0.85,
        model_name: str = WAKE_WORD_MODEL,
        wake_word_name: str = WAKE_WORD_NAME,
        wake_word_phrase: str = WAKE_WORD_PHRASE,
    ):
        self.callback = callback
        self.threshold = threshold
        self.wake_word_name = wake_word_name
        self.wake_word_phrase = wake_word_phrase

        self.model = Model(wakeword_models=[model_name])

        self.busy = False
        self.running = False
        self.stream = None

        self.last_detection = 0
        self.previous_score = 0.0

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            print(status)

        if self.busy:
            return

        # Convert float32 microphone input to int16
        audio = (indata[:, 0] * 32767).astype(np.int16)

        prediction = self.model.predict(audio)
        score = float(prediction.get(self.wake_word_name, 0.0))

        now = time.time()

        # Trigger only when crossing the threshold
        triggered = (
            score >= self.threshold
            and self.previous_score < self.threshold
            and (now - self.last_detection) > 2
            and not self.busy
        )

        self.previous_score = score

        if triggered:
            self.busy = True
            self.last_detection = now

            print(f"Wake word detected! ({score:.3f})")

            if self.callback:
                threading.Thread(
                    target=self.callback,
                    daemon=True
                ).start()

    def start(self):
        if self.running:
            return

        print("Listening... Say 'Hey Jarvis'")

        self.stream = sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype="float32",
            blocksize=1280,
            callback=self.audio_callback,
        )

        self.stream.start()
        self.running = True

        print("Microphone stream started.")

    def stop(self):
        if not self.running:
            return

        self.running = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        print("Microphone stopped.")
