from PIL import Image, ImageTk
import sqlite3
import tkinter as tk
from tkinter import ttk

from utils import helpers
from widgets.buttons import BLButton


class PickParticipant(tk.Toplevel):

    def __init__(self, controller: tk.Tk, parent: ttk.Frame) -> None:
        super(PickParticipant, self).__init__()
        self.controller = controller
        self.parent = parent
        self.geometry("500x250")
        self.resizable(False, False)
        self.title("Teilnehmer:In")
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        # data to be passed to parent
        self.participants = {}
        self.selected_participant = None
        self.participant = tk.StringVar()
        self.error_message = tk.StringVar()

        # LEFT HAND SIDE
        frame_left = ttk.Frame(self, style="TFrame")
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.columnconfigure(0, weight=1)
        frame_left.rowconfigure(0, weight=1)

        logo = Image.open(f"{self.controller.pic_gallery_path}/logos/bl_logo.png")
        desired_width = 200
        ratio = logo.height / logo.width
        calculated_height = int(desired_width * ratio)
        logo = logo.resize((desired_width, calculated_height), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo)

        lbl = ttk.Label(frame_left, image=logo_image, style="TLabel")
        lbl.image = logo_image
        lbl.grid(padx=20)

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1)

        # header
        lbl_header = ttk.Label(frame_right, text="Teilnehmerauswahl", style="Secondary.Header.TLabel")
        lbl_header.grid(pady=(0, 30))

        # dropdown menu
        self.cmb_participants = ttk.Combobox(frame_right, textvariable=self.participant)
        try:
            for participant in self.controller.db.get_participants():
                self.participants[str(participant.data_base_id)] = participant
        except sqlite3.OperationalError:
            self.destroy()
            helpers.DatabaseErrorWindow()
            return

        sorted_values = sorted(self.participants.values(), key=lambda x: x.first_name)
        self.cmb_participants["values"] = [f"{participant.first_name} {participant.last_name} - (ID: " 
                                           f"{participant.data_base_id})" for participant
                                           in sorted_values]
        self.cmb_participants["state"] = "readonly"
        self.cmb_participants.bind("<<ComboboxSelected>>", self.handle_user_selection)
        self.cmb_participants.grid(padx=20)

        # Error message
        self.lbl_error = ttk.Label(frame_right, textvariable=self.error_message, style="Secondary.Error.TLabel")
        self.lbl_error.grid(pady=(20, 5))

        # Go button
        btn = BLButton(frame_right, style="Secondary.TButton", text="Teilnehmer:In ausw??hlen",
                         command=self.send_data)
        btn.grid()

    def handle_user_selection(self, event: tk.Event) -> None:
        """Get data from frame when user changes a selection"""

        # get ID
        selected_participant = self.cmb_participants.get()
        id_pos = selected_participant.find("ID: ")
        id = selected_participant[id_pos + 4:-1]

        # Assign selected participant
        self.selected_participant = self.participants[id]

        self.error_message.set("")

    def send_data(self) -> None:
        """Send the data to the parent frame"""

        if self.selected_participant is None:
            self.error_message.set("Bitte Teilnehmer:In ausw??hlen")
            return

        self.parent.participant_title.set(self.selected_participant.title)
        self.parent.participant_first_name.set(self.selected_participant.first_name)
        self.parent.participant_last_name.set(self.selected_participant.last_name)
        self.parent.participant_jc_id.set(self.selected_participant.id_with_jc)

        self.destroy()


class PickJobcenter(tk.Toplevel):

    def __init__(self, controller: tk.Tk, parent: ttk.Frame) -> None:
        super(PickJobcenter, self).__init__()
        self.controller = controller
        self.parent = parent
        self.geometry("500x250")
        self.resizable(False, False)
        self.title("Jobcenter")
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        # data to be passed to parent
        self.jobcenters = {}
        self.selected_jc = None
        self.jobcenter = tk.StringVar()
        self.error_message = tk.StringVar()

        # LEFT HAND SIDE
        frame_left = ttk.Frame(self, style="TFrame")
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.columnconfigure(0, weight=1)
        frame_left.rowconfigure(0, weight=1)

        logo = Image.open(f"{self.controller.pic_gallery_path}/logos/bl_logo.png")
        desired_width = 200
        ratio = logo.height / logo.width
        calculated_height = int(desired_width * ratio)
        logo = logo.resize((desired_width, calculated_height), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo)

        lbl = ttk.Label(frame_left, image=logo_image, style="TLabel")
        lbl.image = logo_image
        lbl.grid(padx=20)

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1)

        # header
        lbl_header = ttk.Label(frame_right, text="Jobcenterauswahl", style="Secondary.Header.TLabel")
        lbl_header.grid(pady=(0, 30))

        # dropdown menu
        self.cmb_jobcenter = ttk.Combobox(frame_right, textvariable=self.jobcenter)
        try:
            for jc in self.controller.db.get_jobcenters():
                self.jobcenters[str(jc.data_base_id)] = jc
        except sqlite3.OperationalError:
            self.destroy()
            helpers.DatabaseErrorWindow()
            return

        sorted_values = sorted(self.jobcenters.values(), key=lambda x: x.name)
        self.cmb_jobcenter["values"] = [f"{jc.name} - (ID: " 
                                           f"{jc.data_base_id})" for jc
                                        in sorted_values]
        self.cmb_jobcenter["state"] = "readonly"
        self.cmb_jobcenter.bind("<<ComboboxSelected>>", self.handle_user_selection)
        self.cmb_jobcenter.grid(padx=20)

        # Error message
        self.lbl_error = ttk.Label(frame_right, textvariable=self.error_message, style="Secondary.Error.TLabel")
        self.lbl_error.grid(pady=(20, 5))

        # Go button
        btn = BLButton(frame_right, style="Secondary.TButton", text="Jobcenter ausw??hlen",
                         command=self.send_data)
        btn.grid()

    def handle_user_selection(self, event: tk.Event) -> None:
        """Get data from frame when user changes a selection"""

        # get ID
        selected_jobcenter = self.cmb_jobcenter.get()
        id_pos = selected_jobcenter.find("ID: ")
        id = selected_jobcenter[id_pos + 4:-1]

        # Assign selected participant
        self.selected_jc = self.jobcenters[id]

        self.error_message.set("")

    def send_data(self) -> None:
        """Send the data to the parent frame"""

        if self.selected_jc is None:
            self.error_message.set("Bitte Jobcenter ausw??hlen")
            return

        self.parent.jc_name.set(self.selected_jc.name)
        self.parent.jc_street.set(self.selected_jc.street)
        self.parent.jc_street_nr.set(self.selected_jc.street_nr)
        self.parent.jc_zip_and_city.set(f"{self.selected_jc.zip_code} {self.selected_jc.city}")

        self.destroy()


class PickTraining(tk.Toplevel):
    """A data picker window for picking a training (Ma??nahme) from a data base"""

    def __init__(self, controller: tk.Tk, parent: ttk.Frame) -> None:
        super(PickTraining, self).__init__()
        self.controller = controller
        self.parent = parent
        self.geometry("500x250")
        self.resizable(False, False)
        self.title("Ma??nahme")
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        # data to be passed to parent
        self.trainings = {}
        self.selected_training = None
        self.var_training = tk.StringVar()
        self.error_message = tk.StringVar()

        # LEFT HAND SIDE
        frame_left = ttk.Frame(self, style="TFrame")
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.columnconfigure(0, weight=1)
        frame_left.rowconfigure(0, weight=1)

        logo = Image.open(f"{self.controller.pic_gallery_path}/logos/bl_logo.png")
        desired_width = 200
        ratio = logo.height / logo.width
        calculated_height = int(desired_width * ratio)
        logo = logo.resize((desired_width, calculated_height), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo)

        lbl = ttk.Label(frame_left, image=logo_image, style="TLabel")
        lbl.image = logo_image
        lbl.grid(padx=20)

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1)

        # header
        lbl_header = ttk.Label(frame_right, text="Auswahl Ma??nahme", style="Secondary.Header.TLabel")
        lbl_header.grid(pady=(0, 30))

        # dropdown menu
        self.cmb_training = ttk.Combobox(frame_right, textvariable=self.var_training)
        try:
            for training in self.controller.db.get_trainings():
                self.trainings[str(training.data_base_id)] = training
        except sqlite3.OperationalError:
            self.destroy()
            helpers.DatabaseErrorWindow()
            return

        self.cmb_training["values"] = [f"{training.name} - (ID: " 
                                           f"{training.data_base_id})" for training
                                       in self.trainings.values()]
        self.cmb_training["state"] = "readonly"
        self.cmb_training.bind("<<ComboboxSelected>>", self.handle_user_selection)
        self.cmb_training.grid(padx=20)

        # Error message
        self.lbl_error = ttk.Label(frame_right, textvariable=self.error_message, style="Secondary.Error.TLabel")
        self.lbl_error.grid(pady=(20, 5))

        # Go button
        btn = BLButton(frame_right, style="Secondary.TButton", text="Ma??nahme ausw??hlen",
                         command=self.send_data)
        btn.grid()

    def handle_user_selection(self, event: tk.Event) -> None:
        """Get data from frame when user changes a selection"""

        # get ID
        selected_training = self.cmb_training.get()
        id_pos = selected_training.find("ID: ")
        id = selected_training[id_pos + 4:-1]

        # Assign selected participant
        self.selected_training = self.trainings[id]

        self.error_message.set("")

    def send_data(self) -> None:
        """Send the data to the parent frame"""

        if self.selected_training is None:
            self.error_message.set("Bitte Ma??nahme ausw??hlen")
            return

        self.parent.training_name.set(self.selected_training.name)
        self.parent.training_cost_per_lesson.set(self.selected_training.cost_per_training_lesson)
        self.parent.training_id.set(self.selected_training.data_base_id)

        self.destroy()
