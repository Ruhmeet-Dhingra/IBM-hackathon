import sounddevice as sd
import soundfile as sf


class Recorder:
    def __init__(self, samplerate=16000):
        self.samplerate = samplerate

    def record(self, duration=5, filename="command.wav"):
        """
        Record audio for a fixed duration and save it as a WAV file.
        """
        print("🎤 Listening for your command...")

        audio = sd.rec(
            int(duration * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        sf.write(filename, audio, self.samplerate)

        print("✅ Recording finished.")

        return filename