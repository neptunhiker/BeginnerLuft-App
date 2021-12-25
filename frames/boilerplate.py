import datetime
from tkinter import ttk
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

from design.colors import bl_colors
from frames.dashboard import Dashboard
from reports.invoice import PDFInvoice
from tools import helpers
from widgets.buttons import BLButton, BLImageButtonLabel


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

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid()

        # header frame
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=30)
        header_frame.columnconfigure(0, weight=1)


        # CONTENT frame
        content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        content_frame.grid(padx=20)

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # # go button
        # back_image = Image.open("assets/buttons/back_01.png")
        # button_photo = ImageTk.PhotoImage(back_image)
        # #
        # # button_photo = PhotoImage("assets/buttons/back_01.png")
        #
        # btn = ttk.Label(buttons_frame, image=button_photo, style="Secondary.TLabel")
        # btn.image = button_photo
        # btn.grid()

        btn_img_back = BLImageButtonLabel(
            parent=buttons_frame,
            func=self.back_button,
            path_to_file_01="assets/buttons/back_01.png",
            path_to_file_02="assets/buttons/back_02.png",
        )
        btn_img_back.grid()

        # back button
        btn_back = BLButton(buttons_frame, text="<< zurück", command=self.back_button)
        btn_back.grid(pady=(20, 10))

    def go_button(self):
        print("Testing go button")

    def back_button(self):
        self.controller.show_frame(Dashboard)