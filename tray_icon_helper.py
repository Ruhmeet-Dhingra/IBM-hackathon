import os
from PIL import Image

def get_icon():
    # Try to load a nice icon, else fallback to a solid color
    icon_path = os.path.join(os.path.dirname(__file__), "data", "icon.ico")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    else:
        return Image.new("RGB", (64, 64), (43, 43, 43))
