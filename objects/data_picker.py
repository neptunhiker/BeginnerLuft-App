from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

from widgets.buttons import BLButton


class PickParticipant(tk.Toplevel):

    def __init__(self, controller, parent):
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

        logo = Image.open("assets/bl_logo.png")
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
        for participant in self.controller.db.get_participants():
            self.participants[str(participant.data_base_id)] = participant

        self.cmb_participants["values"] = [f"{participant.first_name} {participant.last_name} - (ID: " 
                                           f"{participant.data_base_id})" for participant
                                           in self.participants.values()]
        self.cmb_participants["state"] = "readonly"
        self.cmb_participants.bind("<<ComboboxSelected>>", self.handle_user_selection)
        self.cmb_participants.grid(padx=20)

        # Error message
        self.lbl_error = ttk.Label(frame_right, textvariable=self.error_message, style="Secondary.Error.TLabel")
        self.lbl_error.grid(pady=(20, 5))

        # Go button
        btn = BLButton(frame_right, style="Secondary.TButton", text="Teilnehmer:In auswählen",
                         command=self.send_data)
        btn.grid()

    def handle_user_selection(self, event):
        """Get data from frame when user changes a selection"""

        # get ID
        selected_participant = self.cmb_participants.get()
        id_pos = selected_participant.find("ID: ")
        id = selected_participant[id_pos + 4:-1]

        # Assign selected participant
        self.selected_participant = self.participants[id]

        self.error_message.set("")

    def send_data(self):
        """Send the data to the parent frame"""

        if self.selected_participant is None:
            self.error_message.set("Bitte Teilnehmer:In auswählen")
            return

        self.parent.participant_title.set(self.selected_participant.title)
        self.parent.participant_first_name.set(self.selected_participant.first_name)
        self.parent.participant_last_name.set(self.selected_participant.last_name)
        self.parent.participant_jc_id.set(self.selected_participant.id_with_jc)

        self.destroy()
