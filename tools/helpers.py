import datetime
import hashlib, binascii, os
from pathlib import Path
from PIL import Image, ImageTk
from typing import Union
import tkinter as tk
from tkinter import ttk

from tools.custom_exceptions import DateFormatException


def check_if_file_exists(path_to_file: str) -> bool:
    """Check if a file exists"""

    path = Path(path_to_file)
    return path.is_file()


def create_invoice_nr(creation_date: Union[str, datetime.datetime], participant_first_name: str,
                      participant_last_name: str) -> str:
    """Return an invoice number based on a date and participant first and last name"""

    try:
        creation_date = parse_date_from_string(creation_date)
    except AttributeError:
        creation_date = creation_date.strftime("%Y-%m-%d")

    if participant_first_name == "" or participant_last_name == "":
        raise AttributeError

    return f"{creation_date}-{participant_first_name[0]}{participant_last_name[0]}"


def create_invoice_name(creation_date: Union[str, datetime.date], participant_first_name: str,
                        participant_last_name: str) -> str:
    """Return an invoice name based on a date and first and last name of a participant"""

    try:
        creation_date = parse_date_from_string(creation_date)
    except AttributeError:
        creation_date = creation_date.strftime("%Y-%m-%d")

    if participant_first_name == "" or participant_last_name == "":
        raise AttributeError

    return f"{creation_date} Rechnung {participant_first_name} {participant_last_name}"


def determine_payment_target_date(starting_date: datetime.date, payment_horizon_in_days: int,
                                  weekend_adjustment: bool = True) -> datetime.date:
    """
    Return a target date based on a starting date and a payment horizon

    starting_date -- date at which payment horizon begins
    payment_horizon_in_days -- duration of the payment horizon
    weekend_adjustment  -- payment horizon cannot end on a weekend
    """

    target_date = starting_date + datetime.timedelta(days=payment_horizon_in_days)
    if weekend_adjustment:
        while target_date.weekday() in [5, 6]:
            target_date += datetime.timedelta(days=1)

    return target_date


def format_to_german_date(date: datetime.date) -> str:
    """Converts a date into a German string date format with long German month name"""

    month = date.month
    german_months = {1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
                     9: "September", 10: "Oktober", 11: "November", 12: "Dezember"}

    return f"{date.strftime('%d.')} {german_months[month]} {date.strftime('%Y')}"


def hash_password(password: str) -> str:
    """Convert a string to a hashed password"""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    pwd = (salt + pwdhash).decode('ascii')
    return pwd


def open_directory(path):
    """Opens the given directory"""
    # does not work
    pass


def parse_date_from_string(datestring: str) -> datetime.date:
    """Parse date in various formats to datetime.date object"""

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


def string_to_float(string: str) -> float:
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


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Return whether a stored password is equivalent to a provided password"""

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
    """A separate message window"""

    def __init__(self, message_header: str, message: str, width: int = 600, height: int = 200,
                 alert: bool = False):
        """
        Pops up a window with a header and a message

        message_header -- The header displayed at the top of the window
        message -- The message displayed underneath the header
        width -- The widht of the window (default 600)
        height -- The height of the window (default 200)
        alert -- The color of the left hand side of the window (default False = yellow; True = red)
        """

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

        if alert:
            frame_left.configure(style="Alert.TFrame")
            lbl.configure(style="Alert.TLabel")

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

        self.mainloop()


class DatabaseErrorWindow(MessageWindow):
    """Pops up a data base error window"""

    def __init__(self):
        super(DatabaseErrorWindow, self).__init__(message_header="Datenbankfehler",
                                                  message="Auf die Datenbank kann nicht zugegriffen werden.",
                                                  alert=True)


if __name__ == '__main__':
    MessageWindow(message_header="Test", message="a very long message with a lot of text and some more text"
                                                 "and even more and more and more and maybeeven some more text")
