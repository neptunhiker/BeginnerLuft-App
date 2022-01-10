import random

from PIL import Image, ImageTk
import sqlite3
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
from typing import Type, Union

from frames import dashboard
from objects.jobcenter import Jobcenter
from objects.people import Participant, Coach
from utils.helpers import DatabaseErrorWindow, MessageWindow
from widgets.background import create_background_image
from widgets.buttons import BLImageButtonLabel
from widgets.entries import BLEntryWidget


class AddParticipant(ttk.Frame):
    """A frame that allows to add a participant to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        frame_left = ttk.Frame(self)
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)

        # create image on canvas
        create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/office01.jpg",
                                frame=frame_left, desired_width=1200)

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid()

        # header frame
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=30)
        header_frame.columnconfigure(0, weight=1)

        lbl_add_participant = ttk.Label(header_frame, text="Persönliche Informationen", style="Secondary.Header.TLabel")
        lbl_add_participant.grid()

        # CONTENT frame
        content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        content_frame.grid(padx=20)

        pad_x = 5
        pad_y = 5

        # labels
        self.lbl_title = ttk.Label(content_frame, text="Anrede*", style="Secondary.TLabel")
        self.lbl_title.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_first_name = ttk.Label(content_frame, text="Vorname*", style="Secondary.TLabel")
        self.lbl_first_name.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_last_name = ttk.Label(content_frame, text="Nachname*", style="Secondary.TLabel")
        self.lbl_last_name.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_street_and_nr = ttk.Label(content_frame, text="Straße und Nr", style="Secondary.TLabel")
        self.lbl_street_and_nr.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_zip = ttk.Label(content_frame, text="PLZ", style="Secondary.TLabel")
        self.lbl_zip.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_city = ttk.Label(content_frame, text="Ort", style="Secondary.TLabel")
        self.lbl_city.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_email = ttk.Label(content_frame, text="E-Mail", style="Secondary.TLabel")
        self.lbl_email.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_cell_phone_nr = ttk.Label(content_frame, text="Handynummer", style="Secondary.TLabel")
        self.lbl_cell_phone_nr.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_country_of_origin = ttk.Label(content_frame, text="Herkunftsland", style="Secondary.TLabel")
        self.lbl_country_of_origin.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_driving_license = ttk.Label(content_frame, text="Führerschein", style="Secondary.TLabel")
        self.lbl_driving_license.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_residency_status = ttk.Label(content_frame, text="Aufenthaltsstatus", style="Secondary.TLabel")
        self.lbl_residency_status.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        # entry fields
        self.title = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.street_and_nr = tk.StringVar()
        self.zip = tk.StringVar()
        self.city = tk.StringVar()
        self.email = tk.StringVar()
        self.cell_phone_nr = tk.StringVar()
        self.country_of_origin = tk.StringVar()
        self.driving_license = tk.StringVar()
        self.residency_status = tk.StringVar()

        self.variables = [self.title, self.first_name, self.last_name, self.street_and_nr, self.zip,
                          self.city, self.email, self.cell_phone_nr,
                          self.country_of_origin, self.driving_license, self.residency_status]

        self.cmb_title = ttk.Combobox(content_frame, textvariable=self.title)
        self.cmb_title["values"] = ["Frau", "Herr"]
        self.cmb_title["state"] = "readonly"
        self.cmb_title.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_first_name = BLEntryWidget(content_frame, textvariable=self.first_name)
        self.ent_first_name.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_last_name = BLEntryWidget(content_frame, textvariable=self.last_name)
        self.ent_last_name.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_street_and_nr = BLEntryWidget(content_frame, textvariable=self.street_and_nr)
        self.ent_street_and_nr.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_zip = BLEntryWidget(content_frame, textvariable=self.zip)
        self.ent_zip.grid(row=4, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_city = BLEntryWidget(content_frame, textvariable=self.city)
        self.ent_city.grid(row=5, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_email = BLEntryWidget(content_frame, textvariable=self.email)
        self.ent_email.grid(row=6, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_cell_phone_nr = BLEntryWidget(content_frame, textvariable=self.cell_phone_nr)
        self.ent_cell_phone_nr.grid(row=7, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.cmb_country_of_origin = ttk.Combobox(content_frame, textvariable=self.country_of_origin)
        country_list = ['Afghanistan', 'Aserbaidschan', 'Brasilien', 'Eritrea', 'Irak', 'Iran', 'Kamerun', 'Nigeria',
                        'Palästina', 'Somalia', 'Syrien', 'Türkei', 'Ukrain', 'Yemen']
        country_list = sorted(country_list)
        self.cmb_country_of_origin["values"] = country_list
        self.cmb_country_of_origin.grid(row=8, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.cmb_driving_license = ttk.Combobox(content_frame, textvariable=self.driving_license, state="readonly")
        self.cmb_driving_license["values"] = ["ja", "nein"]
        self.cmb_driving_license.grid(row=9, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.cmb_residency_status = ttk.Combobox(content_frame, textvariable=self.residency_status)
        sql = "SELECT * FROM Aufenthaltsstati"
        result = self.controller.db.select_multiple_query(sql)
        statuses = [row["Aufenthaltsstatus"] for row in result]
        self.cmb_residency_status["values"] = statuses
        self.cmb_residency_status.grid(row=10, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # go button
        btn = BLImageButtonLabel(parent=buttons_frame, func=self.next_frame,
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/next_written_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/next_written_02.png")
        btn.grid()

        # back button
        btn = BLImageButtonLabel(parent=buttons_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseCreateDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid(pady=(20, 10))

        self.pre_populate()
        self.cmb_title.focus()

    def next_frame(self) -> None:
        """Show the next frame"""

        # check if all fields have been entered that have an asterix
        if not self.completeness_check() or not self.correctness_check():
            return

        # get data from form and create Participant object
        participant = self.create_participant()

        # navigate to next frame
        self.controller.frames[AddLanguageSkills].refresh(participant=participant)
        self.controller.frames[AddLanguageSkills].tkraise()

    def create_participant(self) -> Participant:
        """Create a participant from data entered by user"""

        return Participant(
            title=self.title.get(),
            first_name=self.first_name.get(),
            last_name=self.last_name.get(),
            street_and_nr=self.street_and_nr.get(),
            zip_code=self.zip.get(),
            city=self.city.get(),
            country_of_origin=self.country_of_origin.get(),
            driving_license=self.driving_license.get(),
            email=self.email.get(),
            cell_phone_nr=self.cell_phone_nr.get(),
            residency_status=self.residency_status.get(),
        )

    # def insert_into_db(self) -> None:
    #     """Insert data into data base"""
    #
    #     # check if all fields have been entered that have an asterix
    #     if not self.completeness_check() or not self.correctness_check():
    #         return
    #
    #     # ask user to confirm data base entry to be made
    #     confirmation_to_write = self.confirm_message(self.first_name.get(), self.last_name.get())
    #     if not confirmation_to_write:
    #         self.show_abort_message()
    #         return
    #
    #     # Check if a user with a given jobcenter id already exists in database
    #     if self.controller.db.check_for_participant_jc_id(jobcenter_id=self.jc_id.get()):
    #         msg = f"Es existiert bereits ein Eintrag mit der Kundennummer {self.jc_id.get()} in der Datenbank." \
    #               f" Ein erneuter Eintrag wurde nicht vorgenommen."
    #         MessageWindow(controller=self.controller, message_header="Dateinbankeintrag bereits vorhanden",
    #                       message=msg, alert=True)
    #         return
    #
    #     # write to data base
    #     if self.write_to_db():
    #         first_name = self.first_name.get()
    #         last_name = self.last_name.get()
    #         full_name = f"{first_name} {last_name}"
    #         self.clear_all_fields()
    #         self.show_success_message(name=full_name)

    def completeness_check(self) -> bool:
        """Check if all mandatory fields have been filled out"""
        completeness_check = True

        if self.title.get() == "":
            self.lbl_title.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_title.configure(style="Secondary.TLabel")

        if self.first_name.get() == "":
            self.lbl_first_name.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_first_name.configure(style="Secondary.TLabel")

        if self.last_name.get() == "":
            self.lbl_last_name.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_last_name.configure(style="Secondary.TLabel")

        return completeness_check

    def correctness_check(self) -> bool:
        """Check whether fields have been filled in correctly"""

        if len(self.zip.get()) != 0:

            # check if given zip has 5 characters
            if len(self.zip.get()) != 5:
                self.lbl_zip.configure(style="Secondary.Emphasize.TLabel")
                return False
            else:
                # check if given zip contains only numeric values
                try:
                    int(self.zip.get())
                except ValueError:
                    self.lbl_zip.configure(style="Secondary.Emphasize.TLabel")
                    return False
                self.lbl_zip.configure(style="Secondary.TLabel")
                return True

        else:
            return True

    # def confirm_message(self, participant_first_name: str, participant_last_name: str) -> bool:
    #     """Ask user to confirm whether participant should be added to database"""
    #
    #     title = "Teilnehmer:In in Datenbank eintragen"
    #     full_name = f"{participant_first_name} {participant_last_name}"
    #     msg = f"Soll {full_name} wirklich in die Datenbank eingetragen werden?"
    #     ans = tk.messagebox.askyesno(title=title, message=msg, default="no")
    #
    #     return ans
    #
    # def write_to_db(self) -> bool:
    #     """Write participant to data base"""
    #
    #     participant = Participant(
    #         title=self.title.get(),
    #         first_name=self.first_name.get(),
    #         last_name=self.last_name.get(),
    #         street_and_nr=self.street_and_nr.get(),
    #         zip_code=self.zip.get(),
    #         city=self.city.get(),
    #         country_of_origin=self.country_of_origin.get(),
    #         driving_license=self.driving_license.get(),
    #         email=self.email.get(),
    #         cell_phone_nr=self.cell_phone_nr.get(),
    #         residency_status=self.residency_status.get(),
    #         mother_tongue=self.mother_tongue.get(),
    #         school_degree_germany=self.school_degree_germany.get(),
    #         client_id_with_jc=self.jc_id.get(),
    #     )
    #
    #     try:
    #         self.controller.db.add_participant(participant)
    #         self.controller.bl_logger.info(f"{self.controller.current_user} added participant {participant.first_name} "
    #                                        f"{participant.last_name} to the data base.")
    #     except sqlite3.OperationalError as err:
    #         print(err)
    #         DatabaseErrorWindow(self.controller)
    #         return False
    #     else:
    #         return True

    def pre_populate(self) -> None:
        """Fill the form with data for test purposes"""

        participant = Participant.test_participant()

        self.title.set(participant.title)
        self.first_name.set(participant.first_name)
        self.last_name.set(participant.last_name)
        self.street_and_nr.set(participant.street_and_nr)
        self.zip.set(participant.zip_code)
        self.city.set(participant.city)
        self.email.set(participant.email)
        self.cell_phone_nr.set(participant.cell_phone_nr)
        self.country_of_origin.set(participant.country_of_origin)
        self.driving_license.set(participant.driving_license)
        self.residency_status.set(participant.residency_status)

    def clear_all_fields(self) -> None:
        for variable in self.variables:
            variable.set("")

    # def show_abort_message(self) -> None:
    #     header = "Kein Datenbankeintrag"
    #     message = f"Für {self.first_name.get()} {self.last_name.get()} wurde kein Datenbankeintrag vorgenommen."
    #     MessageWindow(controller=self.controller, message_header=header, message=message, alert=True)
    #
    # def show_success_message(self, name: str) -> None:
    #     header = "Datenbankeintrag erfolgreich"
    #     message = f"{name} wurde erfolgreich in die Datenbank eingetragen."
    #     MessageWindow(controller=self.controller, message_header=header, message=message)


class AddCoach(ttk.Frame):
    """A frame that allows to add a coach to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        frame_left = ttk.Frame(self)
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)

        # create image on canvas
        create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/office01.jpg",
                                frame=frame_left, desired_width=1200)

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid()

        # header frame
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=30)
        header_frame.columnconfigure(0, weight=1)

        lbl_add_coach = ttk.Label(header_frame, text="Coach hinzufügen", style="Secondary.Header.TLabel")
        lbl_add_coach.grid()

        # CONTENT frame
        content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        content_frame.grid(padx=20)

        pad_x = 5
        pad_y = 5

        # labels
        self.lbl_title = ttk.Label(content_frame, text="Anrede*", style="Secondary.TLabel")
        self.lbl_title.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_first_name = ttk.Label(content_frame, text="Vorname*", style="Secondary.TLabel")
        self.lbl_first_name.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_last_name = ttk.Label(content_frame, text="Nachname*", style="Secondary.TLabel")
        self.lbl_last_name.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        # entry fields
        self.title = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()

        self.variables = [self.title, self.first_name, self.last_name]

        self.cmb_title = ttk.Combobox(content_frame, textvariable=self.title)
        self.cmb_title["values"] = ["Frau", "Herr"]
        self.cmb_title["state"] = "readonly"
        self.cmb_title.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_first_name = BLEntryWidget(content_frame, textvariable=self.first_name)
        self.ent_first_name.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_last_name = BLEntryWidget(content_frame, textvariable=self.last_name)
        self.ent_last_name.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # go button
        btn = BLImageButtonLabel(parent=buttons_frame, func=self.insert_into_db,
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/enter_into_database_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/enter_into_database_02.png")
        btn.grid()

        # back button
        btn = BLImageButtonLabel(parent=buttons_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseCreateDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid(pady=(20, 10))

        self.cmb_title.focus()

    def insert_into_db(self) -> None:
        """Insert data into data base"""

        # check if all fields have been entered that have an asterix
        if not self.completeness_check():
            return

        # ask user to confirm data base entry to be made
        confirmation_to_write = self.confirm_message(self.first_name.get(), self.last_name.get())
        if not confirmation_to_write:
            self.show_abort_message()
            return

        # check if a coach already exists with that name in database
        if self.controller.db.check_for_coach_full_name(coach_first_name=self.first_name.get(),
                                                        coach_last_name=self.last_name.get()):
            if self.abort_duplicate_entry():
                self.show_abort_message()
                return

        # write to data base
        if self.write_to_db():
            first_name = self.first_name.get()
            last_name = self.last_name.get()
            full_name = f"{first_name} {last_name}"
            self.clear_all_fields()
            self.show_success_message(name=full_name)

    def completeness_check(self) -> bool:
        """Check if all mandatory fields have been filled out"""

        completeness_check = True

        if self.title.get() == "":
            self.lbl_title.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_title.configure(style="Secondary.TLabel")

        if self.first_name.get() == "":
            self.lbl_first_name.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_first_name.configure(style="Secondary.TLabel")

        if self.last_name.get() == "":
            self.lbl_last_name.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_last_name.configure(style="Secondary.TLabel")

        return completeness_check

    def confirm_message(self, coach_first_name: str, coach_last_name: str) -> bool:
        """Ask user to confirm whether the coach should be added to database"""

        title = "Teilnehmer:In in Datenbank eintragen"
        full_name = f"{coach_first_name} {coach_last_name}"
        msg = f"Soll {full_name} wirklich in die Datenbank als Coach eingetragen werden?"
        ans = tk.messagebox.askyesno(title=title, message=msg, default="no")

        return ans

    def abort_duplicate_entry(self) -> bool:
        """Ask user to whether they want to abort a duplicate entry to the database"""

        title = "Achtung: Duplikat in Datenbank"
        full_name = f"{self.first_name.get()} {self.last_name.get()}"
        msg = f"Achtung. Es existiert bereits ein Eintrag für {full_name} in der Datenbank. Es wird empfohlen den " \
              f"Datenbankeintrag abzubrechen, damit für {full_name} nicht zwei identische Einträge in der Datenbank " \
              f"entstehen. Wenn es sich wirklich um einen anderen Coach mit gleichem Namen handelt, dann sollte " \
              f"zumindest der Vorname so angepasst werden, dass eine klare Unterscheidung zwischen den beiden Coaches " \
              f"möglich ist, zum Beispiel durch die Verwendung eines zweiten Vornames. \n\n" \
              f"Soll der Vorgang abgebrochen werden?"
        ans = tk.messagebox.askyesno(title=title, message=msg, default="yes")

        return ans

    def write_to_db(self) -> bool:
        """Write coach to data base"""

        coach = Coach(
            title=self.title.get(),
            first_name=self.first_name.get(),
            last_name=self.last_name.get(),
        )

        try:
            self.controller.db.add_coach(coach)
            self.controller.bl_logger.info(f"{self.controller.current_user} added coach {coach.first_name} "
                                           f"{coach.last_name} to the data base.")
        except sqlite3.OperationalError as err:
            print(err)
            DatabaseErrorWindow(self.controller)
            return False
        else:
            return True

    def clear_all_fields(self) -> None:
        for variable in self.variables:
            variable.set("")

    def show_abort_message(self) -> None:
        header = "Kein Datenbankeintrag"
        message = f"Für {self.first_name.get()} {self.last_name.get()} wurde kein Datenbankeintrag vorgenommen."
        MessageWindow(controller=self.controller, message_header=header, message=message, alert=True)

    def show_success_message(self, name: str) -> None:
        header = "Datenbankeintrag erfolgreich"
        message = f"{name} wurde erfolgreich in die Datenbank eingetragen."
        MessageWindow(controller=self.controller, message_header=header, message=message)


class AddJobcenter(ttk.Frame):
    """A frame that allows to add a jobcenter to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        frame_left = ttk.Frame(self)
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)

        # create image on canvas
        create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/office01.jpg",
                                frame=frame_left, desired_width=1200)

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid()

        # header frame
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=30)
        header_frame.columnconfigure(0, weight=1)

        lbl_add_jc = ttk.Label(header_frame, text="Jobcenter hinzufügen", style="Secondary.Header.TLabel")
        lbl_add_jc.grid()

        # CONTENT frame
        content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        content_frame.grid(padx=20)

        pad_x = 5
        pad_y = 5

        # labels
        self.lbl_name = ttk.Label(content_frame, text="Name*", style="Secondary.TLabel")
        self.lbl_name.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_email = ttk.Label(content_frame, text="E-Mail", style="Secondary.TLabel")
        self.lbl_email.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_street = ttk.Label(content_frame, text="Straße*", style="Secondary.TLabel")
        self.lbl_street.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_nr = ttk.Label(content_frame, text="Nr*", style="Secondary.TLabel")
        self.lbl_nr.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_zip = ttk.Label(content_frame, text="PLZ*", style="Secondary.TLabel")
        self.lbl_zip.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        self.lbl_city = ttk.Label(content_frame, text="Ort*", style="Secondary.TLabel")
        self.lbl_city.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        # entry fields
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.street = tk.StringVar()
        self.nr = tk.StringVar()
        self.zip = tk.StringVar()
        self.city = tk.StringVar()

        self.variables = [self.name, self.email, self.street, self.nr, self.zip, self.city]

        self.ent_name = BLEntryWidget(content_frame, textvariable=self.name)
        self.ent_name.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_email = BLEntryWidget(content_frame, textvariable=self.email)
        self.ent_email.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_street = BLEntryWidget(content_frame, textvariable=self.street)
        self.ent_street.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_nr = BLEntryWidget(content_frame, textvariable=self.nr)
        self.ent_nr.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_zip = BLEntryWidget(content_frame, textvariable=self.zip)
        self.ent_zip.grid(row=4, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_city = BLEntryWidget(content_frame, textvariable=self.city)
        self.ent_city.grid(row=5, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # go button
        btn = BLImageButtonLabel(parent=buttons_frame, func=self.insert_into_db,
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/enter_into_database_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/enter_into_database_02.png")
        btn.grid()

        # back button
        btn = BLImageButtonLabel(parent=buttons_frame,
                                 func=lambda: self.controller.show_frame(dashboard.DatabaseCreateDashboard),
                                 path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                 path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn.grid(pady=(20, 10))

        self.ent_name.focus()

        # self.populate_with_test_data()

    def populate_with_test_data(self) -> None:
        self.name.set("Testcenter")
        self.street.set("Berlinerstr.")
        self.nr.set("12")
        self.zip.set("12345")
        self.city.set("Berlin")

    def insert_into_db(self) -> None:
        """Insert data into data base"""

        # check if all fields have been entered that have an asterix
        if not self.completeness_check():
            return

        # ask user to confirm data base entry to be made
        confirmation_to_write = self.confirm_message(self.name.get())
        if not confirmation_to_write:
            self.show_abort_message()
            return

        # Check if a jobcenter with a given name already exists in database
        if self.controller.db.check_for_jobcenter_name(jobcenter_name=self.name.get()):
            msg = f"Für das Jobcenter '{self.name.get()}' existiert" \
                  f" bereits ein Eintrag in der Datenbank. Ein erneuter Eintrag wurde nicht vorgenommen."
            MessageWindow(
                controller=self.controller,
                message_header="Dateinbankeintrag bereits vorhanden",
                message=msg,
                alert=True
            )

        # write to data base
        if self.write_to_db():
            name = self.name.get()
            self.clear_all_fields()
            self.show_success_message(name)

    def completeness_check(self) -> bool:
        """Check if all mandatory fields have been filled out"""
        completeness_check = True

        if self.name.get() == "":
            self.lbl_name.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_name.configure(style="Secondary.TLabel")

        if self.street.get() == "":
            self.lbl_street.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_street.configure(style="Secondary.TLabel")

        if self.nr.get() == "":
            self.lbl_nr.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_nr.configure(style="Secondary.TLabel")

        if self.zip.get() == "":
            self.lbl_zip.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_zip.configure(style="Secondary.TLabel")

        if self.city.get() == "":
            self.lbl_city.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_city.configure(style="Secondary.TLabel")

        return completeness_check

    def confirm_message(self, name: str) -> bool:
        """Ask user to confirm whether jobcenter should be added to database"""

        title = "Jobcenter in Datenbank eintragen"
        msg = f"Soll '{name}' wirklich in die Datenbank als Jobcenter eingetragen werden?"
        ans = tk.messagebox.askyesno(title=title, message=msg, default="no")

        return ans

    def write_to_db(self) -> bool:
        """Write jobcenter to data base"""

        jobcenter = Jobcenter(
            name=self.name.get(),
            street=self.street.get(),
            street_nr=self.nr.get(),
            zip_code=self.zip.get(),
            city=self.city.get(),
            email=self.email.get(),
        )

        try:
            self.controller.db.add_jobcenter(jobcenter)
            self.controller.bl_logger.info(f"{self.controller.current_user} added jobcenter {jobcenter.name} "
                                           f"to the data base.")
        except sqlite3.OperationalError as err:
            print(err)
            DatabaseErrorWindow(self.controller)
            return False
        else:
            return True

    def clear_all_fields(self) -> None:
        for variable in self.variables:
            variable.set("")

    def show_abort_message(self) -> None:
        header = "Kein Datenbankeintrag"
        message = f"Für das Jobcenter '{self.name.get()}' wurde kein Datenbankeintrag vorgenommen."
        MessageWindow(controller=self.controller, message_header=header, message=message, alert=True)

    def show_success_message(self, name: str) -> None:
        header = "Datenbankeintrag erfolgreich"
        message = f"{name} wurde erfolgreich in die Datenbank eingetragen."
        MessageWindow(controller=self.controller, message_header=header, message=message)


class AddLanguageSkills(ttk.Frame):
    """A frame that allows to add a participant to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.participant = None
        self.full_name = ""
        self.widget_count = 0
        self.language_skills = {}
        self.available_languages = ["Arabisch", "Deutsch", "Englisch", "Farsi", "Italienisch", "Russisch", "Spanisch"]
        self.language_widgets = {}
        self.list_of_languages_and_levels = []
        self.error_message = tk.StringVar()
        self.error_message.set("")

        self.frame_left = ttk.Frame(self)
        self.frame_left.grid(row=0, column=0, sticky="NSEW")
        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.columnconfigure(0, weight=1)

        # create image on canvas
        create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/office01.jpg",
                                frame=self.frame_left, desired_width=1200)

        # existing language skills
        # self.show_existing_data()

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid(sticky="NSEW")
        pos_frame.columnconfigure(0, weight=1)
        pos_frame.rowconfigure(1, weight=1)

        # header frame
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=30)
        header_frame.columnconfigure(0, weight=1)

        lbl_header = ttk.Label(header_frame, text="Sprachkenntnisse", style="Secondary.Header.TLabel")
        lbl_header.grid()
        self.var_full_name = tk.StringVar()
        self.var_full_name.set(self.full_name)
        lbl_subheader = ttk.Label(header_frame, textvariable=self.var_full_name, style="Secondary.Header.TLabel")
        lbl_subheader.grid()

        # CONTENT frame
        self.content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        self.content_frame.grid(padx=20, sticky="NSEW")
        self.content_frame.columnconfigure(0, weight=1)

        btn_add = BLImageButtonLabel(
            self.content_frame,
            self.add_language,
            path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/add_language_01.png",
            path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/add_language_02.png",
        )
        btn_add.grid(pady=(10, 20))

        # LANGUAGES frame
        self.languages_frame = ttk.Frame(self.content_frame, style="Secondary.TFrame")
        self.languages_frame.grid()
        self.add_language(pre_populate=True)  # pre_populate for testing purposes
        self.add_language(pre_populate=True)

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # error message
        lbl_error_message = ttk.Label(buttons_frame, textvariable=self.error_message, style="Secondary.Error.TLabel")
        lbl_error_message.grid()

        # next button
        btn_next = BLImageButtonLabel(parent=buttons_frame, func=self.next_frame,
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/next_written_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/next_written_02.png")
        btn_next.grid()

        # back button
        btn_back = BLImageButtonLabel(parent=buttons_frame, func=lambda: self.controller.show_frame(AddParticipant),
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn_back.grid()

    def next_frame(self) -> None:
        """Navgiate to next frame"""

        if not self.completeness_check():
            self.error_message.set("Bitte Sprache und Level ausfüllen!")
            return

        if not self.duplicate_check():
            self.error_message.set("Bitte jede Sprache nur einmal auswählen!")
            return

        self.collect_data()
        self.language_skills_to_participant()

        self.clear_all_fields()
        self.error_message.set("")

        self.controller.frames[OverviewParticipant].refresh(participant=self.participant)
        self.controller.show_frame(OverviewParticipant)

    def duplicate_check(self) -> bool:
        """Check whether languages have been entered more than once"""

        language_names = [item[0].get() for item in self.list_of_languages_and_levels]
        unique_language_names = set(language_names)

        if len(language_names) != len(unique_language_names):
            return False

        return True

    def completeness_check(self) -> bool:
        """Check if all mandatory fields have been filled out"""

        if len(self.list_of_languages_and_levels) == 0:
            return False

        for item in self.list_of_languages_and_levels:
            language_name = item[0].get()
            language_level = item[1].get()
            if language_name == "" or language_level == "":
                return False

        return True

    def clear_all_fields(self) -> None:
        """Clear all existing fields and variables"""

        self.language_skills = {}
        self.list_of_languages_and_levels = []
        self.language_widgets = {}
        self.widget_count = 0
        self.error_message.set("")

        for widget in self.languages_frame.winfo_children():
            widget.destroy()

        self.add_language()

    def add_language(self, pre_populate: bool = False) -> None:
        """Add two dropdown fields for choosing a language and a language level"""

        self.language_widgets[self.widget_count] = [tk.StringVar(), tk.StringVar()]

        lbl_language_name = ttk.Label(self.languages_frame, text="Sprache", style="Secondary.TLabel")
        lbl_language_name.grid(row=self.widget_count * 2, column=0, sticky="W")

        var_language_name = self.language_widgets[self.widget_count][0]
        cmb_language_name = ttk.Combobox(self.languages_frame, textvariable=var_language_name)
        cmb_language_name["values"] = self.available_languages
        cmb_language_name.grid(row=self.widget_count * 2 + 1, column=0, sticky="W", pady=(0, 10))

        lbl_language_level = ttk.Label(self.languages_frame, text="Level", style="Secondary.TLabel")
        lbl_language_level.grid(row=self.widget_count * 2, column=1, sticky="W", padx=(10, 0))

        var_language_level = self.language_widgets[self.widget_count][1]
        cmb_language_level = ttk.Combobox(self.languages_frame, textvariable=var_language_level, state="readonly")
        cmb_language_level["values"] = ["A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache"]
        cmb_language_level.grid(row=self.widget_count * 2 + 1, column=1, sticky="W", padx=(10, 10), pady=(0, 10))

        widgets = [lbl_language_name, lbl_language_level, cmb_language_name, cmb_language_level]
        pos = self.widget_count
        btn_delete = BLImageButtonLabel(parent=self.languages_frame,
                                        func=lambda: self.delete_widgets(*widgets, btn_delete, language_pos=pos),
                                        path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/x_01.png",
                                        path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/x_02.png")
        btn_delete.grid(row=self.widget_count * 2 + 1, column=2, sticky="NW", pady=(0, 10))

        self.list_of_languages_and_levels.append([var_language_name, var_language_level])

        self.widget_count += 1

        if pre_populate:
            var_language_name.set(random.choice(("Deutsch", "Englisch", "Farsi", "Russich")))
            var_language_level.set(random.choice(("A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache")))

    def delete_widgets(self, *widgets: Union[ttk.Label, ttk.Combobox, BLImageButtonLabel], language_pos: int) -> None:
        """Removes widgets from scree"""
        for widget in widgets:
            widget.destroy()

        # set the language name and level to
        self.list_of_languages_and_levels[language_pos][0].set(None)
        self.list_of_languages_and_levels[language_pos][1].set(None)

        # remove language from dict of language and skills
        language_name = self.list_of_languages_and_levels[language_pos][0].get()
        self.language_skills.pop(language_name, None)

    def collect_data(self) -> None:
        """Write user defined languages and their levels into dictionary"""

        for item in self.list_of_languages_and_levels:
            language_name = item[0].get()
            language_level = item[1].get()
            if language_name not in ["", "None"] and language_name is not None and \
                    language_level not in ["", "None"] and language_level is not None:
                self.language_skills[language_name] = language_level

    def language_skills_to_participant(self) -> bool:
        """Assign language skills to participant"""

        self.participant.language_skills = self.language_skills

    def refresh(self, participant: Participant) -> None:
        """Update the frame"""
        self.participant = participant
        self.var_full_name.set(self.participant.full_name)

        # self.show_existing_data()
    #
    # def get_existing_language_skills(self) -> dict:
    #     """Show existing data as saved in database"""
    #
    #     sql = "SELECT * FROM Sprachkenntnisse WHERE Teilnehmer_ID = 80"
    #     results = self.controller.db.select_multiple_query(sql)
    #     existing_skils = {}
    #     for sqlite3_row in results:
    #         language_name = sqlite3_row["Sprache"]
    #         level = sqlite3_row["Level"]
    #         existing_skils[language_name] = level
    #
    #     return existing_skils
    #
    # def show_existing_data(self) -> None:
    #     """Show existing data as saved in database"""
    #
    #     # get existing skils
    #     language_skills = self.get_existing_language_skills()
    #
    #     row_counter = 0
    #     for language_name, level in language_skills.items():
    #         ttk.Label(self.frame_left, text=language_name, style="Secondary.TLabel").grid(
    #             row=row_counter, column=0, sticky="E", padx=(0, 10))
    #         ttk.Label(self.frame_left, text=level, style="Secondary.TLabel").grid(
    #             row=row_counter, column=1, sticky="W")
    #
    #         row_counter += 1

class AddWorkExperience(ttk.Frame):
    """A frame that allows to add work experience to the database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.participant = None
        self.full_name = ""
        self.widget_count = 0
        self.language_skills = {}
        self.available_languages = ["Arabisch", "Deutsch", "Englisch", "Farsi", "Italienisch", "Russisch", "Spanisch"]
        self.language_widgets = {}
        self.list_of_languages_and_levels = []
        self.error_message = tk.StringVar()
        self.error_message.set("")

        self.frame_left = ttk.Frame(self)
        self.frame_left.grid(row=0, column=0, sticky="NSEW")
        self.frame_left.rowconfigure(0, weight=1)
        self.frame_left.columnconfigure(0, weight=1)

        # create image on canvas
        create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/office01.jpg",
                                frame=self.frame_left, desired_width=1200)

        # existing language skills
        # self.show_existing_data()

        # RIGHT HAND SIDE
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid(sticky="NSEW")
        pos_frame.columnconfigure(0, weight=1)
        pos_frame.rowconfigure(1, weight=1)

        # header frame
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=30)
        header_frame.columnconfigure(0, weight=1)

        lbl_header = ttk.Label(header_frame, text="Sprachkenntnisse", style="Secondary.Header.TLabel")
        lbl_header.grid()
        self.var_full_name = tk.StringVar()
        self.var_full_name.set(self.full_name)
        lbl_subheader = ttk.Label(header_frame, textvariable=self.var_full_name, style="Secondary.Header.TLabel")
        lbl_subheader.grid()

        # CONTENT frame
        self.content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        self.content_frame.grid(padx=20, sticky="NSEW")
        self.content_frame.columnconfigure(0, weight=1)

        btn_add = BLImageButtonLabel(
            self.content_frame,
            self.add_language,
            path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/add_language_01.png",
            path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/add_language_02.png",
        )
        btn_add.grid(pady=(10, 20))

        # LANGUAGES frame
        self.languages_frame = ttk.Frame(self.content_frame, style="Secondary.TFrame")
        self.languages_frame.grid()
        self.add_language(pre_populate=True)  # pre_populate for testing purposes
        self.add_language(pre_populate=True)

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # error message
        lbl_error_message = ttk.Label(buttons_frame, textvariable=self.error_message, style="Secondary.Error.TLabel")
        lbl_error_message.grid()

        # next button
        btn_next = BLImageButtonLabel(parent=buttons_frame, func=self.next_frame,
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/next_written_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/next_written_02.png")
        btn_next.grid()

        # back button
        btn_back = BLImageButtonLabel(parent=buttons_frame, func=lambda: self.controller.show_frame(AddParticipant),
                                      path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
                                      path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png")
        btn_back.grid()

    def next_frame(self) -> None:
        """Navgiate to next frame"""

        if not self.completeness_check():
            self.error_message.set("Bitte Sprache und Level ausfüllen!")
            return

        if not self.duplicate_check():
            self.error_message.set("Bitte jede Sprache nur einmal auswählen!")
            return

        self.collect_data()
        self.language_skills_to_participant()

        self.clear_all_fields()
        self.error_message.set("")

        self.controller.frames[OverviewParticipant].refresh(participant=self.participant)
        self.controller.show_frame(OverviewParticipant)

    def duplicate_check(self) -> bool:
        """Check whether languages have been entered more than once"""

        language_names = [item[0].get() for item in self.list_of_languages_and_levels]
        unique_language_names = set(language_names)

        if len(language_names) != len(unique_language_names):
            return False

        return True

    def completeness_check(self) -> bool:
        """Check if all mandatory fields have been filled out"""

        if len(self.list_of_languages_and_levels) == 0:
            return False

        for item in self.list_of_languages_and_levels:
            language_name = item[0].get()
            language_level = item[1].get()
            if language_name == "" or language_level == "":
                return False

        return True

    def clear_all_fields(self) -> None:
        """Clear all existing fields and variables"""

        self.language_skills = {}
        self.list_of_languages_and_levels = []
        self.language_widgets = {}
        self.widget_count = 0
        self.error_message.set("")

        for widget in self.languages_frame.winfo_children():
            widget.destroy()

        self.add_language()

    def add_language(self, pre_populate: bool = False) -> None:
        """Add two dropdown fields for choosing a language and a language level"""

        self.language_widgets[self.widget_count] = [tk.StringVar(), tk.StringVar()]

        lbl_language_name = ttk.Label(self.languages_frame, text="Sprache", style="Secondary.TLabel")
        lbl_language_name.grid(row=self.widget_count * 2, column=0, sticky="W")

        var_language_name = self.language_widgets[self.widget_count][0]
        cmb_language_name = ttk.Combobox(self.languages_frame, textvariable=var_language_name)
        cmb_language_name["values"] = self.available_languages
        cmb_language_name.grid(row=self.widget_count * 2 + 1, column=0, sticky="W", pady=(0, 10))

        lbl_language_level = ttk.Label(self.languages_frame, text="Level", style="Secondary.TLabel")
        lbl_language_level.grid(row=self.widget_count * 2, column=1, sticky="W", padx=(10, 0))

        var_language_level = self.language_widgets[self.widget_count][1]
        cmb_language_level = ttk.Combobox(self.languages_frame, textvariable=var_language_level, state="readonly")
        cmb_language_level["values"] = ["A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache"]
        cmb_language_level.grid(row=self.widget_count * 2 + 1, column=1, sticky="W", padx=(10, 10), pady=(0, 10))

        widgets = [lbl_language_name, lbl_language_level, cmb_language_name, cmb_language_level]
        pos = self.widget_count
        btn_delete = BLImageButtonLabel(parent=self.languages_frame,
                                        func=lambda: self.delete_widgets(*widgets, btn_delete, language_pos=pos),
                                        path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/x_01.png",
                                        path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/x_02.png")
        btn_delete.grid(row=self.widget_count * 2 + 1, column=2, sticky="NW", pady=(0, 10))

        self.list_of_languages_and_levels.append([var_language_name, var_language_level])

        self.widget_count += 1

        if pre_populate:
            var_language_name.set(random.choice(("Deutsch", "Englisch", "Farsi", "Russich")))
            var_language_level.set(random.choice(("A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache")))

    def delete_widgets(self, *widgets: Union[ttk.Label, ttk.Combobox, BLImageButtonLabel], language_pos: int) -> None:
        """Removes widgets from scree"""
        for widget in widgets:
            widget.destroy()

        # set the language name and level to
        self.list_of_languages_and_levels[language_pos][0].set(None)
        self.list_of_languages_and_levels[language_pos][1].set(None)

        # remove language from dict of language and skills
        language_name = self.list_of_languages_and_levels[language_pos][0].get()
        self.language_skills.pop(language_name, None)

    def collect_data(self) -> None:
        """Write user defined languages and their levels into dictionary"""

        for item in self.list_of_languages_and_levels:
            language_name = item[0].get()
            language_level = item[1].get()
            if language_name not in ["", "None"] and language_name is not None and \
                    language_level not in ["", "None"] and language_level is not None:
                self.language_skills[language_name] = language_level

    def language_skills_to_participant(self) -> bool:
        """Assign language skills to participant"""

        self.participant.language_skills = self.language_skills

    def refresh(self, participant: Participant) -> None:
        """Update the frame"""
        self.participant = participant
        self.var_full_name.set(self.participant.full_name)

class OverviewParticipant(ttk.Frame):
    """A frame that gives an overview of data to be written to database"""

    def __init__(self, parent: Union[tk.Tk, ttk.Frame], controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.participant = None
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((1, 2), weight=1)

        self.frame_header = ttk.Frame(self, style="Secondary.TFrame")
        self.frame_header.grid(row=0, column=0, columnspan=3, sticky="EW", pady=50, padx=20)
        self.frame_header.columnconfigure(0, weight=1)
        ttk.Label(self.frame_header, text="Zusammenfassung", style="Secondary.Title.TLabel").grid()

        self.frame_personal_data = ttk.Frame(self, style="Border.Secondary.TFrame")
        self.frame_personal_data.grid(row=1, column=0, sticky="NSEW", padx=20, pady=20)
        ttk.Label(self.frame_personal_data, text="Persönliche Daten", style="Secondary.Header.TLabel").grid(
            columnspan=2, padx=10, pady=5, sticky="W")

        self.frame_jobcenter = ttk.Frame(self, style="Border.Secondary.TFrame")
        self.frame_jobcenter.grid(row=2, column=0, sticky="NSEW", padx=20, pady=20)
        ttk.Label(self.frame_jobcenter, text="Jobcenter", style="Secondary.Header.TLabel").grid(
            columnspan=2, padx=10, pady=5)

        self.frame_languages = ttk.Frame(self, style="Border.Secondary.TFrame")
        self.frame_languages.grid(row=1, column=1, sticky="NSEW", padx=20, pady=20)
        ttk.Label(self.frame_languages, text="Sprachkenntnisse", style="Secondary.Header.TLabel").grid(
            columnspan=2, padx=10, pady=5)

        self.frame_work = ttk.Frame(self, style="Border.Secondary.TFrame")
        self.frame_work.grid(row=2, column=1, sticky="NSEW", padx=20, pady=20)
        ttk.Label(self.frame_work, text="Arbeitserfahrung", style="Secondary.Header.TLabel").grid(
            columnspan=2, padx=10, pady=5)

        self.frame_education = ttk.Frame(self, style="Border.Secondary.TFrame")
        self.frame_education.grid(row=1, column=2, sticky="NSEW", padx=20, pady=20)
        ttk.Label(self.frame_education, text="Bildungsabschlüsse",
                  style="Secondary.Header.TLabel").grid(columnspan=2, padx=10, pady=5)

        self.frame_coaching_goals = ttk.Frame(self, style="Border.Secondary.TFrame")
        self.frame_coaching_goals.grid(row=2, column=2, sticky="NSEW", padx=20, pady=20)
        ttk.Label(self.frame_coaching_goals, text="Coaching-Ziele", style="Secondary.Header.TLabel").grid(
            columnspan=2, padx=10, pady=5)

        # BUTTON FRAME
        self.frame_buttons = ttk.Frame(self, style="Testing.TFrame")
        self.frame_buttons.grid(row=3, column=0, columnspan=3, sticky="NSEW", padx=20, pady=20)
        self.frame_buttons.columnconfigure(0, weight=1)

        btn_ok = BLImageButtonLabel(parent=self.frame_buttons, func=lambda: print("ok"),
                                    path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/ok_01.png",
                                    path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/ok_02.png")
        btn_ok.grid()

    def refresh(self, participant: Participant) -> None:
        """Refresh the page with client data"""

        self.participant = participant
        self.add_personal_data()
        self.add_language_skills()

    def add_personal_data(self) -> None:
        """Add personal data to the screen"""
        participant = self.participant

        # personal data
        labels = ["Anrede", "Vorname", "Nachname", "Straße und Nr", "PLZ und Ort", "E-Mail", "Handynummer",
                  "Herkunftsland", "Aufenthaltsstatus", "Führerschein"]
        personal_data = [participant.title, participant.first_name, participant.last_name, participant.street_and_nr,
                         f"{participant.zip_code} {participant.city}", participant.email, participant.cell_phone_nr,
                         participant.country_of_origin, participant.residency_status, participant.driving_license]

        row_counter = 1
        for label_text, data in zip(labels, personal_data):
            ttk.Label(self.frame_personal_data, text=label_text, style="Bold.Secondary.TLabel").grid(
                row=row_counter, column=0, sticky="W", padx=10, pady=2)
            ttk.Label(self.frame_personal_data, text=data, style="Secondary.TLabel").grid(
                row=row_counter, column=1, sticky="W"
            )
            row_counter += 1

    def add_language_skills(self) -> None:
        """Add language skills to the screen"""

        row_counter = 1
        for language_name, level in self.participant.language_skills.items():
            ttk.Label(self.frame_languages, text=language_name, style="Bold.Secondary.TLabel").grid(
                row=row_counter, column=0, sticky="W", padx=10, pady=5)
            ttk.Label(self.frame_languages, text=level, style="Secondary.TLabel").grid(
                row=row_counter, column=1, sticky="W")

            row_counter += 1

