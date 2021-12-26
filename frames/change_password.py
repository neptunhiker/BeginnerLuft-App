from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from frames.start import Entry
from frames.password import Password
from tools.helpers import verify_password, MessageWindow, hash_password, password_min_requirements
from widgets.buttons import BLButton, BLImageButtonLabel


class ChangePassword(ttk.Frame):
    """A frame to change the password"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.login_users = {}
        self.error_text = tk.StringVar()
        self.user_selected = tk.StringVar()
        self.old_pw = tk.StringVar()
        self.ent_pw = None
        self.new_pw = tk.StringVar()
        self.ent_new_pw = None
        self.new_pw_repeat = tk.StringVar()
        self.ent_new_pw_repeat = None

        # create background image
        image = Image.open("assets/people.jpg")
        desired_width = 1800
        ratio = image.height / image.width
        calculated_height = int(desired_width * ratio)
        image = image.resize((desired_width, calculated_height), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(image)

        # create canvas
        canvas = tk.Canvas(self)
        canvas.grid(row=0, column=0, sticky="NSEW")

        # set image in canvas
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image

        self.container = ttk.Frame(self, style="Secondary.TFrame")
        self.container.grid(row=0, column=0)
        self.container.columnconfigure((0, 1), weight=1)

        self.widgets()

    def widgets(self):
        """Create labels and entry widgets"""

        # LEFT-HAND FRAME
        logo_frame = ttk.Frame(self.container, style="Secondary.TFrame")
        logo_frame.grid(row=0, column=0)

        logo = Image.open("assets/bl_logo.png")
        desired_width = 180
        ratio = logo.height / logo.width
        calculated_height = int(desired_width * ratio)
        logo = logo.resize((desired_width, calculated_height), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(logo)

        lbl = ttk.Label(logo_frame, image=logo_image, style="Secondary.TLabel")
        lbl.image = logo_image
        lbl.grid(sticky="EW", padx=20)

        # RIGHT-HAND FRAME
        frame = ttk.Frame(self.container, style="Secondary.TFrame")
        frame.grid(row=0, column=1)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        lbl_login = ttk.Label(frame, text="Passwort ändern", style="Secondary.Header.TLabel")
        lbl_login.grid(sticky="W", pady=(20, 5))

        lbl_user = ttk.Label(frame, text="Benutzer:In", style="Bold.Secondary.TLabel")
        lbl_user.grid(sticky="W", pady=(30, 0))

        lbl_logged_in_user = ttk.Label(frame, textvariable=self.user_selected, style="Secondary.TLabel")
        for employee in self.controller.db.get_employees():
            self.login_users[f"{employee.first_name} {employee.last_name}"] = employee.data_base_id
        self.user_selected.set(self.controller.current_user)
        lbl_logged_in_user.grid(sticky="W")

        lbl_pw = ttk.Label(frame, text="Altes Passwort", style="Secondary.TLabel")
        lbl_pw.grid(sticky="W", pady=(10, 0))

        self.ent_pw = ttk.Entry(frame, show="*", textvariable=self.old_pw)
        self.ent_pw.grid(sticky="EW")
        self.old_pw.trace("w", lambda a, b, c, d=self: self.on_change())

        lbl_pw_new = ttk.Label(frame, text="Neues Passwort", style="Secondary.TLabel")
        lbl_pw_new.grid(sticky="W", pady=(10, 0))

        self.ent_new_pw = ttk.Entry(frame, show="*", textvariable=self.new_pw)
        self.ent_new_pw.grid(sticky="EW")
        self.new_pw.trace("w", lambda a, b, c, d=self: self.on_change())

        lbl_pw_new_repeat = ttk.Label(frame, text="Neues Passwort wiederholen", style="Secondary.TLabel")
        lbl_pw_new_repeat.grid(sticky="W", pady=(10, 0))

        self.ent_new_pw_repeat = ttk.Entry(frame, show="*", textvariable=self.new_pw_repeat)
        self.ent_new_pw_repeat.grid(sticky="EW")
        self.new_pw_repeat.trace("w", lambda a, b, c, d=self: self.on_change())

        lbl_error = ttk.Label(frame, textvariable=self.error_text, style="Secondary.Error.TLabel")
        lbl_error.grid(sticky="W")

        btn_change_pw = BLImageButtonLabel(frame,
                                           self.change_pw,
                                           "assets/buttons/change_pw_01.png",
                                           "assets/buttons/change_pw_02.png")
        btn_change_pw.grid(pady=(20, 20), sticky="E")

        for child in frame.winfo_children():
            child.grid_configure(padx=20)

        self.bind("<Enter>", lambda event: self.change_pw())
        self.ent_pw.focus()

    def handle_user_selection(self, event):
        print(self.user_selected.get())
        self.ent_pw.focus()  # does not seem to have an effect

    def on_change(self):
        """Remove error text when user changes the password entry field"""
        self.error_text.set("")

    def refresh(self):
        """Refreshes the frame to allow for the current user to be displayed correctly"""
        self.user_selected.set(self.controller.current_user)

    def change_pw(self):
        """Check whether user can login with given information"""

        # get user from frame
        user = self.user_selected.get()
        user_database_id = self.login_users[user]

        # get target password from data base
        sql = "SELECT * FROM Passwoerter WHERE ID = ?"
        row = self.controller.db.select_single_query(query=sql, arguments=[user_database_id])
        target_pw = row["Passwort"]

        # compare passwords
        if verify_password(target_pw, self.old_pw.get()):

            if self.new_pw.get() != self.new_pw_repeat.get():
                self.error_text.set("Neues Passwort bitte korrekt wiederholen.")
                return

            if not password_min_requirements(self.new_pw.get()):
                self.error_text.set("Passwort erfüllt nicht die Mindestvoraussetzungen.")
                return

            # hash password
            hashed_pw = hash_password(password=self.new_pw.get())

            # change password
            self.controller.db.update_password(user_id=user_database_id, password=hashed_pw)
            self.controller.logout()

        else:
            if self.old_pw.get() != "":
                self.old_pw.set("")
                self.error_text.set("Falsches Passwort")
                self.ent_pw.focus_set()

    def clear_all(self):
        self.old_pw.set("")
        self.new_pw.set("")
        self.new_pw_repeat.set("")
