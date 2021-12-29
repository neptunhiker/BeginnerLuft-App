"""Custom labels"""

import tkinter as tk
from tkinter import ttk
from typing import Union


class BLBoldClickableSecondaryLabel(ttk.Label):

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], **kwargs) -> None:
        super(BLBoldClickableSecondaryLabel, self).__init__(parent, cursor="hand2",
                                                            style="Bold.Clickable.Secondary.TLabel",
                                                            **kwargs)
