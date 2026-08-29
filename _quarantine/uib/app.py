import customtkinter as ctk

from uib.orb import Orb
from uib.theme import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def create_app():

    app = ctk.CTk()

    app.title("ROV")
    app.geometry("500x650")
    app.configure(fg_color=BACKGROUND)

    # --------------------
    # Title
    # --------------------

    title = ctk.CTkLabel(
        app,
        text="ROV",
        font=TITLE_FONT,
        text_color=TEXT
    )

    title.pack(pady=(25, 10))

    # --------------------
    # Orb
    # --------------------

    orb = Orb(app)
    orb.pack(pady=20)

    # --------------------
    # Status
    # --------------------

    status = ctk.CTkLabel(
        app,
        text="Idle",
        font=STATUS_FONT,
        text_color=TEXT
    )

    status.pack(pady=20)

    # --------------------
    # Command Box
    # --------------------

    command_box = ctk.CTkEntry(
        app,
        width=350,
        height=40,
        placeholder_text="Enter command..."
    )

    command_box.pack(pady=20)

    # --------------------
    # Button
    # --------------------

    execute_button = ctk.CTkButton(
        app,
        text="Execute"
    )

    execute_button.pack()

    return app