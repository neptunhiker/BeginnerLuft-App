"""Customized Buttons"""
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from typing import Callable, Union

from design.colors import bl_colors


class BLButton(ttk.Button):

    def __init__(self, parent: Union[ttk.Frame, tk.Tk], **kwargs) -> None:
        super(BLButton, self).__init__(parent, cursor="hand2", **kwargs)


class BLImageButtonLabel(tk.Label):

    def __init__(self, parent: Union[ttk.Frame, tk.Tk], func: Callable, path_to_file_01: str,
                 path_to_file_02: str, *args, **kwargs) -> None:

        self.func = func
        self.image_01 = Image.open(path_to_file_01)
        self.image_02 = Image.open(path_to_file_02)

        self.button_photo_01 = ImageTk.PhotoImage(self.image_01)
        self.button_photo_02 = ImageTk.PhotoImage(self.image_02)

        self.button_photo_01 = self.button_photo_01
        self.button_photo_02 = self.button_photo_02

        super(BLImageButtonLabel, self).__init__(parent, *args, image=self.button_photo_01, cursor="hand2",
                                                 background=bl_colors["bg secondary"], **kwargs)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_leave(self, event: tk.Event) -> None:
        self.configure(image=self.button_photo_01)

    def on_enter(self, event: tk.Event) -> None:
        self.configure(image=self.button_photo_02)

    def on_click(self, event: tk.Event) -> None:
        self.func()


class BLImageButtonCanvas:
    """Clickable button based on a picture that can be placed on a canvas"""

    def __init__(self, parent: Union[ttk.Frame, tk.Tk], canvas: tk.Canvas, path_to_image_01: str,
                 path_to_image_02: str, x_coor: int, y_coor: int, func: Callable = None, *args, **kwargs) -> None:
        self.parent = parent
        self.canvas = canvas
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.image_01 = PhotoImage(file=path_to_image_01)
        self.image_02 = PhotoImage(file=path_to_image_02)

        self.img_on_canvas = self.canvas.create_image(
            x_coor,
            y_coor,
            image=self.image_01,
            anchor="n",
        )

        self.canvas.tag_bind(self.img_on_canvas, '<ButtonPress-1>', self.on_click)
        self.canvas.tag_bind(self.img_on_canvas, '<Enter>', self.on_enter)
        self.canvas.tag_bind(self.img_on_canvas, '<Leave>', self.on_leave)

    def on_enter(self, event: tk.Event) -> None:
        self.parent.configure(cursor="hand2")
        self.canvas.itemconfig(self.img_on_canvas, image=self.image_02)

    def on_leave(self, event: tk.Event) -> None:
        self.parent.configure(cursor="")
        self.canvas.itemconfig(self.img_on_canvas, image=self.image_01)

    def on_click(self, event: tk.Event) -> None:
        if self.func is not None:
            self.func(*self.args, **self.kwargs)

