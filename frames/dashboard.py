from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from design.fonts import bl_font_title, bl_font_subtitle
from frames.database_operations.creating_data import AddParticipant, AddCoach, AddJobcenter
from frames.invoice import Invoice
from frames.time_tracking import TimeTrackingDataSelection
from widgets.background import create_background_image
from widgets.buttons import BLImageButtonCanvas


class Dashboard(ttk.Frame):
    """A frame that displays different little programs available to the user"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        # create background image
        image = Image.open(f"{self.controller.pic_gallery_path}/backgrounds/people.jpg")
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

    def create_header(self) -> None:
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle, text="Dashboard")

    def create_buttons(self) -> None:
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["databaseoperations", "dashboard_invoice",
                              "timetracking"]  # without exetension such as _01, _02
        next_frames = [DatabaseOperationsDashboard, Invoice, TimeTrackingDataSelection]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"{self.controller.pic_gallery_path}/buttons/{file_name}_01.png",
                                path_to_image_02=f"{self.controller.pic_gallery_path}/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift


class DatabaseOperationsDashboard(ttk.Frame):
    """A frame that displays options for executing CRUD operations on a database"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self)

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self) -> None:
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle,
                                text="Datenbankoperationen")

    def create_buttons(self) -> None:
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["data_create", "data_read", "data_update", "data_delete", "back"]  # without exetension such as _01, _02
        next_frames = [DatabaseCreateDashboard, DatabaseReadDashboard, DatabaseUpdateDashboard, DatabaseDeleteDashboard,
                       Dashboard]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"{self.controller.pic_gallery_path}/buttons/{file_name}_01.png",
                                path_to_image_02=f"{self.controller.pic_gallery_path}/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift


class DatabaseCreateDashboard(ttk.Frame):
    """A frame that displays Create-options on a database"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self)

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self) -> None:
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle,
                                text="Daten hinzufügen")

    def create_buttons(self) -> None:
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["participants", "coaches", "jobcenter",
                              "back"]  # without exetension such as _01, _02
        next_frames = [AddParticipant, AddCoach, AddJobcenter, DatabaseOperationsDashboard]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"{self.controller.pic_gallery_path}/buttons/{file_name}_01.png",
                                path_to_image_02=f"{self.controller.pic_gallery_path}/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift


class DatabaseReadDashboard(ttk.Frame):
    """A frame that displays Read-options on a database"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self)

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self) -> None:
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle,
                                text="Daten einsehen")

    def create_buttons(self) -> None:
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["participants", "coaches", "jobcenter", "trainings",
                              "back"]  # without exetension such as _01, _02
        next_frames = [DatabaseReadDashboard, DatabaseReadDashboard, DatabaseReadDashboard, DatabaseReadDashboard,
                       DatabaseOperationsDashboard]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"{self.controller.pic_gallery_path}/buttons/{file_name}_01.png",
                                path_to_image_02=f"{self.controller.pic_gallery_path}/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift


class DatabaseUpdateDashboard(ttk.Frame):
    """A frame that displays Update-options on a database"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self)

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self) -> None:
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle,
                                text="Daten aktualisieren")

    def create_buttons(self) -> None:
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["participants", "coaches", "jobcenter", "trainings",
                              "back"]  # without exetension such as _01, _02
        next_frames = [DatabaseUpdateDashboard, DatabaseUpdateDashboard, DatabaseUpdateDashboard,
                       DatabaseUpdateDashboard,
                       DatabaseOperationsDashboard]

        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"{self.controller.pic_gallery_path}/buttons/{file_name}_01.png",
                                path_to_image_02=f"{self.controller.pic_gallery_path}/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift


class DatabaseDeleteDashboard(ttk.Frame):
    """A frame that displays Delte-options on a database"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.screen_midpoint = self.winfo_screenwidth() / 2

        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self)

        # create header and buttons
        self.create_header()
        self.create_buttons()

    def create_header(self) -> None:
        """Create a header for the canvas"""

        self.canvas.create_text(self.screen_midpoint, 100, fill="white", font=bl_font_title, text="BeginnerLuft")
        self.canvas.create_text(self.screen_midpoint, 170, fill="white", font=bl_font_subtitle,
                                text="Daten löschen")

    def create_buttons(self) -> None:
        """Create clickable buttons that lead to other frames"""

        picture_file_names = ["participants", "coaches", "jobcenter", "trainings",
                              "back"]  # without exetension such as _01, _02
        next_frames = [DatabaseDeleteDashboard, DatabaseDeleteDashboard, DatabaseDeleteDashboard,
                       DatabaseDeleteDashboard,
                       DatabaseOperationsDashboard]


        x_start_pos = self.screen_midpoint
        y_start_pos = 300
        button_height = 75  # needs to be adjusted if button size changes
        vert_space = 25
        y_shift = button_height + vert_space

        y_pos = y_start_pos
        for file_name, next_frame in zip(picture_file_names, next_frames):
            BLImageButtonCanvas(parent=self,
                                canvas=self.canvas,
                                path_to_image_01=f"{self.controller.pic_gallery_path}/buttons/{file_name}_01.png",
                                path_to_image_02=f"{self.controller.pic_gallery_path}/buttons/{file_name}_02.png",
                                x_coor=x_start_pos,
                                y_coor=y_pos,
                                func=self.controller.show_frame,
                                container=next_frame
                                )
            y_pos += y_shift
