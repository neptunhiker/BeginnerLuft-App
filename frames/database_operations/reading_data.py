import tkinter as tk
from tkinter import ttk
from typing import Union

from frames import dashboard
from widgets.background import create_background_image
from widgets.buttons import BLImageButtonLabel

class ReadParticipant(ttk.Frame):
    """A frame that allows to add a participant to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # create image on canvas
        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self, desired_width=1800)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        # CONTAINER ################################################
        container_frame = ttk.Frame(self.canvas, style="Testing.TFrame")
        container_frame.grid(ipadx=20, ipady=20)
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        # HEADER FRAME ################################################
        header_frame = ttk.Frame(container_frame)
        header_frame.grid()
        lbl_header = ttk.Label(header_frame, text="Teilnehmer:Innen", style="Secondary.Header.TLabel")
        lbl_header.grid()

        # DATA FRAME ################################################
        data_frame = ttk.Frame(container_frame)
        data_frame.grid()

        # NAV FRAME ################################################
        nav_frame = ttk.Frame(container_frame)
        nav_frame.grid()

        btn = BLImageButtonLabel(parent=nav_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseCreateDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid()

    def read_from_database(self) -> None:
        """Get data from database"""


        participants = self.controller.db.get_participants()

        for participant in participants:
