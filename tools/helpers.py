import datetime
import hashlib, binascii, os
from pathlib import Path
from PIL import Image, ImageTk
import subprocess
import tkinter as tk
from tkinter import ttk
import webbrowser

from design.colors import bl_colors
from tools.custom_exceptions import DateFormatException


def format_to_german_date(date):
    """Converts a date into a German string date format"""

    if isinstance(date, datetime.date):
        month = date.month
        german_months = {1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
                         9: "September", 10: "Oktober", 11: "November", 12: "Dezember"}

        return f"{date.strftime('%d.')} {german_months[month]} {date.strftime('%Y')}"

    else:
        return f"Cannot format date {date}"


def check_if_file_exists(path_to_file):
    """Check if a file exists"""

    path = Path(path_to_file)

    return path.is_file()


def create_invoice_nr(creation_date, participant_first_name, participant_last_name):
    """Create an invoice number based on input arguments"""
    try:
        creation_date = parse_date_from_string(creation_date)
    except AttributeError as err:
        print(err)
        pass
    else:
        creation_date = creation_date.strftime("%Y-%m-%d")
    invoice_nr = f"{creation_date}-{participant_first_name[0]}{participant_last_name[0]}"

    return invoice_nr


def create_invoice_name(creation_date, participant_first_name, participant_last_name):
    """Create an invoice name based on input arguments"""

    try:
        creation_date = parse_date_from_string(creation_date)
    except Exception:
        creation_date = creation_date.strftime("%Y-%m-%d")

    if participant_first_name == "" or participant_last_name == "":
        raise AttributeError

    invoice_nr = f"{creation_date} Rechnung {participant_first_name} {participant_last_name}"

    return invoice_nr

def determine_payment_target_date(date, payment_horizon_in_days):
    """Determines a target date for payment"""

    if isinstance(date, datetime.date) and isinstance(payment_horizon_in_days, int):

        target_date = date + datetime.timedelta(days=payment_horizon_in_days)
        while target_date.weekday() in [5, 6]:
            target_date += datetime.timedelta(days=1)

        return target_date

    else:
        raise Exception


def hash_password(password):
    """Hash a password for storing"""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    pwd = (salt+pwdhash).decode('ascii')
    return pwd


def parse_date_from_string(datestring):
    """Parses dates in various formats to datetime.date object"""

    datestring = datestring.strip()  # remove leading and trailing whitespace

    try:

        return datetime.datetime.fromisoformat(datestring).date()

    except ValueError:

        if "-" in datestring:
            year, month, day = datestring.split("-")
            sep = "-"
        elif "." in datestring:
            day, month, year = datestring.split(".")
            sep = "."
        else:
            raise DateFormatException(datestring)

        if len(year) == 2:
            year_format = "%y"
        elif len(year) == 4:
            year_format = "%Y"
        else:
            raise DateFormatException

        if sep == "-":
            parsing_format = f"{year_format}{sep}%m{sep}%d"
        elif sep == ".":
            parsing_format = f"%d{sep}%m{sep}{year_format}"

        try:
            return datetime.datetime.strptime(datestring, parsing_format).date()

        except Exception as err:
            print(err)
            raise DateFormatException


def string_to_float(string):
    """Convert a string to a float"""

    try:
        return float(string)
    except ValueError:
        dot_last_occurence = string.rfind(".")
        comma_last_occurence = string.rfind(",")
        if dot_last_occurence > comma_last_occurence:
            return float(string.replace(",", ""))
        else:
            return float(string.replace(".", "X").replace(",", ".").replace("X", ""))


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by a user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    if pwdhash == stored_password:
        return True
    else:
        return False


class NewWindow(tk.Toplevel):

    def __init__(self):
        super(NewWindow, self).__init__()
        self.mainloop()


class MessageWindow(tk.Toplevel):
    """Pops up a window with a message defined by a header and a message"""

    def __init__(self, message_header, message, path_to_file=None, width=600, height=200):
        super(MessageWindow, self).__init__()
        self.title("BeginnerLuft")
        self.geometry(f"{width}x{height}")
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        # LEFT HAND SIDE
        frame_left = ttk.Frame(self)
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
        frame_right.grid(row=0, column=1, sticky="NSEW")
        frame_right.columnconfigure(0, weight=1)
        frame_right.rowconfigure((0, 1), weight=1)

        # header
        lbl_header = ttk.Label(frame_right, text=message_header, style="Secondary.Header.TLabel")
        lbl_header.grid()

        # message
        lbl_message = ttk.Label(frame_right, text=message, style="Secondary.TLabel", wraplength=180, anchor="center")
        lbl_message.grid()

        if path_to_file is not None:
            self.path_to_file = path_to_file
            lbl_message.configure(cursor="hand2")
            lbl_message.bind("<Button-1>", self.open_url)

        self.mainloop()

    def open_url(self, event):
        """Opens a file"""
        # subprocess.Popen([f"'{self.path_to_file}'"], shell=True)  # does not work
        pass

if __name__ == '__main__':
    MessageWindow(message_header="Test", message="a very long message with a lot of text and some more text"
                                                 "and even more and more and more and maybeeven some more text")