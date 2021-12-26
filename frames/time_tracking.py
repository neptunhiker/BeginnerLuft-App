import datetime
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import os
from PIL import Image, ImageTk

from tools import helpers
from objects.data_picker import PickParticipant, PickTraining
from reports.time_tracking.time_tracking import TimeReport
from widgets.buttons import BLImageButtonLabel
from widgets.labels import BLBoldClickableSecondaryLabel


class TimeTracking(ttk.Frame):
    """A frame that allows user to create a pdf for time tracking of coachings"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.participant_title = tk.StringVar()
        self.participant_first_name = tk.StringVar()
        self.participant_last_name = tk.StringVar()
        self.participant_jc_id = tk.StringVar()
        self.training_name = tk.StringVar()
        self.training_id = tk.StringVar()
        self.training_cost_per_lesson = tk.StringVar()  # not needed but keep it as it is passed by datapicker
        # self.avgs_coupon_id = tk.StringVar()
        self.confirmation_period_start = tk.StringVar()
        self.confirmation_period_end = tk.StringVar()
        self.file_path_time_sheet_bl = tk.StringVar()
        self.file_path_time_sheet_coach = tk.StringVar()

        self.variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                          self.participant_jc_id, self.training_name, self.training_id,
                          self.confirmation_period_start, self.confirmation_period_end, self.file_path_time_sheet_bl,
                          self.file_path_time_sheet_coach]

        # FRAME left
        frame_left = ttk.Frame(self)
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)

        # create background image
        image = Image.open("assets/office01.jpg")
        desired_width = 1200
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

        # RIGHT HAND SIDE ----------------------------------------------------
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure(0, weight=1)

        # POSITIONING frame ----------------------------------------------------
        pos_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        pos_frame.grid(row=0, sticky="NSEW")
        pos_frame.columnconfigure(0, weight=1)
        pos_frame.rowconfigure(1, weight=1)

        # HEADER frame ----------------------------------------------------
        header_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        header_frame.grid(row=0, sticky="EW", padx=10, pady=(50, 0))
        header_frame.columnconfigure(0, weight=1)

        # header
        header = ttk.Label(header_frame, text="Zeiterfassung", style="Secondary.Header.TLabel")
        header.grid()

        # CONTENT frame ----------------------------------------------------
        self.content_frame = ttk.Frame(pos_frame, style="Secondary.TFrame")
        self.content_frame.grid(row=1, padx=10)
        # self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        sep_pad_y = 10
        self.pad_x = 20
        self.pad_y = 5
        self.labels = {}

        # next_row = self.create_labels_participant(0)

        descriptions = ["Anrede", "Vorname", "Nachname", "Kundennummer"]
        variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                     self.participant_jc_id]
        next_row = self.create_header_labels_labels(starting_row=0, header_text="Teilnehmer:In",
                                                    header_func=self.pick_participant_from_db,
                                                    descriptions=descriptions, variables=variables, sep=False)

        # trainings
        descriptions = ["Bezeichnung", "ID"]
        variables = [self.training_name, self.training_id]
        next_row = self.create_header_labels_labels(starting_row=next_row, header_text="Maßnahme",
                                                    header_func=self.pick_training_from_db, descriptions=descriptions,
                                                    variables=variables, sep=True)

        # # AVGS coupon
        # descriptions = ["Nummer"]
        # variables = [self.avgs_coupon_id]
        # next_row = self.create_header_labels_entries(starting_row=next_row, header_text="AVGS-Gutschein",
        #                                              header_func=None, descriptions=descriptions,
        #                                              variables=variables, sep=True)

        # Confirmation period (Bewilligungszeitraum)
        descriptions = ["Beginn", "Ende"]
        variables = [self.confirmation_period_start, self.confirmation_period_end]
        next_row = self.create_header_labels_entries(starting_row=next_row, header_text="Bewilligungszeitraum",
                                                     header_func=None, descriptions=descriptions,
                                                     variables=variables, sep=True)

        # Date files for time sheets
        descriptions = ["Datei BeginnerLuft", "Datei Coach"]
        variables = [self.file_path_time_sheet_bl, self.file_path_time_sheet_coach]
        self.create_file_picker(starting_row=next_row, header_text="Zeiterfassung-Sheets", descriptions=descriptions,
                                variables=variables, sep=True)

        # FRAME action ----------------------------------------------------
        action_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        action_frame.grid(row=1, column=0, sticky="EW", padx=10)
        action_frame.columnconfigure(0, weight=1)

        btn_go = BLImageButtonLabel(
            parent=action_frame,
            func=self.go_button,
            path_to_file_01="assets/buttons/timetracking_sheet_01.png",
            path_to_file_02="assets/buttons/timetracking_sheet_02.png",
        )
        btn_go.grid(pady=10)

        # FRAME navigation ----------------------------------------------------
        nav_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        nav_frame.grid(row=2, column=0, sticky="EW", padx=10)
        nav_frame.columnconfigure(0, weight=1)

        btn_img_back = BLImageButtonLabel(
            parent=nav_frame,
            func=self.back_button,
            path_to_file_01="assets/buttons/back_01.png",
            path_to_file_02="assets/buttons/back_02.png",
        )
        btn_img_back.grid(pady=10)

        self.pre_populate()
        # self.populate_with_test_data()

    def pre_populate(self):
        """Populates the form with some data"""

        training_name = "Individuelles Berufscoaching"
        self.training_name.set(training_name)
        sql = f"SELECT * FROM Massnahmen WHERE Bezeichnung = '{training_name}'"
        training_id = self.controller.db.select_single_query(sql)["ID"]
        self.training_id.set(training_id)

    def populate_with_test_data(self):
        self.participant_title.set("Herr")
        self.participant_first_name.set("Jimmy")
        self.participant_last_name.set("Murt")
        self.participant_jc_id.set("jcid123")
        # self.avgs_coupon_id.set("lsajfd123")
        self.training_name.set("fast ind. Coaching")
        self.training_id.set("123321")
        self.confirmation_period_start.set("22.01.1984")
        self.confirmation_period_end.set("29.03.1984")
        self.file_path_time_sheet_bl.set("/Volumes/GoogleDrive/Meine Ablage/2021-10-03 Operations/Arbeitsordner/Python/Zeiterfassung/BL-Time-Tracking/resources/Zeiterfassung Ahmed Muhadi.xlsx")
        self.file_path_time_sheet_coach.set("/Volumes/GoogleDrive/Meine Ablage/2021-10-03 Operations/Arbeitsordner/Python/Zeiterfassung/BL-Time-Tracking/resources/Zeiterfassung Ahmed Muhadi.xlsx")

    def go_button(self):

        # completeness check
        if not self.completeness_check():
            return
        # correctness check
        if not self.correctness_check():
            return

        # Instantiate the TimeReport
        try:
            report = TimeReport(
                file_coach=self.file_path_time_sheet_coach.get(),
                file_bl=self.file_path_time_sheet_bl.get(),
                participant_title=self.participant_title.get(),
                participant_first_name=self.participant_first_name.get(),
                participant_last_name=self.participant_last_name.get(),
                participant_jc_id=self.participant_jc_id.get(),
                training_name=self.training_name.get(),
                training_nr=self.training_id.get(),
                confirmation_period_start=helpers.parse_date_from_string(self.confirmation_period_start.get()),
                confirmation_period_end=helpers.parse_date_from_string(self.confirmation_period_end.get())
            )
        except Exception as err:
            print(err)
            helpers.MessageWindow("Zeiterfassung nicht erstellt!",
                                  f"Leider ist etwas schiefgegangen! Bitte Dateneingaben überprüfen. Ggf. liegen "
                                  f"die ausgewählten Dateien nicht im richtigen Format (excel) vor oder die Excel-"
                                  f"Dateien haben nicht die richtige Struktur (Anzahl der Spalten, Spaltenüberschriften"
                                  f" o.ä.)", height=300)
            return

        # ask user where to save the file
        today = datetime.date.today().strftime("%Y-%m-%d")
        pre_filled_file_name = f"{today} Zeiterfassung {self.participant_first_name.get()} " \
                               f"{self.participant_last_name.get()}.pdf"
        path = asksaveasfilename(title="BeginnerLuft Zeiterfassung", initialdir="../Output/Zeiterfassung",
                                 initialfile=pre_filled_file_name, filetypes=(("pdf", "*.pdf"),))
        if path:
            try:
                report.create_report(path=path)
            except Exception as err:
                print(err)
                helpers.MessageWindow("Kein Zeiterfassungs-Sheet erstellt!", f"Leider ist etwas schiefgegangen! Bitte "
                                                                       f"Dateneingaben überprüfen.")
                return
            else:
                full_name = f"{self.participant_first_name.get()} {self.participant_last_name.get()}"
                self.clear_all()
                helpers.MessageWindow("Zeiterfassungs-Sheet erstellt!",
                                      f"Ein Zeiterfassungs-Sheet für {full_name} wurde "
                                      f"unter \n\n'{path}' \n\n erstellt.",
                                      height=300)

    def back_button(self):
        self.controller.back_to_dashboard()

    def completeness_check(self):
        """Check whether all data have been filled out"""

        completeness_check = True
        trigger_words = ["", "Bitte auswählen", "Bitte Datei auswählen"]

        # check that all required fields have been filled out except the data file picker fields
        for lbl_text, item in self.labels.items():

            if lbl_text not in ["Datei Coach", "Datei BeginnerLuft"]:

                if item[1].get() in trigger_words:
                    item[0].configure(style="Secondary.Emphasize.TLabel")
                    completeness_check = False
                else:
                    item[0].configure(style="Secondary.TLabel")

        # if both data file picker fields are empty fail the completeness check else pass it
        if self.file_path_time_sheet_coach.get() in trigger_words and self.file_path_time_sheet_bl.get() in trigger_words:
            self.labels["Datei Coach"][0].configure(style="Secondary.Emphasize.TLabel")
            self.labels["Datei BeginnerLuft"][0].configure(style="Secondary.Emphasize.TLabel")
            completeness_check = False

        else:
            self.labels["Datei Coach"][0].configure(style="Secondary.TLabel")
            self.labels["Datei BeginnerLuft"][0].configure(style="Secondary.TLabel")

        return completeness_check

    def correctness_check(self):
        """Check whether data have been entered correctly"""

        # check if entered dates are dates indeed
        errors = 0
        for lbl_text in ["Beginn", "Ende"]:

            try:
                helpers.parse_date_from_string(self.labels[lbl_text][1].get())
            except:
                self.labels[lbl_text][0].configure(style="Secondary.Emphasize.TLabel")
                errors += 1
            else:
                self.labels[lbl_text][0].configure(style="Secondary.TLabel")

        if errors == 0:
            correctness_check = True
        else:
            correctness_check = False

        # check if confirmation period end is after confirmation period start
        if correctness_check:

            start = helpers.parse_date_from_string(self.confirmation_period_start.get())
            end = helpers.parse_date_from_string(self.confirmation_period_end.get())

            if end < start:
                correctness_check = False
                for lbl_text in ["Beginn", "Ende"]:
                    self.labels[lbl_text][0].configure(style="Secondary.Emphasize.TLabel")
            else:
                correctness_check = True
                for lbl_text in ["Beginn", "Ende"]:
                    self.labels[lbl_text][0].configure(style="Secondary.TLabel")

        return correctness_check


    def pick_participant_from_db(self, event):
        """Opens a new window that allows the user to pick a participant from the database"""
        PickParticipant(controller=self.controller, parent=self)

    def pick_training_from_db(self, event):
        """Opens a new window that allows the user to pick a training (Maßnahme) from the database"""
        PickTraining(controller=self.controller, parent=self)

    def create_header_labels_entries(self, starting_row, header_text, descriptions, variables, header_func=None, sep=False):
        """Create a header, static labels and dynamic entry fields"""

        if sep is True:
            ttk.Separator(self.content_frame).grid(row=starting_row, column=0, columnspan=3,
                                                   sticky="EW", pady=10)
            starting_row += 1

        if header_func is not None:
            lbl = BLBoldClickableSecondaryLabel(self.content_frame, text=header_text)
            lbl.bind("<Button-1>", header_func)
        else:
            lbl = ttk.Label(self.content_frame, text=header_text, style="Bold.Secondary.TLabel")

        lbl.grid(row=starting_row, column=0, sticky="W", pady=self.pad_y)

        for i, item in enumerate(zip(descriptions, variables)):
            lbl = ttk.Label(self.content_frame, text=item[0], style="Secondary.TLabel")
            lbl.grid(row=starting_row + i, column=1, padx=self.pad_x, pady=self.pad_y, sticky="W")
            self.labels[item[0]] = (lbl, item[1])

            ent_var = ttk.Entry(self.content_frame, textvariable=item[1])
            ent_var.grid(row=starting_row + i, column=2, pady=self.pad_y, sticky="W")

        return starting_row + (i + 1)

    def create_header_labels_labels(self, starting_row, header_text, descriptions, variables, header_func=None, sep=False):
        """Create a header, static labels and dynamic labels"""
        if sep is True:
            ttk.Separator(self.content_frame).grid(row=starting_row, column=0, columnspan=3,
                                                   sticky="EW", pady=10)
            starting_row += 1

        if header_func is not None:
            lbl = BLBoldClickableSecondaryLabel(self.content_frame, text=header_text)
            lbl.bind("<Button-1>", header_func)
        else:
            lbl = ttk.Label(self.content_frame, text=header_text, style="Bold.Secondary.TLabel")

        lbl.grid(row=starting_row, column=0, sticky="W", pady=self.pad_y)

        for i, item in enumerate(zip(descriptions, variables)):
            lbl = ttk.Label(self.content_frame, text=item[0], style="Secondary.TLabel")
            lbl.grid(row=starting_row + i, column=1, padx=self.pad_x, pady=self.pad_y, sticky="W")
            item[1].set("Bitte auswählen")
            self.labels[item[0]] = (lbl, item[1])

            lbl_var = ttk.Label(self.content_frame, textvariable=item[1], style="Secondary.TLabel")
            lbl_var.grid(row=starting_row + i, column=2, pady=self.pad_y, sticky="W")

        return starting_row + (i + 1)

    def create_file_picker(self, starting_row, header_text, descriptions, variables, sep=False):
        if sep is True:
            ttk.Separator(self.content_frame).grid(row=starting_row, column=0, columnspan=3,
                                                   sticky="EW", pady=10)
            starting_row += 1

        lbl = ttk.Label(self.content_frame, text=header_text, style="Bold.Secondary.TLabel")
        lbl.grid(row=starting_row, column=0, sticky="NW", pady=self.pad_y)

        for i, item in enumerate(zip(descriptions, variables)):
            lbl = ttk.Label(self.content_frame, text=item[0], style="Secondary.TLabel")
            lbl.grid(row=starting_row + i, column=1, padx=self.pad_x, pady=self.pad_y, sticky="NW")
            item[1].set("Bitte Datei auswählen")
            self.labels[item[0]] = (lbl, item[1])

            lbl_var = ttk.Label(self.content_frame, textvariable=item[1], style="Clickable.Secondary.TLabel",
                                cursor="hand2", wraplength=250)
            lbl_var.bind("<Button-1>", lambda event, variable=item[1]: self.choose_file(event, variable))
            lbl_var.grid(row=starting_row + i, column=2, pady=self.pad_y, sticky="NW")

    def choose_file(self, event, variable):
        """Ask user to pick a file that contains time tracking data"""
        variable.set(askopenfilename(initialdir=os.getcwd(), title="Dateiauswahl"))

        if variable.get() == "":
            variable.set("Bitte Datei auswählen")

        self.completeness_check()

    def clear_all(self):
        """Clears all data on the form"""
        for label_text, item in self.labels.items():
            print(label_text)
            if label_text in ["Nummer"]:
                item[1].set("")
            elif label_text in ["Datei BeginnerLuft", "Datei Coach"]:
                item[1].set("Bitte Datei auswählen")
            else:
                item[1].set("Bitte auswählen")
        self.update()
        self.update_idletasks()

