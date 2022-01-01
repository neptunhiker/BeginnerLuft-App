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

        lbl_add_participant = ttk.Label(header_frame, text="Teilnehmer:In hinzufügen", style="Secondary.Header.TLabel")
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

        self.lbl_jc_id = ttk.Label(content_frame, text="Kundennummer (Jobcenter)*", style="Secondary.TLabel")
        self.lbl_jc_id.grid(column=0, sticky="W", padx=pad_x, pady=pad_y)

        # entry fields
        self.title = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.street_and_nr = tk.StringVar()
        self.zip = tk.StringVar()
        self.city = tk.StringVar()
        self.jc_id = tk.StringVar()

        self.variables = [self.title, self.first_name, self.last_name, self.street_and_nr, self.zip,
                          self.city, self.jc_id]

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

        self.ent_jc_id = BLEntryWidget(content_frame, textvariable=self.jc_id)
        self.ent_jc_id.grid(row=6, column=1, padx=pad_x, pady=pad_y, sticky="EW")

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
        if not self.completeness_check() or not self.correctness_check():
            return

        # ask user to confirm data base entry to be made
        confirmation_to_write = self.confirm_message(self.first_name.get(), self.last_name.get())
        if not confirmation_to_write:
            self.show_abort_message()
            return

        # Check if a user with a given jobcenter id already exists in database
        if self.controller.db.check_for_participant_jc_id(jobcenter_id=self.jc_id.get()):
            msg = f"Es existiert bereits ein Eintrag mit der Kundennummer {self.jc_id.get()} in der Datenbank." \
                  f" Ein erneuter Eintrag wurde nicht vorgenommen."
            MessageWindow(message_header="Dateinbankeintrag bereits vorhanden", message=msg, alert=True)
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

        if self.jc_id.get() == "":
            self.lbl_jc_id.configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False
        else:
            self.lbl_jc_id.configure(style="Secondary.TLabel")

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

    def confirm_message(self, participant_first_name: str, participant_last_name: str) -> bool:
        """Ask user to confirm whether participant should be added to database"""

        title = "Teilnehmer:In in Datenbank eintragen"
        full_name = f"{participant_first_name} {participant_last_name}"
        msg = f"Soll {full_name} wirklich in die Datenbank eingetragen werden?"
        ans = tk.messagebox.askyesno(title=title, message=msg, default="no")

        return ans

    def write_to_db(self) -> bool:
        """Write participant to data base"""

        participant = Participant(
            title=self.title.get(),
            first_name=self.first_name.get(),
            last_name=self.last_name.get(),
            street_and_nr=self.street_and_nr.get(),
            zip_code=self.zip.get(),
            city=self.city.get(),
            client_id_with_jc=self.jc_id.get(),
        )

        try:
            self.controller.db.add_participant(participant)
            self.controller.bl_logger.info(f"{self.controller.current_user} added participant {participant.first_name} "
                                           f"{participant.last_name} to the data base.")
        except sqlite3.OperationalError as err:
            print(err)
            DatabaseErrorWindow()
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
            DatabaseErrorWindow()
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
            DatabaseErrorWindow()
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
