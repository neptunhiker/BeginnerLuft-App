from tkinter import ttk


class Entry(ttk.Frame):
    """A Frame for a starting screen"""

    def __init__(self, parent, controller, next_screen):
        super(Entry, self).__init__(parent)

        # self["style"] = "TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        header = ttk.Label(
            self,
            style="Title.TLabel",
            text="BeginnerLuft",
            anchor="center",
        )
        header.grid(row=0, column=0, sticky="EW")
        header.bind("<Button-1>", next_screen)
