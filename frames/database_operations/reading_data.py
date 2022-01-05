import tkinter as tk
from tkinter import ttk
from typing import Union

from frames import dashboard
from widgets.background import create_background_image
from widgets.buttons import BLImageButtonLabel


class ReadParticipants(ttk.Frame):
    """A frame that allows to read data for participants from the database"""

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
        container_frame.grid()
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        pad_x = 50
        pad_y = 50

        # HEADER FRAME ################################################
        header_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        header_frame.grid()
        lbl_header = ttk.Label(header_frame, text="Teilnehmer:Innen", style="Secondary.Header.TLabel")
        lbl_header.grid(padx=pad_x, pady=pad_y)

        # SELECTION FRAME ###########################################
        # participant selector via dropdown
        selection_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        selection_frame.grid(padx=pad_x)
        selection_frame.columnconfigure(1, weight=1)

        ttk.Label(selection_frame, text="Auswahl", style="Bold.Secondary.TLabel").grid()
        self.cmb_participants = ttk.Combobox(selection_frame, textvariable=self.selected_participant)
        self.cmb_participants.bind("<<ComboboxSelected>>", lambda event: self.handle_user_selection())
        self.cmb_participants["state"] = "readonly"
        self.cmb_participants.grid(row=0, column=1)

        btn_previous = BLImageButtonLabel(parent=selection_frame,
                                          func=lambda: self.loop_through(direction="previous"),
                                          path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/previous_01.png",
                                          path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/previous_02.png")
        btn_previous.grid(row=0, column=0, padx=(0, 10))

        btn_next = BLImageButtonLabel(parent=selection_frame,
                                      func=lambda: self.loop_through(direction="next"),
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/next_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/next_02.png")
        btn_next.grid(row=0, column=2, padx=(10, 0))

        # DATA FRAME ################################################
        self.data_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        self.data_frame.grid(padx=pad_x, pady=20, sticky="W")
        # self.data_frame.columnconfigure((1), weight=1)

        # participant data
        self.participant_title = tk.StringVar()
        self.participant_first_name = tk.StringVar()
        self.participant_last_name = tk.StringVar()
        self.participant_street_and_nr = tk.StringVar()
        self.participant_zip_code = tk.StringVar()
        self.participant_city = tk.StringVar()
        self.participant_email = tk.StringVar()
        self.participant_cell_phone_nr = tk.StringVar()
        self.participant_residency_status = tk.StringVar()
        self.participant_country_of_origin = tk.StringVar()
        self.participant_driving_license = tk.StringVar()
        self.participant_mother_tongue = tk.StringVar()
        self.participant_school_degree_germany = tk.StringVar()
        self.participant_id_with_jc = tk.StringVar()

        self.variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                          self.participant_street_and_nr, self.participant_zip_code, self.participant_city,
                          self.participant_email, self.participant_cell_phone_nr,
                          self.participant_country_of_origin, self.participant_driving_license,
                          self.participant_id_with_jc, self.participant_residency_status, self.participant_mother_tongue,
                          self.participant_school_degree_germany]
        lbl_headers = ["Anrede", "Vorname", "Nachname", "Straße und Nr", "PLZ", "Stadt", "E-Mail", "Handynummer",
                       "Herkunftsland", "Führerschein", "Kundennummer", "Aufenthaltsstaus", "Muttersprache",
                       "Schulabschluss in Deutschland"]
        for i, item in enumerate(zip(lbl_headers, self.variables)):
            lbl_header = item[0]
            variable = item[1]
            ttk.Label(self.data_frame, text=lbl_header,
                      style="Bold.Secondary.TLabel").grid(row=i, column=0, sticky="W", padx=(40, 10))
            ttk.Label(self.data_frame, textvariable=variable,
                      style="Secondary.TLabel").grid(row=i, column=1, sticky="W")

        # NAV FRAME ################################################
        nav_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        nav_frame.grid(padx=pad_x, pady=(30, pad_y))

        btn = BLImageButtonLabel(parent=nav_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseReadDashboard),
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
        self.participant_email.set(self.selected_participant.email)
        self.participant_cell_phone_nr.set(self.selected_participant.cell_phone_nr)
        self.participant_residency_status.set(self.selected_participant.residency_status)
        self.participant_country_of_origin.set(self.selected_participant.country_of_origin)
        self.participant_driving_license.set(self.selected_participant.driving_license)
        self.participant_id_with_jc.set(self.selected_participant.id_with_jc)
        self.participant_mother_tongue.set(self.selected_participant.mother_tongue)
        self.participant_school_degree_germany.set(self.selected_participant.school_degree_germany)

    def loop_through(self, direction: str = "next") -> None:
        """Pick the next participant from the dropdown box"""
        current = self.cmb_participants.current()
        length = len(self.cmb_participants["values"])
        if direction == "next":
            next_participant = (current + 1) % length
        else:
            next_participant = (current - 1) % length
        self.cmb_participants.current(next_participant)

        # update data
        self.handle_user_selection()

    def handle_user_selection(self) -> None:
        """Run whenever user changes the selection in the dropdown menu"""

        # get ID
        selected_participant = self.cmb_participants.get()
        id_pos = selected_participant.find("ID: ")
        the_id = selected_participant[id_pos + 4:-1]

        # Assign selected participant
        self.selected_participant = self.participants[the_id]

        # update data
        self.update_data()

        # append participant to clipboard
        self.append_to_clipboard()

    def append_to_clipboard(self) -> None:
        """Append the selected participant to clipboard"""

        self.controller.clipboard_clear()
        self.controller.clipboard_append(self.selected_participant)
        self.controller.update()  # now it stays on the clipboard after the window is closed


class ReadCoaches(ttk.Frame):
    """A frame that allows to read data for coches from to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.coaches = {}
        self.selected_coach = None

        # create image on canvas
        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self, desired_width=1800)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        # CONTAINER ################################################
        container_frame = ttk.Frame(self.canvas, style="Secondary.TFrame")
        container_frame.grid()
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        pad_x = 50
        pad_y = 50

        # HEADER FRAME ################################################
        header_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        header_frame.grid()
        lbl_header = ttk.Label(header_frame, text="Coaches", style="Secondary.Header.TLabel")
        lbl_header.grid(padx=pad_x, pady=pad_y)

        # SELECTION FRAME ###########################################
        # coach selector via dropdown
        selection_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        selection_frame.grid(padx=pad_x)
        selection_frame.columnconfigure(1, weight=1)

        ttk.Label(selection_frame, text="Auswahl", style="Bold.Secondary.TLabel").grid()
        self.cmb_coaches = ttk.Combobox(selection_frame, textvariable=self.selected_coach)
        self.cmb_coaches.bind("<<ComboboxSelected>>", lambda event: self.handle_user_selection())
        self.cmb_coaches["state"] = "readonly"
        self.cmb_coaches.grid(row=0, column=1)

        btn_previous = BLImageButtonLabel(parent=selection_frame,
                                          func=lambda: self.loop_through(direction="previous"),
                                          path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/previous_01.png",
                                          path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/previous_02.png")
        btn_previous.grid(row=0, column=0, padx=(0, 10))

        btn_next = BLImageButtonLabel(parent=selection_frame,
                                      func=lambda: self.loop_through(direction="next"),
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/next_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/next_02.png")
        btn_next.grid(row=0, column=2, padx=(10, 0))

        # DATA FRAME ################################################
        self.data_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        self.data_frame.grid(padx=pad_x, pady=20, sticky="W")

        # coaches data
        self.coach_title = tk.StringVar()
        self.coach_first_name = tk.StringVar()
        self.coach_last_name = tk.StringVar()

        self.variables = [self.coach_title, self.coach_first_name, self.coach_last_name]
        lbl_headers = ["Anrede", "Vorname", "Nachname"]
        for i, item in enumerate(zip(lbl_headers, self.variables)):
            lbl_header = item[0]
            variable = item[1]
            ttk.Label(self.data_frame, text=lbl_header,
                      style="Bold.Secondary.TLabel").grid(row=i, column=0, sticky="W", padx=(80, 10))
            ttk.Label(self.data_frame, textvariable=variable,
                      style="Secondary.TLabel").grid(row=i, column=1, sticky="W")

        # NAV FRAME ################################################
        nav_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        nav_frame.grid(padx=pad_x, pady=(30, pad_y))

        btn = BLImageButtonLabel(parent=nav_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseReadDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid()

    def refresh(self) -> None:
        """Refresh the page"""
        self.get_coaches()
        self.fill_in_dropdown_options()
        self.update_data()

    def get_coaches(self) -> None:
        """Get a list of coaches from the database"""
        list_of_coaches = self.controller.db.get_coaches()
        print(list_of_coaches)
        for coach in list_of_coaches:
            self.coaches[str(coach.data_base_id)] = coach

    def fill_in_dropdown_options(self) -> None:
        """Fills the list of available options in the dropdown menu"""
        sorted_values = sorted(self.coaches.values(), key=lambda x: x.first_name)
        self.cmb_coaches["values"] = [f"{coach.first_name} {coach.last_name} - (ID: "
                                           f"{coach.data_base_id})" for coach
                                      in sorted_values]

    def update_data(self) -> None:
        """Updates the coaches data that is displayed"""

        if self.selected_coach is None:
            for var in self.variables:
                var.set("")
                return

        self.coach_title.set(self.selected_coach.title)
        self.coach_first_name.set(self.selected_coach.first_name)
        self.coach_last_name.set(self.selected_coach.last_name)

    def loop_through(self, direction: str = "next") -> None:
        """Pick the next coach from the dropdown box"""
        current = self.cmb_coaches.current()
        length = len(self.cmb_coaches["values"])
        if direction == "next":
            next_coach = (current + 1) % length
        else:
            next_coach = (current - 1) % length
        self.cmb_coaches.current(next_coach)

        # update data
        self.handle_user_selection()

    def handle_user_selection(self) -> None:
        """Run whenever user changes the selection in the dropdown menu"""

        # get ID
        selected_coach = self.cmb_coaches.get()
        id_pos = selected_coach.find("ID: ")
        the_id = selected_coach[id_pos + 4:-1]

        # Assign selected coach
        self.selected_coach = self.coaches[the_id]

        # update data
        self.update_data()

        # append coach to clipboard
        self.append_to_clipboard()

    def append_to_clipboard(self) -> None:
        """Append the selected coach to clipboard"""

        self.controller.clipboard_clear()
        self.controller.clipboard_append(self.selected_coach)
        self.controller.update()  # now it stays on the clipboard after the window is closed


class ReadJobcenter(ttk.Frame):
    """A frame that allows to read data for jobcenter from to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.jobcenter = {}
        self.selected_jobcenter = None

        # create image on canvas
        self.canvas = create_background_image(
            path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/people.jpg",
            frame=self, desired_width=1800)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)

        # CONTAINER ################################################
        container_frame = ttk.Frame(self.canvas, style="Secondary.TFrame")
        container_frame.grid()
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        pad_x = 50
        pad_y = 50

        # HEADER FRAME ################################################
        header_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        header_frame.grid()
        lbl_header = ttk.Label(header_frame, text="Jobcenter", style="Secondary.Header.TLabel")
        lbl_header.grid(padx=pad_x, pady=pad_y)

        # SELECTION FRAME ###########################################
        # coach selector via dropdown
        selection_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        selection_frame.grid(padx=pad_x)
        selection_frame.columnconfigure(1, weight=1)

        ttk.Label(selection_frame, text="Auswahl", style="Bold.Secondary.TLabel").grid()
        self.cmb_jobcenter = ttk.Combobox(selection_frame, textvariable=self.selected_jobcenter)
        self.cmb_jobcenter.bind("<<ComboboxSelected>>", lambda event: self.handle_user_selection())
        self.cmb_jobcenter["state"] = "readonly"
        self.cmb_jobcenter.grid(row=0, column=1)

        btn_previous = BLImageButtonLabel(parent=selection_frame,
                                          func=lambda: self.loop_through(direction="previous"),
                                          path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/previous_01.png",
                                          path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/previous_02.png")
        btn_previous.grid(row=0, column=0, padx=(0, 10))

        btn_next = BLImageButtonLabel(parent=selection_frame,
                                      func=lambda: self.loop_through(direction="next"),
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/next_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/next_02.png")
        btn_next.grid(row=0, column=2, padx=(10, 0))

        # DATA FRAME ################################################
        self.data_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        self.data_frame.grid(padx=pad_x, pady=20, sticky="W")

        # coaches data
        self.jobcenter_name = tk.StringVar()
        self.jobcenter_street = tk.StringVar()
        self.jobcenter_street_nr = tk.StringVar()
        self.jobcenter_zip = tk.StringVar()
        self.jobcenter_city = tk.StringVar()

        self.variables = [self.jobcenter_name, self.jobcenter_street, self.jobcenter_street_nr, self.jobcenter_zip,
                          self.jobcenter_city]
        lbl_headers = ["Name", "Straße", "Nr", "PLZ", "Ort"]
        for i, item in enumerate(zip(lbl_headers, self.variables)):
            lbl_header = item[0]
            variable = item[1]
            ttk.Label(self.data_frame, text=lbl_header,
                      style="Bold.Secondary.TLabel").grid(row=i, column=0, sticky="W", padx=(40, 10))
            ttk.Label(self.data_frame, textvariable=variable,
                      style="Secondary.TLabel").grid(row=i, column=1, sticky="W")

        # NAV FRAME ################################################
        nav_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        nav_frame.grid(padx=pad_x, pady=(30, pad_y))

        btn = BLImageButtonLabel(parent=nav_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseReadDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid()

    def refresh(self) -> None:
        """Refresh the page"""
        self.get_jobcenter()
        self.fill_in_dropdown_options()
        self.update_data()

    def get_jobcenter(self) -> None:
        """Get a list of all jobcenters from the database"""
        list_of_jobcenters = self.controller.db.get_jobcenters()
        for jobcenter in list_of_jobcenters:
            self.jobcenter[str(jobcenter.data_base_id)] = jobcenter

    def fill_in_dropdown_options(self) -> None:
        """Fills the list of available options in the dropdown menu"""
        sorted_values = sorted(self.jobcenter.values(), key=lambda x: x.name)
        self.cmb_jobcenter["values"] = [f"{jobcenter.name} - (ID: "
                                           f"{jobcenter.data_base_id})" for jobcenter
                                        in sorted_values]

    def update_data(self) -> None:
        """Updates the jobcenter data that is displayed"""

        if self.selected_jobcenter is None:
            for var in self.variables:
                var.set("")
                return

        self.jobcenter_name.set(self.selected_jobcenter.name)
        self.jobcenter_street.set(self.selected_jobcenter.street)
        self.jobcenter_street_nr.set(self.selected_jobcenter.street_nr)
        self.jobcenter_zip.set(self.selected_jobcenter.zip_code)
        self.jobcenter_city.set(self.selected_jobcenter.city)

    def loop_through(self, direction: str = "next") -> None:
        """Pick the next jobcenter from the dropdown box"""
        current = self.cmb_jobcenter.current()
        length = len(self.cmb_jobcenter["values"])
        if direction == "next":
            next_jobcenter = (current + 1) % length
        else:
            next_jobcenter = (current - 1) % length
        self.cmb_jobcenter.current(next_jobcenter)

        # update data
        self.handle_user_selection()

    def handle_user_selection(self) -> None:
        """Run whenever user changes the selection in the dropdown menu"""

        # get ID
        selected_jc = self.cmb_jobcenter.get()
        id_pos = selected_jc.find("ID: ")
        the_id = selected_jc[id_pos + 4:-1]

        # Assign selected coach
        self.selected_jobcenter = self.jobcenter[the_id]

        # update data
        self.update_data()

        # append jobcenter to clipboard
        self.append_to_clipboard()

    def append_to_clipboard(self) -> None:
        """Append the selected jobcenter to clipboard"""

        self.controller.clipboard_clear()
        self.controller.clipboard_append(self.selected_jobcenter)
        self.controller.update()  # now it stays on the clipboard after the window is closed

