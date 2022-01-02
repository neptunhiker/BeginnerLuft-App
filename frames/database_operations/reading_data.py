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
        self.participants = {}
        self.selected_participant = None

        # create image on canvas
        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self, desired_width=1800)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        # CONTAINER ################################################
        container_frame = ttk.Frame(self.canvas, style="Secondary.TFrame")
        container_frame.grid(ipadx=20, ipady=20)
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        # HEADER FRAME ################################################
        header_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        header_frame.grid()
        lbl_header = ttk.Label(header_frame, text="Teilnehmer:Innen", style="Secondary.Header.TLabel")
        lbl_header.grid()

        # SELECTION FRAME ###########################################
        # participant selector via dropdown
        selection_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        selection_frame.grid()

        ttk.Label(selection_frame, text="Auswahl", style="Bold.Secondary.TLabel").grid()
        self.cmb_participants = ttk.Combobox(selection_frame, textvariable=self.selected_participant)
        self.cmb_participants.bind("<<ComboboxSelected>>", self.handle_user_selection)
        self.cmb_participants["state"] = "readonly"
        self.cmb_participants.grid()

        # DATA FRAME ################################################
        self.data_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        self.data_frame.grid(pady=20, sticky="EW")
        self.data_frame.columnconfigure((0, 1), weight=1)

        # participant data
        self.participant_title = tk.StringVar()
        self.participant_first_name = tk.StringVar()
        self.participant_last_name = tk.StringVar()
        self.participant_street_and_nr = tk.StringVar()
        self.participant_zip_code= tk.StringVar()
        self.participant_city = tk.StringVar()
        self.participant_id_with_jc = tk.StringVar()

        self.variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                          self.participant_street_and_nr, self.participant_zip_code, self.participant_city,
                          self.participant_id_with_jc]
        lbl_headers = ["Anrede", "Vorname", "Nachname", "Straße und Nr", "PLZ", "Stadt", "Kundennummer"]
        for i, item in enumerate(zip(lbl_headers, self.variables)):
            lbl_header = item[0]
            variable = item[1]
            ttk.Label(self.data_frame, text=lbl_header,
                      style="Bold.Secondary.TLabel").grid(row=i, column=0, sticky="E")
            ttk.Label(self.data_frame, textvariable=variable,
                      style="Secondary.TLabel").grid(row=i, column=1, sticky="W", padx=(10, 0))

        # NAV FRAME ################################################
        nav_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        nav_frame.grid(pady=30)

        btn = BLImageButtonLabel(parent=nav_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseCreateDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid()

    def refresh(self) -> None:
        """Refresh the page"""
        self.get_participants()
        self.fill_in_dropdown_options()
        self.update_data()

    def get_participants(self) -> None:
        """Get a list of participants from the database"""
        list_of_participants = self.controller.db.get_participants()
        for participant in list_of_participants:
            self.participants[str(participant.data_base_id)] = participant

    def fill_in_dropdown_options(self) -> None:
        """Fills the list of available options in the dropdown menu"""
        sorted_values = sorted(self.participants.values(), key=lambda x: x.first_name)
        self.cmb_participants["values"] = [f"{participant.first_name} {participant.last_name} - (ID: " 
                                           f"{participant.data_base_id})" for participant
                                           in sorted_values]

    def update_data(self) -> None:
        """Updates the participant data that is displayed"""

        if self.selected_participant is None:
            for var in self.variables:
                var.set("")
                return

        self.participant_title.set(self.selected_participant.title)
        self.participant_first_name.set(self.selected_participant.first_name)
        self.participant_last_name.set(self.selected_participant.last_name)
        self.participant_street_and_nr.set(self.selected_participant.street_and_nr)
        self.participant_zip_code.set(self.selected_participant.zip_code)
        self.participant_city.set(self.selected_participant.city)
        self.participant_id_with_jc.set(self.selected_participant.id_with_jc)

    def handle_user_selection(self, event) -> None:
        """Run whenever user changes the selection in the dropdown menu"""
        print("test")

        # get ID
        selected_participant = self.cmb_participants.get()
        id_pos = selected_participant.find("ID: ")
        id = selected_participant[id_pos + 4:-1]

        # Assign selected participant
        self.selected_participant = self.participants[id]

        # update data
        self.update_data()