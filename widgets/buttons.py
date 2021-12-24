"""Customized Buttons"""

from tkinter import ttk
from tkinter import PhotoImage


class BLButton(ttk.Button):

    def __init__(self, parent, **kwargs):
        super(BLButton, self).__init__(parent, cursor="hand2", **kwargs)


class ImageButton:
    """Clickable button based on a picture that can be placed on a canvas"""

    def __init__(self, parent, canvas, path_to_image_01, path_to_image_02, x_coor, y_coor, func=None, *args, **kwargs):
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

    def on_enter(self, event):
        self.parent.configure(cursor="hand2")
        self.canvas.itemconfig(self.img_on_canvas, image=self.image_02)

    def on_leave(self, event):
        self.parent.configure(cursor="")
        self.canvas.itemconfig(self.img_on_canvas, image=self.image_01)

    def on_click(self, event):
        if self.func is not None:
            self.func(*self.args, **self.kwargs)

