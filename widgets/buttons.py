"""Customized Buttons"""

from tkinter import ttk


class BLButton(ttk.Button):

    def __init__(self, parent, **kwargs):
        super(BLButton, self).__init__(parent, cursor="hand2", **kwargs)
