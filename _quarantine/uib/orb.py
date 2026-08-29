import customtkinter as ctk


class Orb(ctk.CTkCanvas):

    def __init__(self, master):

        super().__init__(
            master,
            width=220,
            height=220,
            bg="#0B0F19",
            highlightthickness=0
        )

        self.radius = 55
        self.direction = 1

        self.circle = self.create_oval(
            110-self.radius,
            110-self.radius,
            110+self.radius,
            110+self.radius,
            fill="#3B82F6",
            outline=""
        )

        self.animate()

    def animate(self):

        if self.radius >= 65:
            self.direction = -1

        elif self.radius <= 55:
            self.direction = 1

        self.radius += self.direction

        self.coords(
            self.circle,
            110-self.radius,
            110-self.radius,
            110+self.radius,
            110+self.radius
        )

        self.after(40, self.animate)