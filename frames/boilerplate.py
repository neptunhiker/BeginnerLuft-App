import random
from tkinter import ttk
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk

from design.colors import bl_colors
from frames.password import Password
from frames.start import Entry
from tools.helpers import verify_password
from widgets.buttons import BLButton


class Boilerplate(ttk.Frame):
    """A boilerplate frame"""

    def __init__(self, parent, controller, back_function):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)

        # NAV TOP FRAME
        nav_top_frame = ttk.Frame(self)
        nav_top_frame.grid(row=0, column=0, sticky="EW")
        nav_top_frame.columnconfigure(0, weight=1)

        header = ttk.Label(
            nav_top_frame,
            text=f"{self.__class__.__name__}",
            style="Header.TLabel",
            justify="center",
            anchor="center"
        )
        header.grid(pady=10)

        # CONTENT FRAME
        content_frame = ttk.Frame(self, style="Secondary.TFrame")
        content_frame.grid(row=1, column=0, sticky="NSEW")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)

        lbl = ttk.Label(
            content_frame,
            text=f"Content for {self.__class__.__name__}",
            style="Secondary.TLabel")
        lbl.grid()

        # NAV BOTTOM FRAME
        nav_bottom_frame = ttk.Frame(self)
        nav_bottom_frame.grid(row=2, column=0, sticky="NESW")
        nav_bottom_frame.rowconfigure(0, weight=1)

        back_button = BLButton(
            nav_bottom_frame,
            text="<< zurück",
            command=back_function,
        )
        back_button.grid(sticky="SW", pady=10)


class OneHalfFrame(ttk.Frame):
    """A test frame for a frame with a picture on the left hand side"""

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
        frame_right.rowconfigure((0, 1, 2), weight=1)

        # header frame
        header_frame = ttk.Frame(frame_right, style="Testing.TFrame")
        header_frame.grid(sticky="EW", padx=20)
        header_frame.columnconfigure(0, weight=1)

        lbl_test = ttk.Label(
            header_frame,
            text="Rechnungserstellung - Datenübersicht",
            style="Secondary.Header.TLabel",
            anchor="center",
        )
        lbl_test.grid(sticky="EW")

        # data frame
        data_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        data_frame.grid(padx=20)

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
            frame=data_frame,
            title="Teilnehmerdaten",
            label_texts=lbl_texts,
            string_variables=string_variables,
        )

        # invoice data
        sep = ttk.Separator(data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Rechnungsbetrag (brutto)", "Rechnungsnummer", "Name der Rechnungsdatei", "Rechnungsdatum",
                     "Zahlungsziel"]
        self.invoice_amount_gross = tk.StringVar()
        self.invoice_nr = tk.StringVar()
        self.invoice_name = tk.StringVar()
        self.invoice_creation_date = tk.StringVar()
        self.invoice_target_date = tk.StringVar()
        string_variables = [self.invoice_amount_gross, self.invoice_nr, self.invoice_name, self.invoice_creation_date,
                            self.invoice_target_date]
        next_row = self.create_widgets(
            frame=data_frame,
            title="Rechnungsdaten",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
        )

        # coaching data
        sep = ttk.Separator(data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Maßnahme", "Coaching-Beginn", "Coaching-Ende", "Anzahl Unterrichtseinheiten"]
        self.training_name = tk.StringVar()
        self.training_start = tk.StringVar()
        self.training_end = tk.StringVar()
        self.training_nr_training_lesseons = tk.StringVar()

        string_variables = [self.training_name, self.training_start, self.training_end,
                            self.training_nr_training_lesseons]
        next_row = self.create_widgets(
            frame=data_frame,
            title="Coaching-Daten",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
        )

        # job center data
        sep = ttk.Separator(data_frame)
        sep.grid(row=next_row, column=0, columnspan=3, sticky="EW", pady=sep_pad_y)
        lbl_texts = ["Name des Jobcenters", "Straße und Nr", "PLZ und Ort"]
        self.jc_name = tk.StringVar()
        self.jc_street_and_nr = tk.StringVar()
        self.jc_zip_and_city = tk.StringVar()
        string_variables = [self.jc_name, self.jc_street_and_nr, self.jc_zip_and_city]
        next_row = self.create_widgets(
            frame=data_frame,
            title="Jobcenter",
            label_texts=lbl_texts,
            string_variables=string_variables,
            starting_row=next_row + 1,
        )

        # Go button
        button_frame = ttk.Frame(frame_right, style="Secondary.TFrame")
        button_frame.grid(row=2, column=0, sticky="EW")
        button_frame.columnconfigure(0, weight=1)
        btn = BLButton(button_frame, text="Rechnung erstellen!")
        btn.grid()
        btn.bind("<Button-1>", self.create_invoice)

    def create_widgets(self, frame, title, label_texts, string_variables, starting_row=0):
        """Create title, label, and entry widgets"""

        pad_y = 5

        lbl_header = ttk.Label(
            frame,
            text=title,
            style="Bold.Secondary.TLabel"
        )
        lbl_header.grid(column=0, row=starting_row, sticky="W", padx=(0, 30))

        row_counter = starting_row
        for lbl_text, string_variable in zip(label_texts, string_variables):
            lbl = ttk.Label(frame, text=lbl_text, style="Secondary.TLabel")
            lbl.grid(row=row_counter, column=1, sticky="W", pady=pad_y, padx=(0,10))
            ttk.Entry(frame, textvariable=string_variable).grid(row=row_counter, column=2,
                                                                sticky="W", pady=pad_y)
            row_counter += 1

        return row_counter


    def create_invoice(self, event):
        """Creates a PDF invoice and saves it on file"""

        # collect relevant data


        # check that all necessary data are availble


        # if necessary data not available show error message

        
        # else create pdf invoice and save on file

        tk.filedialog.asksaveasfile()
