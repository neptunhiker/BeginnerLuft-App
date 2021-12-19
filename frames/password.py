from tkinter import ttk


class Password(ttk.Frame):
    """A Frame for password settings"""

    def __init__(self, parent, controller, back_function):
        super(Password, self).__init__(parent)

        # self["style"] = bl_colors["bg primary"]

        self.controller = controller

        nav_bar = ttk.Frame(self)
        nav_bar.grid(sticky="EW")

        back_button = ttk.Button(
            nav_bar,
            text="<< zurück",
            command=back_function
        )
        back_button.grid(sticky="W")

        password_frame = ttk.Frame(self)
        password_frame.grid()

        header = ttk.Label(
            password_frame,
            text="Passwort ändern")
        header.grid()
