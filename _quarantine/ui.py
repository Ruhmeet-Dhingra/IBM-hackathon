import customtkinter as ctk

from core.dispatcher import process_input

history = []
history_index = 0

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def create_app():
    app = ctk.CTk()

    app.title("ROV")
    app.geometry("450x450")

    title = ctk.CTkLabel(
        app,
        text="ROV",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=30)

    welcome = ctk.CTkLabel(
        app,
        text="Welcome back.",
        font=("Arial", 18)
    )
    welcome.pack()

    command_box = ctk.CTkEntry(
        app,
        width=500,
        height=40,
        placeholder_text="Enter a command..."
    )
    command_box.pack(pady=40)

    def run_command():
        global history_index

        command = command_box.get()

        if command.strip() == "":
            return

        history.append(command)
        history_index = len(history)

        process_input(command)

        command_box.delete(0, "end")
        command_box.focus()

    def previous_command(event):
        global history_index

        if not history:
            return

        history_index = max(0, history_index - 1)

        command_box.delete(0, "end")
        command_box.insert(0, history[history_index])

    def next_command(event):
        global history_index

        if not history:
            return

        history_index = min(len(history) - 1, history_index + 1)

        command_box.delete(0, "end")
        command_box.insert(0, history[history_index])

    command_box.bind("<Return>", lambda event: run_command())
    command_box.bind("<Up>", previous_command)
    command_box.bind("<Down>", next_command)

    execute_button = ctk.CTkButton(
        app,
        text="Execute",
        command=run_command
    )
    execute_button.pack()

    command_box.focus()

    return app