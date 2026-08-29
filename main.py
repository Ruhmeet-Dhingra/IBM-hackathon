import time
import traceback

from voice.detector import WakeWordDetector
from voice.recorder import Recorder
from voice.whisper_engine import transcribe

from core.audio import speaker
from brain_v2.brain import Brain
from router.router import Router




class ROV:

    def __init__(self):
        self.recorder = Recorder()
        self.detector = WakeWordDetector(
            callback=self.on_wake
        )
        self.brain = Brain()

        self.router = Router()

    def on_wake(self):

        try:

            # Acknowledge wake word
            speaker.speak("Yes sir.")

            # Record user's command
            audio = self.recorder.record()

            # Convert speech to text
            command = transcribe(audio)

            if not command.strip():
                print("No command detected.")
                return

            print(f"You: {command}")

            # Process command
            try:
                plan = self.brain.process(command)
            except ValueError as e:
                speaker.speak(f"Sorry, {str(e)}")
                return

            reply = self.router.execute(plan)

            if reply is None:
                return

            if isinstance(reply, list):
                reply = " ".join(
                    result.message
                    if hasattr(result, "message")
                    else str(result)
                    for result in reply
                )

            print(f"ROV: {reply}")

            # -----------------------------
            # Normal chat response
            # -----------------------------
            if isinstance(reply, str):

                speaker.speak(
                    reply.replace("**", "")
                )

            # -----------------------------
            # Developer Mode response
            # -----------------------------
            elif isinstance(reply, dict):

                status = reply.get("status", "unknown")

                if status == "success":

                    speaker.speak(
                        f"Plugin {reply['plugin_name']} created successfully."
                    )

                elif status == "review_failed":

                    speaker.speak(
                        "Plugin generation failed review."
                    )

                elif status == "installation_failed":

                    speaker.speak(
                        "Plugin installation failed."
                    )

                elif status == "failed":

                    speaker.speak(
                        reply.get(
                            "message",
                            "Developer Mode failed."
                        )
                    )

                elif status == "error":

                    speaker.speak(
                        reply.get(
                            "message",
                            "An error occurred."
                        )
                    )

                else:

                    speaker.speak(
                        "Developer Mode completed."
                    )

            else:

                speaker.speak(str(reply))

        except Exception:
            traceback.print_exc()

        finally:

            # Allow wake-word detection again
            self.detector.busy = False

    def on_text_command(self, command: str):
        print(f"You (Text): {command}")
        
        try:
            plan = self.brain.process(command)
        except ValueError as e:
            speaker.speak(f"Sorry, {str(e)}")
            return

        reply = self.router.execute(plan)

        if reply is None:
            return

        if isinstance(reply, list):
            reply = " ".join(
                result.message if hasattr(result, "message") else str(result)
                for result in reply
            )

        print(f"ROV: {reply}")
        
        if isinstance(reply, str):
            speaker.speak(reply.replace("**", ""))
        else:
            speaker.speak(str(reply))

    def start_tray(self):
        import pystray
        from tray_icon_helper import get_icon
        import tkinter as tk
        import tkinter.simpledialog
        import threading

        def on_command(icon, item):
            # Run tkinter dialog in the callback thread
            def show_dialog():
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                command = tkinter.simpledialog.askstring("Command ROV", "Enter your command:")
                root.destroy()
                if command and command.strip():
                    # Call on_text_command
                    self.on_text_command(command.strip())
            
            # Start in a new thread to avoid blocking tray
            t = threading.Thread(target=show_dialog)
            t.daemon = True
            t.start()

        def on_exit(icon, item):
            icon.stop()
            self.detector.stop()
            import os
            os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem("Command ROV...", on_command, default=True),
            pystray.MenuItem("Exit", on_exit)
        )

        self.tray_icon = pystray.Icon("ROV", get_icon(), "ROV Assistant", menu)
        
    def start(self):

        self.detector.start()
        self.start_tray()

        print("ROV is running...")
        print(f"Say '{self.detector.wake_word_phrase}' to wake me.")

        try:
            # Run the tray icon in the main thread to ensure it appears in Windows
            self.tray_icon.run()

        except KeyboardInterrupt:
            print("\nStopping ROV...")
            self.detector.stop()
            self.tray_icon.stop()


if __name__ == "__main__":

    rov = ROV()
    rov.start()
