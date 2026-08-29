from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw


class Tray:

    def __init__(self):
        self.icon = Icon(
            "ROV",
            self.create_image(),
            "ROV Assistant",
            Menu(
                MenuItem("Exit", self.exit_app)
            )
        )

    def create_image(self):
        image = Image.new("RGB", (64, 64), "black")
        draw = ImageDraw.Draw(image)

        draw.ellipse((12, 12, 52, 52), fill="cyan")

        return image

    def exit_app(self, icon, item):
        icon.stop()

    def start(self):
        self.icon.run_detached()