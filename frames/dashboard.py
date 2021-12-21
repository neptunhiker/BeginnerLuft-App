from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from frames.invoice import Invoice
from design.colors import bl_colors
from widgets.buttons import BLButton


class Dashboard(ttk.Frame):
    """Dashboard frame"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # create background image
        image = Image.open("assets/people.jpg")
        desired_width = 1800
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        # create canvas
        canvas = tk.Canvas(self)
        canvas.grid(row=0, column=0, sticky="NSEW")

        # set image in canvas
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image

        canvas.columnconfigure(0, weight=1)
        canvas.rowconfigure(0, weight=1)

        frame = ttk.Frame(canvas, style="Secondary.TFrame")
        frame.grid(ipadx=20, ipady=20)

        frame.columnconfigure((0, 1), weight=1)
        frame.rowconfigure(0, weight=1)

        image = Image.open("assets/test_button.png")
        desired_width = 200
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)

        lbl_invoices = ttk.Label(
            frame,
            image=image,
            style="Secondary.TLabel",
            cursor="hand2",
        )
        lbl_invoices.grid(row=0, column=0, padx=10)
        lbl_invoices.image = image
        lbl_invoices.bind("<Button-1>", self.show_invoice_frame)

        lbl_time_tracking = ttk.Label(frame, image=image, style="Secondary.TLabel")
        lbl_time_tracking.grid(row=0, column=1, padx=10)
        lbl_time_tracking.image = image

    def show_invoice_frame(self, event):
        self.controller.show_frame(Invoice)
