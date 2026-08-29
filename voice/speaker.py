import asyncio
import edge_tts
import tempfile
import os
import vlc
import time


class Speaker:
    def __init__(self):
        self.player = None

    async def _generate_audio(self, text, filename):
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-GB-RyanNeural",
            rate = "+10%",
            volume = "+10%"
        )
        await communicate.save(filename)

    def speak(self, text):
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        filename = temp.name
        temp.close()

        asyncio.run(self._generate_audio(text, filename))

        media = vlc.Media(filename)

        self.player = vlc.MediaPlayer()
        self.player.set_media(media)

        self.player.play()

        # Wait up to 2 seconds for VLC to actually start playing
        timeout = 2.0
        while not self.player.is_playing() and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1

        # Now wait for the audio to finish
        while self.player.is_playing():
            time.sleep(0.1)

        self.player.stop()
        self.player.release()

        # Retry mechanism for file deletion in case VLC is slow to release the file handle
        for _ in range(5):
            try:
                os.remove(filename)
                break
            except PermissionError:
                time.sleep(0.2)