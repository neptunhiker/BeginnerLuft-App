import datetime
import hashlib, binascii, os
import tkinter as tk
from tkinter import ttk

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


class MessageWindow(tk.Toplevel):
    """Pops up a window with a message defined by a header and a message"""

    def __init__(self, message_header, message, bg_color="yellow", fg_color="black", width=600, height=200):
        super(MessageWindow, self).__init__()
        self.title("BeginnerLuft")
        self.geometry(f"{width}x{height}")
        self.style = ttk.Style()
        self.font = "Times New Roman"
        self.style.configure("MessageHeader.TLabel", font=(self.font, 20, "bold"), background=bg_color,
                             foreground=fg_color)
        self.style.configure("Message.TLabel", font=(self.font, 12), background=bg_color, foreground=fg_color)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        for i in range(2):
            self.frame.grid_rowconfigure(i, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        lbl_message_header = ttk.Label(self.frame, text=message_header, style="MessageHeader.TLabel", anchor=tk.CENTER,
                                       justify="center")
        lbl_message_header.grid(row=0, column=0, sticky="nsew")
        lbl_message = ttk.Label(self.frame, text=message, style="Message.TLabel", anchor=tk.CENTER, justify="center")
        lbl_message.grid(row=1, column=0, sticky="nsew")

        self.mainloop()


if __name__ == '__main__':
    stored_password= hash_password("hallo")
    print()
    verify_password(stored_password=stored_password, provided_password="hallo")
    print()