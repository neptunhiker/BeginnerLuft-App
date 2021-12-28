from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk


class Entry(ttk.Frame):
    """A Frame for a starting screen"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk, next_screen):
        super(Entry, self).__init__(parent)

        # self["style"] = "TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        image = Image.open("assets/bl_logo.png")
        desired_width = 400
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bl_logo = ImageTk.PhotoImage(image)

        lbl_logo = ttk.Label(
            self,
            image=bl_logo,
            cursor="hand2",
        )
        lbl_logo.image = bl_logo
        lbl_logo.grid()

        lbl_logo.bind("<Button-1>", next_screen)
