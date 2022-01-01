import datetime
import os
import pandas as pd
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Callable, List

from objects.data_picker import PickParticipant, PickTraining
from reports.time_tracking.time_tracking import TimeReport
from utils import helpers
from utils.custom_exceptions import InsufficientTimeTrackingData
from widgets.background import create_background_image
from widgets.buttons import BLImageButtonLabel
from widgets.labels import BLBoldClickableSecondaryLabel


class TimeTrackingDataSelection(ttk.Frame):
    """A frame that allows user to create a pdf for time tracking of coachings"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.parent = parent
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
        self.confirmation_period_start = tk.StringVar()
        self.confirmation_period_end = tk.StringVar()
        self.file_path_time_sheet_bl = tk.StringVar()
        self.file_path_time_sheet_coach = tk.StringVar()
        self.report = None
        self.checkbutton_list = []

        self.variables = [self.participant_title, self.participant_first_name, self.participant_last_name,
                          self.participant_jc_id, self.training_name, self.training_id,
                          self.confirmation_period_start, self.confirmation_period_end, self.file_path_time_sheet_bl,
                          self.file_path_time_sheet_coach]

        # LEFT HAND SIDE ----------------------------------------------------
        frame_left = ttk.Frame(self, style="Secondary.TFrame")
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.columnconfigure(0, weight=1)
        frame_left.rowconfigure(0, weight=1)

        create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/backgrounds/office01.jpg",
                                frame=frame_left, desired_width=1200)

        # RIGHT HAND SIDE ----------------------------------------------------
        frame_right = ttk.Frame(self, style="Secondary.TFrame")
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure((0), weight=1)

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
        self.content_frame_left = ttk.Frame(pos_frame, style="Secondary.TFrame")
        self.content_frame_left.grid(row=1, padx=10)
        # self.content_frame.columnconfigure(0, weight=1)
        self.content_frame_left.rowconfigure(0, weight=1)

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

        # FRAME navigation ----------------------------------------------------
        nav_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        nav_frame.grid(row=2, column=0, sticky="EW", padx=10)
        nav_frame.columnconfigure(0, weight=1)

        btn_data_preview = BLImageButtonLabel(
            parent=nav_frame,
            func=self.enter_data_preview_screen,
            path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/data_preview_01.png",
            path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/data_preview_02.png",
        )
        btn_data_preview.grid(pady=10)

        btn_back = BLImageButtonLabel(
            parent=nav_frame,
            func=self.back_button,
            path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
            path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png",
        )
        btn_back.grid(pady=10)

        # self.pre_populate()
        self.populate_with_test_data()

    def enter_data_preview_screen(self) -> None:
        """
        Navigate to the data preview screen

        - check completeness and correctness of data

        """
        if not self.run_all_prechecks():
            return

        # Instantiate the TimeReport
        if not self.create_time_tracking_instance():
            return

        self.controller.frames[TimeTrackingDataPreview].build_up_frame(report=self.report)
        self.controller.show_frame(TimeTrackingDataPreview)

    def run_all_prechecks(self) -> bool:
        """Run all pre checks needed to be completed for the creation of a time tracking pdf and/or data preview"""

        # completeness check
        if not self.completeness_check():
            return False
        # correctness check
        if not self.correctness_check():
            return False

        return True

    def create_time_tracking_instance(self) -> bool:
        """Create an instance of the object TimeReport"""

        try:
            self.report = TimeReport(
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

            return True

        except InsufficientTimeTrackingData as err:
            msg_logging = f"Time tracking sheet could not be created."
            self.controller.bl_logger.exception(msg_logging)
            helpers.MessageWindow(controller=self.controller,
                                  message_header="Zeiterfassung nicht erstellt!",
                                  message=f"Die Zeiterfassung konnte nicht erstellt werden, da weder eine korrekte "
                                          f"Datei für die Zeiterfassung des Coaches noch für die Zeiterfassung von "
                                          f"BeginnerLuft importiert werden konnte.",
                                  alert=True)
            return False

        except Exception as err:
            print(err)
            msg_logging = f"Time tracking sheet could not be created."
            self.controller.bl_logger.exception(msg_logging)
            helpers.MessageWindow(controller=self.controller,
                                  message_header="Zeiterfassung nicht erstellt!",
                                  message=f"Leider ist etwas schiefgegangen! Bitte Dateneingaben überprüfen. Ggf. "
                                          f"liegen die ausgewählten Dateien nicht im richtigen Format (excel) vor oder "
                                          f"die Excel-Dateien haben nicht die richtige Struktur (Anzahl der Spalten, "
                                          f"Spaltenüberschriften o.ä.)",
                                  height=300,
                                  alert=True)
            return False


    def pre_populate(self) -> None:
        """Populates the form with some data"""

        training_name = "Individuelles Berufscoaching"
        self.training_name.set(training_name)
        sql = f"SELECT * FROM Massnahmen WHERE Bezeichnung = '{training_name}'"
        training_id = self.controller.db.select_single_query(sql)["ID"]
        self.training_id.set(training_id)

    def populate_with_test_data(self) -> None:
        """Populates the form with test data"""

        self.participant_title.set("Herr")
        self.participant_first_name.set("Jimmy")
        self.participant_last_name.set("Murt")
        self.participant_jc_id.set("jcid123")
        # self.avgs_coupon_id.set("lsajfd123")
        self.training_name.set("fast ind. Coaching")
        self.training_id.set("123321")
        self.confirmation_period_start.set("22.01.1984")
        self.confirmation_period_end.set("29.03.1984")
        self.file_path_time_sheet_bl.set("../Test_data/zeiterfassung_test_bl.xlsx")
        self.file_path_time_sheet_coach.set("../Test_data/zeiterfassung_test_coach.xlsx")

    def back_button(self) -> None:
        """Navigate to the dashboard"""
        self.controller.nav_to_dashboard()

    def completeness_check(self) -> bool:
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

    def correctness_check(self) -> bool:
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

    def pick_participant_from_db(self, event: tk.Event) -> None:
        """Opens a new window that allows the user to pick a participant from the database"""
        PickParticipant(controller=self.controller, parent=self)

    def pick_training_from_db(self, event: tk.Event) -> None:
        """Opens a new window that allows the user to pick a training (Maßnahme) from the database"""
        PickTraining(controller=self.controller, parent=self)

    def create_header_labels_entries(self, starting_row: int, header_text: str, descriptions: List[str],
                                     variables: List[tk.StringVar], header_func: Callable = None,
                                     sep: bool = False) -> int:
        """Create a header, static labels and dynamic entry fields"""

        if sep is True:
            ttk.Separator(self.content_frame_left).grid(row=starting_row, column=0, columnspan=3,
                                                        sticky="EW", pady=10)
            starting_row += 1

        if header_func is not None:
            lbl = BLBoldClickableSecondaryLabel(self.content_frame_left, text=header_text)
            lbl.bind("<Button-1>", header_func)
        else:
            lbl = ttk.Label(self.content_frame_left, text=header_text, style="Bold.Secondary.TLabel")

        lbl.grid(row=starting_row, column=0, sticky="W", pady=self.pad_y)

        for i, item in enumerate(zip(descriptions, variables)):
            lbl = ttk.Label(self.content_frame_left, text=item[0], style="Secondary.TLabel")
            lbl.grid(row=starting_row + i, column=1, padx=self.pad_x, pady=self.pad_y, sticky="W")
            self.labels[item[0]] = (lbl, item[1])

            ent_var = ttk.Entry(self.content_frame_left, textvariable=item[1])
            ent_var.bind("<FocusIn>", lambda event, entry_widget=ent_var: self.focus_in(entry_widget))
            ent_var.bind("<FocusOut>", lambda event, entry_widget=ent_var: self.focus_out(entry_widget))
            ent_var.grid(row=starting_row + i, column=2, pady=self.pad_y, sticky="W")

        return starting_row + (i + 1)

    def focus_in(self, entry_widget: ttk.Entry) -> bool:
        """Clears the text when a user enters an entry widget and it still contains a specific text"""
        if entry_widget.get() == "Bitte auswählen":
            entry_widget.delete("0", tk.END)

    def focus_out(self, entry_widget: ttk.Entry) -> bool:
        """Writes a specific text into an Entry widget when the user focses out and leaves it blank"""
        if entry_widget.get() == "":
            entry_widget.insert("0", "Bitte auswählen")

    def create_header_labels_labels(self, starting_row: int, header_text: str, descriptions: List[str],
                                    variables: List[tk.StringVar], header_func: Callable = None, sep=False) -> int:
        """Create a header, static labels and dynamic labels"""
        if sep is True:
            ttk.Separator(self.content_frame_left).grid(row=starting_row, column=0, columnspan=3,
                                                        sticky="EW", pady=10)
            starting_row += 1

        if header_func is not None:
            lbl = BLBoldClickableSecondaryLabel(self.content_frame_left, text=header_text)
            lbl.bind("<Button-1>", header_func)
        else:
            lbl = ttk.Label(self.content_frame_left, text=header_text, style="Bold.Secondary.TLabel")

        lbl.grid(row=starting_row, column=0, sticky="W", pady=self.pad_y)

        for i, item in enumerate(zip(descriptions, variables)):
            lbl = ttk.Label(self.content_frame_left, text=item[0], style="Secondary.TLabel")
            lbl.grid(row=starting_row + i, column=1, padx=self.pad_x, pady=self.pad_y, sticky="W")
            item[1].set("Bitte auswählen")
            self.labels[item[0]] = (lbl, item[1])

            lbl_var = ttk.Label(self.content_frame_left, textvariable=item[1], style="Secondary.TLabel")
            lbl_var.grid(row=starting_row + i, column=2, pady=self.pad_y, sticky="W")

        return starting_row + (i + 1)

    def create_file_picker(self, starting_row: int, header_text: str, descriptions: List[str],
                           variables: List[tk.StringVar], sep=False) -> None:
        """"Create a header, labels, and labels that allow for picking files from a directory when clicked on"""
        if sep is True:
            ttk.Separator(self.content_frame_left).grid(row=starting_row, column=0, columnspan=3,
                                                        sticky="EW", pady=10)
            starting_row += 1

        lbl = ttk.Label(self.content_frame_left, text=header_text, style="Bold.Secondary.TLabel")
        lbl.grid(row=starting_row, column=0, sticky="NW", pady=self.pad_y)

        for i, item in enumerate(zip(descriptions, variables)):
            lbl = ttk.Label(self.content_frame_left, text=item[0], style="Secondary.TLabel")
            lbl.grid(row=starting_row + i, column=1, padx=self.pad_x, pady=self.pad_y, sticky="NW")
            item[1].set("Bitte Datei auswählen")
            self.labels[item[0]] = (lbl, item[1])

            lbl_var = ttk.Label(self.content_frame_left, textvariable=item[1], style="Clickable.Secondary.TLabel",
                                cursor="hand2", wraplength=250)
            lbl_var.bind("<Button-1>", lambda event, variable=item[1]: self.choose_file(event, variable))
            lbl_var.grid(row=starting_row + i, column=2, pady=self.pad_y, sticky="NW")

    def choose_file(self, event: tk.Event, variable: tk.StringVar) -> None:
        """Ask user to pick a file that contains time tracking data"""
        variable.set(askopenfilename(initialdir=os.getcwd(), title="Dateiauswahl"))

        if variable.get() == "":
            variable.set("Bitte Datei auswählen")

        self.completeness_check()

    def clear_all(self, pre_populate: bool = False) -> None:
        """Clears all data on the form"""
        for label_text, item in self.labels.items():
            if label_text in ["Nummer"]:
                item[1].set("")
            elif label_text in ["Datei BeginnerLuft", "Datei Coach"]:
                item[1].set("Bitte Datei auswählen")
            else:
                item[1].set("Bitte auswählen")

        if pre_populate:
            self.pre_populate()


class TimeTrackingDataPreview(ttk.Frame):
    """A frame that allows user to select specific months for creating a pdf for time tracking of coachings"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk) -> None:
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.report = None
        self.checkbutton_list = []

        # FRAME left
        frame_left = ttk.Frame(self)
        frame_left.grid(row=0, column=0, sticky="NSEW")
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)

        # create image on canvas
        canvas = create_background_image(path_of_image=f"{self.controller.pic_gallery_path}/"
                                                       f"backgrounds/birches_bw_01.jpg",
                                         frame=frame_left, desired_width=1800)
        canvas.columnconfigure(0, weight=1)
        canvas.rowconfigure(0, weight=1)

        container_frame = ttk.Frame(canvas, style="Secondary.TFrame")
        container_frame.grid(row=0, column=0)
        container_frame.columnconfigure(0, weight=1)

        # HEADER frame ----------------------------------------------------
        header_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        header_frame.grid(sticky="EW", padx=20, pady=20)
        header_frame.columnconfigure(0, weight=1)

        # header
        header = ttk.Label(header_frame, text="Datenvorschau", style="Secondary.Header.TLabel")
        header.grid()

        # FRAME data preview ----------------------------------------------------
        data_preview_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        data_preview_frame.grid(sticky="EW", padx=20, pady=20)
        data_preview_frame.columnconfigure(0, weight=1)

        self.txt_preview = tk.Text(data_preview_frame, width=70, height=20)
        self.txt_preview.grid(row=0, column=0)

        self.scrollbar = ttk.Scrollbar(data_preview_frame, orient="vertical", command=self.txt_preview.yview)
        self.scrollbar.grid(row=0, column=1, sticky="nws")
        self.txt_preview['yscrollcommand'] = self.scrollbar.set  # communicate back to the scrollbar

        # DATA SELECTION FRAME
        self.data_selection_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        self.data_selection_frame.grid(sticky="EW", padx=20, pady=20)
        self.data_selection_frame.columnconfigure(0, weight=1)

        # BUTTON FRAME
        self.button_frame = ttk.Frame(container_frame, style="Secondary.TFrame")
        self.button_frame.grid(sticky="EW", padx=20, pady=20)
        self.button_frame.columnconfigure(0, weight=1)

        btn_go = BLImageButtonLabel(
            parent=self.button_frame,
            func=self.create_time_tracking_pdf,
            path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/timetracking_sheet_01.png",
            path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/timetracking_sheet_02.png",
        )
        btn_go.grid(pady=10)

        btn_back = BLImageButtonLabel(
            parent=self.button_frame,
            func=self.navigate_back,
            path_to_file_01=f"{self.controller.pic_gallery_path}/buttons/back_01.png",
            path_to_file_02=f"{self.controller.pic_gallery_path}/buttons/back_02.png",
        )
        btn_back.grid(pady=10)

    def build_up_frame(self, report: TimeReport) -> None:
        """Pass data to the frame so that it can be built up"""

        self.report = report
        # Place checkbutton and fill preview window with data
        self.place_checkbuttons_and_labels(frame=self.data_selection_frame)
        self.write_to_preview_window()

    def place_checkbuttons_and_labels(self, frame) -> None:
        """Place checkbuttons on frame that allow for filtering data by months"""

        # label
        lbl = ttk.Label(frame, text="Datenauswahl", style="Bold.Secondary.TLabel")
        lbl.grid(row=0, column=0)

        self.create_checkbuttons(frame=frame)
        for i, checkbutton in enumerate(self.checkbutton_list):
            frame.grid_rowconfigure(i, weight=1)
            checkbutton.grid(row=1 + i, column=0, padx=(0, 0))
            checkbutton.var.set(1)  # turns on all checkbuttons

    def create_checkbuttons(self, frame: ttk.Frame) -> None:
        """Create checkbuttons and add them to a list of checkbuttons"""

        # output / return value
        self.checkbutton_list = []

        # get unique dates
        dates = self.report.df["Datum"].unique()
        formatted_dates = [pd.to_datetime(str(date)).strftime("%m/%Y") for date in dates]

        # keep only unique month/year combinations
        final_dates = set(formatted_dates)

        # sort those combinations
        final_parsed_dates = [datetime.datetime.strptime(date, "%m/%Y") for date in final_dates]
        final_parsed_dates.sort()
        final_formatted_dates = [date.strftime("%m/%Y") for date in final_parsed_dates]

        # create checkbuttons
        for i, date in enumerate(final_formatted_dates):
            var = tk.IntVar()
            cbtn = ttk.Checkbutton(frame, text=date, variable=var, style="TCheckbutton")
            cbtn.bind("<ButtonRelease-1>", lambda event: self.update_preview_window())
            cbtn.state(['!alternate'])  # remove alternate selected state
            cbtn.var = var  # attach variable to checkbutton
            self.checkbutton_list.append(cbtn)

    def update_preview_window(self) -> None:
        """Update the data preview based on selection of user for months to show"""

        # determine selected months
        months = []
        for btn in self.checkbutton_list:
            if (btn.instate(["selected"]) or btn.instate(["active"])) and \
                    btn.state() != ('active', 'focus', 'pressed', 'selected', 'hover'):
                months.append(btn.cget("text")[0:2])

        months = [int(month) for month in months]

        # filter dataframe and update preview window
        self.report.filter_df(months=months)
        self.write_to_preview_window()

    def write_to_preview_window(self) -> None:
        """Write data into preview window"""

        # insert dataframe content as a preview to user into text field
        self.txt_preview.delete("1.0", tk.END)
        if not self.report.filtered_df.empty:
            df = self.report.filtered_df.copy()
            df.set_index("Datum", inplace=True)
            self.txt_preview.insert(tk.END, df)
            self.txt_preview.insert(tk.END, f"\n{' ' * 26}{str(df['UE'].sum())}")  # sum of UEs at bottom of table

    def create_time_tracking_pdf(self) -> None:
        """
        Run through all steps needed to create a pdf version for time tracking

        - Ask user where to save the file
        - Create pdf report and save it on file
        """

        # Ask user where to save the file
        today = datetime.date.today().strftime("%Y-%m-%d")
        pre_filled_file_name = f"{today} Zeiterfassung {self.report.participant_first_name} " \
                               f"{self.report.participant_last_name}.pdf"
        path = asksaveasfilename(title="BeginnerLuft Zeiterfassung", initialdir="../Output/Zeiterfassung",
                                 initialfile=pre_filled_file_name, filetypes=(("pdf", "*.pdf"),))
        if path:
            self.create_and_save_pdf_report(path)


    def create_and_save_pdf_report(self, path: str) -> None:
        """Create a pdf version of the time tracking report and save it"""
        try:
            self.report.create_report(path=path)
        except Exception as err:
            print(err)
            msg_logging = f"Time tracking sheet could not be created."
            self.controller.bl_logger.exception(msg_logging)
            helpers.MessageWindow(
                controller=self.controller,
                message_header="Kein Zeiterfassungs-Sheet erstellt!",
                message=f"Leider ist etwas schiefgegangen! Bitte Dateneingaben überprüfen.",
                alert=True
            )

        else:
            full_name = f"{self.report.participant_first_name} {self.report.participant_last_name}"
            logging_msg = f"{self.controller.current_user} successfully created a time tracking report for " \
                          f"{full_name}."
            self.controller.bl_logger.info(logging_msg)
            self.navigate_back(success_message=True, participant_name=full_name, path=path)

    def navigate_back(self, success_message: bool = False, participant_name: str = "", path: str = "") -> None:
        """Navigate to the previous screen"""
        self.controller.show_frame(TimeTrackingDataSelection)

        if success_message:
            self.controller.frames[TimeTrackingDataSelection].clear_all(pre_populate=True)
            helpers.MessageWindow(
                controller=self.controller,
                message_header="Zeiterfassungs-Sheet erstellt!",
                message=f"Ein Zeiterfassungs-Sheet für {participant_name} wurde unter \n\n'{path}' \n\n erstellt.",
                height=300
            )

