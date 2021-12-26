from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from design.fonts import bl_font_title, bl_font_subtitle
from frames.database_operations.adding_data import AddParticipant, AddCoach, AddJobcenter
from frames.invoice import Invoice
from frames.time_tracking import TimeTracking
from widgets.buttons import BLImageButtonCanvas


class Dashboard(ttk.Frame):
    """A frame that displays different little programs available to the user"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        # create background image
        image = Image.open("assets/people.jpg")
        desired_width = 1800
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        # create canvas
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        # set background image in canvas
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self):
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle, text="Dashboard")

    def create_buttons(self):
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["databaseoperations", "dashboard_invoice", "timetracking"]  # without exetension such as _01, _02
        next_frames = [DatabaseOperationsDashboard, Invoice, TimeTracking]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"assets/buttons/{file_name}_01.png",
                                path_to_image_02=f"assets/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift


class DatabaseOperationsDashboard(ttk.Frame):
    """A frame that displays different little programs available to the user for interacting with the database"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        # create background image
        image = Image.open("assets/people.jpg")
        desired_width = 1800
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        # create canvas
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        # set background image in canvas
        self.canvas.create_image(0, 0, image=bg_image, anchor="nw")
        self.canvas.image = bg_image

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self):
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle, text="Datenbankoperationen")

    def create_buttons(self):
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["add_participant", "add_coach", "add_jobcenter", "back"]  # without exetension such as _01, _02
        next_frames = [AddParticipant, AddCoach, AddJobcenter, Dashboard]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"assets/buttons/{file_name}_01.png",
                                path_to_image_02=f"assets/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift