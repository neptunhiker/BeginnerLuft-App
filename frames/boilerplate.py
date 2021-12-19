from tkinter import ttk

from widgets.buttons import BLButton


class Boilerplate(ttk.Frame):
    """A boilerplate frame"""

    def __init__(self, parent, controller, back_function):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # NAV TOP FRAME
        nav_top_frame = ttk.Frame(self)
        nav_top_frame.grid(row=0, column=0, sticky="EW")
        nav_top_frame.columnconfigure(0, weight=1)

        header = ttk.Label(
            nav_top_frame,
            text=f"{self.__class__.__name__}",
            style="Header.TLabel",
            justify="center",
            anchor="center"
        )
        header.grid(pady=10)

        # CONTENT FRAME
        content_frame = ttk.Frame(self, style="Secondary.TFrame")
        content_frame.grid(row=1, column=0, sticky="NSEW")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)

        lbl = ttk.Label(
            content_frame,
            text=f"Content for {self.__class__.__name__}",
            style="Secondary.TLabel")
        lbl.grid()

        # NAV BOTTOM FRAME
        nav_bottom_frame = ttk.Frame(self)
        nav_bottom_frame.grid(row=2, column=0, sticky="NESW")
        nav_bottom_frame.rowconfigure(0, weight=1)

        back_button = BLButton(
            nav_bottom_frame,
            text="<< zurück",
            command=back_function,
        )
        back_button.grid(sticky="SW", pady=10)
