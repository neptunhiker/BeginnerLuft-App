import sqlite3
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk


from objects.people import Participant
from tools.helpers import DatabaseErrorWindow, MessageWindow
from widgets.buttons import BLButton


class AddParticipant(ttk.Frame):
    """A frame that allows to add a participant to the database"""

    def __init__(self, parent, controller):
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

        # create background image
        image = Image.open("assets/office02.jpg")
        desired_width = 800
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        # create canvas
        canvas = tk.Canvas(frame_left)
        canvas.grid(row=0, column=0, sticky="NSEW")

        # set image in canvas
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image

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

        self.cmb_title = ttk.Combobox(content_frame, textvariable=self.title)
        self.cmb_title["values"] = ["Frau", "Herr"]
        self.cmb_title.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_first_name = ttk.Entry(content_frame, textvariable=self.first_name)
        self.ent_first_name.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_last_name = ttk.Entry(content_frame, textvariable=self.last_name)
        self.ent_last_name.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_street_and_nr = ttk.Entry(content_frame, textvariable=self.street_and_nr)
        self.ent_street_and_nr.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_zip = ttk.Entry(content_frame, textvariable=self.zip)
        self.ent_zip.grid(row=4, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_city = ttk.Entry(content_frame, textvariable=self.city)
        self.ent_city.grid(row=5, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        self.ent_jc_id = ttk.Entry(content_frame, textvariable=self.jc_id)
        self.ent_jc_id.grid(row=6, column=1, padx=pad_x, pady=pad_y, sticky="EW")

        # FRAME buttons
        buttons_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        buttons_frame.grid(row=2, column=0, sticky="EW", pady=30)
        buttons_frame.columnconfigure(0, weight=1)

        # go button
        btn = BLButton(buttons_frame, text="In Datenbank eintragen", command=self.insert_into_db)
        btn.grid()

        self.cmb_title.focus()

    def insert_into_db(self):
        """Inser data into data base"""

        # check if all fields have been entered that have an asterix
        if not self.completeness_check() or not self.correctness_check():
            return

        # ask user to confirm data base entry to be made
        confirmation_to_write = self.confirm_message(self.first_name.get(), self.last_name.get())
        if not confirmation_to_write:
            return

        # write to data base
        if self.write_to_db():
            self.show_success_message()

    def completeness_check(self):
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

    def correctness_check(self):
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

    def confirm_message(self, participant_first_name, participant_last_name):
        """Ask user to confirm whether participant should be added to database"""

        title = "Teilnehmer:In in Datenbank eintragen"
        full_name = f"{participant_first_name} {participant_last_name}"
        msg = f"Soll {full_name} wirklich in die Datenbank eingetragen werden?"
        ans = tk.messagebox.askyesno(title=title, message=msg, default="no")

        return ans

    def write_to_db(self):
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
        except sqlite3.OperationalError as err:
            print(err)
            DatabaseErrorWindow()
            return False
        except sqlite3.IntegrityError as err:
            print(err)
            msg = f"Für {self.first_name.get()} {self.last_name.get()} mit der Kundennummer {self.jc_id.get()} existiert" \
                  f" bereits ein Eintrag in der Datenbank. Ein erneuter Eintrag wurde nicht vorgenommen."
            MessageWindow(message_header="Dateinbankeintrag bereits vorhanden", message=msg)
        else:
            return True

    def show_success_message(self):
        header = "Datenbankeintrag erfolgreich"
        message = f"{self.first_name.get()} {self.last_name.get()} wurde erfolgreich in die Datenbank eingetragen."
        MessageWindow(message_header=header, message=message)