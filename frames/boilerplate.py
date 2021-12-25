from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from design.colors import bl_colors
from frames.dashboard import Dashboard
from tools import helpers
from widgets.buttons import BLImageButtonLabel


class Boilerplate(ttk.Frame):
    """A boilerplate frame"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        frame_left = ttk.Frame(self)
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)

        # create background image
        image = Image.open("assets/office01.jpg")
        desired_width = 1200
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        # create canvas
        canvas = tk.Canvas(frame_left)
        canvas.grid(row=0, column=0, sticky="NSEW")

        # set image in canvas
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image

        # RIGHT HAND SIDE ----------------------------------------------------
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        # POSITIONING frame ----------------------------------------------------
        pos_frame = ttk.Frame(frame_right, style="TFrame")
        pos_frame.grid(row=0, sticky="NSEW")
        pos_frame.columnconfigure(0, weight=1)
        pos_frame.rowconfigure(1, weight=1)

        # HEADER frame ----------------------------------------------------
        header_frame = ttk.Frame(pos_frame, style="Testing.TFrame")
        header_frame.grid(row=0, sticky="EW", padx=10)
        header_frame.columnconfigure(0, weight=1)

        # header
        header = ttk.Label(header_frame, text="Boilerplate", style="Secondary.Header.TLabel")
        header.grid()

        # CONTENT frame ----------------------------------------------------
        content_frame = ttk.Frame(pos_frame, style="Testing2.TFrame")
        content_frame.grid(row=1, sticky="EW", padx=10)
        content_frame.rowconfigure(0, weight=1)
        content_frame.columnconfigure(0, weight=1)

        lbl = ttk.Label(content_frame, text="Test Label")
        lbl.grid()

        btn_go = BLImageButtonLabel(
            parent=content_frame,
            func=self.back_button,
            path_to_file_01="assets/buttons/go_01.png",
            path_to_file_02="assets/buttons/go_02.png",
        )
        btn_go.grid(pady=10)

        # FRAME navigation ----------------------------------------------------
        nav_frame = ttk.Frame(frame_right, style="Testing.TFrame")
        nav_frame.grid(row=1, column=0, sticky="EW", padx=10)
        nav_frame.columnconfigure(0, weight=1)

        btn_img_back = BLImageButtonLabel(
            parent=nav_frame,
            func=self.go_button,
            path_to_file_01="assets/buttons/go_01.png",
            path_to_file_02="assets/buttons/go_02.png",
        )
        btn_img_back.grid(pady=10)

    def go_button(self):
        tk.messagebox.showinfo("Go button pressed", "You pressed the Go button.")

    def back_button(self):
        self.controller.show_frame(Dashboard)
