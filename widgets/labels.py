"""Custom labels"""

from tkinter import ttk


class BLBoldClickableSecondaryLabel(ttk.Label):

    def __init__(self, parent, **kwargs):
        super(BLBoldClickableSecondaryLabel, self).__init__(parent, cursor="hand2",
                                                            style="Bold.Clickable.Secondary.TLabel",
                                                            **kwargs)
