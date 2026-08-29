import speech_recognition as sr


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        """
        Listen for one command and return it as text.
        """
        with sr.Microphone() as source:
            print("🎤 Listening for your command...")

            # Reduce background noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text

        except sr.UnknownValueError:
            print("❌ Sorry, I couldn't understand you.")
            return None

        except sr.RequestError as e:
            print(f"Speech Recognition Error: {e}")
            return None