from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk


def create_background_image(path_of_image: str, frame: ttk.Frame, desired_width: int = 1800) -> tk.Canvas:
    """Create and place a background image on a canvas"""

    # create background image
    image = Image.open(path_of_image)
    ratio = image.height / image.width
    calculated_height = int(desired_width * ratio)
    image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
    bg_image = ImageTk.PhotoImage(image)

    # create canvas
    canvas = tk.Canvas(frame)
    canvas.grid(row=0, column=0, sticky="NSEW")

    # set image in canvas
    canvas.create_image(0, 0, image=bg_image, anchor="nw")
    canvas.image = bg_image

    return canvas
