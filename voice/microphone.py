import sounddevice as sd
import soundfile as sf


def record_audio(filename="recording.wav", duration=5, sample_rate=16000):

    print("Recording...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        device=1
    )

    sd.wait()

    sf.write(filename, audio, sample_rate)

    print("Recording saved.")