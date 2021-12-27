import datetime
import os
import sqlite3
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from objects.data_picker import PickJobcenter, PickParticipant, PickTraining
from objects.invoice import Invoice
from widgets.labels import BLBoldClickableSecondaryLabel
from reports.invoice import PDFInvoice
from tools import helpers
from tools import custom_exceptions

from widgets.buttons import BLButton, BLImageButtonLabel


class Invoice(ttk.Frame):
    """A test frame for a frame with a picture on the left hand side"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.error_text = tk.StringVar()

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
        frame_right.rowconfigure((0, 1, 2), weight=1)

        # header frame
        header_frame = ttk.Frame(frame_right, style="Testing.TFrame")
        header_frame.grid(sticky="EW", padx=20)
        header_frame.columnconfigure(0, weight=1)

        lbl_test = ttk.Label(
            header_frame,
            text="Rechnungserstellung",
            style="Secondary.Header.TLabel",
            anchor="center",
        )
        lbl_test.grid(sticky="EW")

        # data frame
        self.data_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        self.data_frame.grid(padx=20)

        sep_pad_y = 10

        # participant data
        self.participant_title = tk.StringVar()
        self.participant_first_name = tk.StringVar()
        self.participant_last_name = tk.StringVar()
        self.participant_jc_id = tk.StringVar()
        lbl_texts = ["Anrede", "Vorname", "Nachname", "Kundennummer"]
        string_variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                            self.participant_jc_id]
        next_row = self.create_widgets(
            frame=self.data_frame,
            title="Teilnehmer",
            label_texts=lbl_texts,
            string_variables=string_variables,
            func=self.pick_participant_from_db,
        )

        # job center data
        sep = ttk.Separator(self.data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Name des Jobcenters", "Straße und Nr", "PLZ und Ort"]
        self.jc_name = tk.StringVar()
        self.jc_street_and_nr = tk.StringVar()
        self.jc_zip_and_city = tk.StringVar()
        string_variables = [self.jc_name]
        next_row = self.create_widgets(
            frame=self.data_frame,
            title="Jobcenter",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
            func=self.pick_jobcenter_from_db,
        )
        for item_label, variable in zip(["Straße und Nr", "PLZ und Ort"], [self.jc_street_and_nr, self.jc_zip_and_city]):
            ttk.Label(self.data_frame, style="Secondary.TLabel", text=item_label).grid(
                row=next_row, column=1, pady=5, sticky="W")
            ttk.Label(self.data_frame, style="Secondary.TLabel", textvariable=variable).grid(
                row=next_row, column=2, pady=5, sticky="W")
            next_row += 1

        # training data (Maßnahme)
        sep = ttk.Separator(self.data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Maßnahme"]
        self.training_name = tk.StringVar()
        self.training_cost_per_lesson = tk.StringVar()
        self.training_id = tk.StringVar()  # not needed here but keep it as it is used by data picker
        string_variables = [self.training_name]
        next_row = self.create_widgets(
            frame=self.data_frame,
            title="Maßnahme",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
            func=self.pick_training_from_db,
        )
        lbl = ttk.Label(self.data_frame, text="Kosten pro Unterrichtseinheit", style="Secondary.TLabel")
        lbl.grid(row=next_row, column=1, sticky="W", pady=5)
        lbl_cost = ttk.Label(self.data_frame, textvariable=self.training_cost_per_lesson, style="Secondary.TLabel")
        lbl_cost.grid(row=next_row, column=2, sticky="W", pady=5)
        next_row += 1

        # coaching data
        sep = ttk.Separator(self.data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Coaching-Beginn", "Coaching-Ende", "Anzahl Unterrichtseinheiten"]
        self.training_start = tk.StringVar()
        self.training_end = tk.StringVar()
        self.training_nr_training_lesseons = tk.StringVar()
        string_variables = [self.training_start, self.training_end, self.training_nr_training_lesseons]
        next_row = self.create_widgets(
            frame=self.data_frame,
            title="Coaching",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
        )

        # invoice data
        sep = ttk.Separator(self.data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Rechnungsdatum", "Zahlungsziel", "Rechnungsnummer", "Name der Rechnungsdatei"]
        self.invoice_nr = tk.StringVar()
        self.invoice_name = tk.StringVar()
        self.invoice_creation_date = tk.StringVar()
        self.invoice_target_date = tk.StringVar()
        string_variables = [self.invoice_creation_date, self.invoice_target_date, self.invoice_nr, self.invoice_name]
        next_row = self.create_widgets(
            frame=self.data_frame,
            title="Rechnungsdaten",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
        )

        # change invoice name and nr when participant data and invoice creation date changes
        for variable in [self.participant_first_name, self.participant_last_name, self.invoice_creation_date]:
            variable.trace("w", self.change_invoice_nr)
            variable.trace("w", self.change_invoice_name)

        # LOWER FRAME
        button_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        button_frame.grid(row=2, column=0, sticky="EW")
        button_frame.columnconfigure(0, weight=1)

        # error text
        lbl_error = ttk.Label(button_frame, textvariable=self.error_text, style="Secondary.Error.TLabel")
        lbl_error.grid(pady=(0, 10))

        # Go button
        btn = BLImageButtonLabel(parent=button_frame, func=self.create_invoice, path_to_file_01="assets/buttons/invoice_01.png",
                                 path_to_file_02="assets/buttons/invoice_02.png")
        btn.grid()

        # back button
        btn = BLImageButtonLabel(parent=button_frame, func=self.controller.nav_to_dashboard,
                                 path_to_file_01="assets/buttons/back_01.png",
                                 path_to_file_02="assets/buttons/back_02.png")
        btn.grid(pady=(10, 5))

        self.variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                          self.participant_jc_id, self.jc_name, self.jc_street_and_nr, self.jc_zip_and_city,
                          self.training_name, self.training_nr_training_lesseons, self.training_start,
                          self.training_end, self.training_cost_per_lesson, self.invoice_name, self.invoice_nr,
                          self.invoice_creation_date, self.invoice_target_date]
        # create random data
        self.pre_populate()
        # self.populate_with_random_data()

    def change_invoice_name(self, var, index, mode):
        """Update the invoice name based on data entries"""

        try:
            self.invoice_name.set(helpers.create_invoice_name(
                creation_date=self.invoice_creation_date.get(),
                participant_first_name=self.participant_first_name.get(),
                participant_last_name=self.participant_last_name.get(),
            ))
        except custom_exceptions.DateFormatException as err:
            print(err)
            self.invoice_name.set("")
        except ValueError as err:
            print(err)
            self.invoice_name.set("")
        except IndexError as err:
            print(err)
            self.invoice_name.set("")
        except AttributeError as err:
            print(err)
            self.invoice_name.set("")

    def change_invoice_nr(self, var, index, mode):
        """Update the invoice nr based on data entries"""
        try:
            self.invoice_nr.set(helpers.create_invoice_nr(
                creation_date=self.invoice_creation_date.get(),
                participant_first_name=self.participant_first_name.get(),
                participant_last_name=self.participant_last_name.get()
            ))
        except custom_exceptions.DateFormatException:
            self.invoice_nr.set("")
        except ValueError:
            self.invoice_nr.set("")
        except IndexError:
            self.invoice_nr.set("")
        except AttributeError:
            self.invoice_nr.set("")

    def pick_jobcenter_from_db(self, event):
        """Opens a new window that allows the user to pick a jobcenter from the database"""
        PickJobcenter(controller=self.controller, parent=self)

    def pick_participant_from_db(self, event):
        """Opens a new window that allows the user to pick a participant from the database"""
        PickParticipant(controller=self.controller, parent=self)

    def pick_training_from_db(self, event):
        """Opens a new window that allows the user to pick a training (Maßnahme) from the database"""
        PickTraining(controller=self.controller, parent=self)

    def create_widgets(self, frame, title, label_texts, string_variables, starting_row=0, func=None):
        """Create title, label, and entry widgets"""

        pad_y = 5

        if func is None:
            lbl_header = ttk.Label(
                frame,
                text=title,
                style="Bold.Secondary.TLabel"
            )
        else:
            lbl_header = BLBoldClickableSecondaryLabel(
                parent=frame,
                text=title,
            )
            lbl_header.bind("<Button-1>", func)

        lbl_header.grid(column=0, row=starting_row, sticky="W", padx=(0, 30))

        row_counter = starting_row
        for lbl_text, string_variable in zip(label_texts, string_variables):
            lbl = ttk.Label(frame, text=lbl_text, style="Secondary.TLabel")
            lbl.grid(row=row_counter, column=1, sticky="W", pady=pad_y, padx=(0, 10))
            entry = ttk.Entry(frame, textvariable=string_variable, width=25)
            entry.grid(row=row_counter, column=2, sticky="W", pady=pad_y)
            # entry.bind("<Button-1>", lambda event, widget=entry: self.turn_entry_red(event, widget=entry))  # only works for the last entry in the loop
            row_counter += 1

        return row_counter

    def check_completeness(self):

        completeness_check = True

        # participants
        pariticpant_entry_fields = [self.participant_title, self.participant_first_name, self.participant_last_name,
                                    self.participant_jc_id]

        # invoice
        invoice_entry_fields = [self.invoice_name, self.invoice_nr, self.invoice_creation_date,
                                self.invoice_target_date]

        # training (Maßnahme)
        training_entry_fields = [self.training_name, self.training_cost_per_lesson]

        # coaching
        coaching_entry_fields = [self.training_start, self.training_end, self.training_nr_training_lesseons]

        # jobcenter
        jc_entry_fields = [self.jc_name, self.jc_street_and_nr, self.jc_zip_and_city]

        for category in [pariticpant_entry_fields, invoice_entry_fields, training_entry_fields, coaching_entry_fields,
                         jc_entry_fields]:
            for field in category:
                if field.get() == "":
                    completeness_check = False

        if completeness_check:
            self.error_text.set("")
        else:
            self.error_text.set("Bitte alle Datenfelder ausfuellen.")

        return completeness_check

    def check_correctness(self):
        """Check correctness of data"""

        correctness_check = True

        try:
            helpers.string_to_float(self.training_cost_per_lesson.get())
            int(self.training_nr_training_lesseons.get())
            coaching_start = helpers.parse_date_from_string(self.training_start.get())
            coaching_end = helpers.parse_date_from_string(self.training_end.get())
            creation_date = helpers.parse_date_from_string(self.invoice_creation_date.get())
            target_date = helpers.parse_date_from_string(self.invoice_target_date.get())

            if target_date <= creation_date:
                error_text = "Das Zahlungsziel muss zeitlich nach dem Rechnungsdatum liegen."
                correctness_check = False
            elif coaching_end <= coaching_start:
                error_text = "Das Coaching-Ende muss zeitlich nach dem Coaching-Beginn liegen."
                correctness_check = False

        except Exception:

            correctness_check = False
            error_text = "Bitte alle Datenfelder im richtigen Format ausfuellen."

        if correctness_check:
            self.error_text.set("")
        else:
            self.error_text.set(error_text)

        return correctness_check

    def create_invoice(self):
        """Creates a PDF invoice and saves it on file"""

        if self.check_correctness() and self.check_completeness():

            self.update()

            creation_date = helpers.parse_date_from_string(self.invoice_creation_date.get())
            target_date = helpers.parse_date_from_string(self.invoice_target_date.get())
            coaching_start = helpers.parse_date_from_string(self.training_start.get())
            coaching_end = helpers.parse_date_from_string(self.training_end.get())
            training_cost_per_lesson = helpers.string_to_float(self.training_cost_per_lesson.get())
            training_lessons = int(self.training_nr_training_lesseons.get())
            invoice_total_amount = training_cost_per_lesson * training_lessons

            # ask user where to save the file
            path = tk.filedialog.askdirectory(initialdir="../Output/PDF Rechnungen")

            if path:
                saving_path = os.path.join(path, f"{self.invoice_name.get()}.pdf")

                # if file does not exist yet, create it
                overwrite = True
                if helpers.check_if_file_exists(saving_path):

                    overwrite = messagebox.askyesno(
                        "Rechnung existiert bereits",
                        f"Es existiert bereits eine Rechnung für {self.participant_first_name.get()} "
                        f"{self.participant_last_name.get()} am gewählten Speicherort. Soll die Rechnung "
                        f"überschrieben werden?",
                        default="no"
                    )

                if overwrite:
                    PDFInvoice.from_data(
                        participant_title=self.participant_title.get(),
                        participant_first_name=self.participant_first_name.get(),
                        participant_last_name=self.participant_last_name.get(),
                        participant_id=self.participant_jc_id.get(),
                        invoice_name=self.invoice_name.get(),
                        invoice_total_amount=invoice_total_amount,
                        invoice_nr=self.invoice_nr.get(),
                        invoice_creation_date=creation_date,
                        invoice_target_date=target_date,
                        training_name=self.training_name.get(),
                        training_cost_per_lesson=training_cost_per_lesson,
                        coaching_start=coaching_start,
                        coaching_end=coaching_end,
                        coaching_nr_lessons=training_lessons,
                        jc_name=self.jc_name.get(),
                        jc_street_and_nr=self.jc_street_and_nr.get(),
                        jc_zip=self.jc_zip_and_city.get().split()[0],
                        jc_city=self.jc_zip_and_city.get().split()[1],
                        path=path
                    )
                    full_name = f"{self.participant_first_name.get()} {self.participant_last_name.get()}"
                    logging_msg = f"{self.controller.current_user} successfully created an invoice document for " \
                                  f"{full_name}."
                    self.controller.bl_logger.info(logging_msg)
                    self.clear_all()

                    helpers.MessageWindow(message_header="Rechnung erstellt",
                                          message=f"Rechnung für {full_name} erstellt unter: \n\n"
                                                  f"{saving_path}",
                                          )

                else:
                    helpers.MessageWindow(message_header="Keine Rechnung erstellt",
                                          message=f"Es wurde keine Rechnung für {self.participant_first_name.get()} "
                                                  f"{self.participant_last_name.get()} erstellt.",
                                          alert=True)

    def pre_populate(self):
        """Populates the form with some data"""
        try:
            training_name = "Individuelles Berufscoaching"
            self.training_name.set(training_name)
            sql = f"SELECT * FROM Massnahmen WHERE Bezeichnung = '{training_name}'"
            training_cost = self.controller.db.select_single_query(sql)["Kosten_pro_UE"]
            self.training_cost_per_lesson.set(training_cost)
        except sqlite3.OperationalError as err:
            print(err)
            print("Cannot pre-populate the invoice form")

        self.invoice_creation_date.set(datetime.date.today().strftime("%d.%m.%Y"))
        self.invoice_target_date.set(helpers.determine_payment_target_date(datetime.date.today(), 14).
                                     strftime("%d.%m.%Y"))

    def populate_with_random_data(self):

        self.participant_title.set("Herr")
        self.participant_first_name.set("Juri")
        self.participant_last_name.set("Ali")
        self.participant_jc_id.set("1234567-DE")

        creation_date = datetime.date(2021, 12, 22)
        self.invoice_name.set(f"Rechnung {str(creation_date.year)}-{str(creation_date.month)}-JA")
        self.invoice_nr.set(f"{str(creation_date.year)}-{str(creation_date.month)}-JA")
        self.invoice_creation_date.set("22.12.2021")
        self.invoice_target_date.set("6.1.2022")

        self.training_name.set("Test Maßnahme")
        self.training_start.set("09.06.2021")
        self.training_end.set("12.09.2021")
        self.training_nr_training_lesseons.set("40")
        self.training_cost_per_lesson.set("12,34")

        self.jc_name.set("Testjobcenter")
        self.jc_street_and_nr.set("Berlinerstr. 987")
        self.jc_zip_and_city.set("12321 Berlin")

    def turn_entry_red(self, event, widget):
        """Turns the value of an Entry field to red"""
        widget.configure(style="Error.TEntry")

    def clear_all(self):
        """Clears fields and fills based on pre-fill settings"""
        for variable in self.variables:
            variable.set("")
        self.pre_populate()