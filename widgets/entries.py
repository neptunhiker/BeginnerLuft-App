from tkinter import ttk

from design.fonts import bl_font_default


class BLEntryWidget(ttk.Entry):

    def __init__(self, parent, *args, **kwargs):
        super(BLEntryWidget, self).__init__(parent, font=bl_font_default, *args, **kwargs)