import random
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk

from frames.start import Entry
from frames.password import Password
from tools.helpers import verify_password
from widgets.buttons import BLButton, BLImageButtonLabel


class Login(ttk.Frame):
    """A Login frame"""

    def __init__(self, parent, controller, next_function):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.next_function = next_function
        self.login_users = {}
        self.error_text = tk.StringVar()
        self.user_selected = tk.StringVar()
        self.pw_given = tk.StringVar()
        self.ent_pw = None

        # create background image
        image_path = random.choice(["people", "birches_bw_01", "birches_bw_02", "fences_bw_01"])
        image = Image.open(f"assets/{image_path}.jpg")
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

        lbl_login = ttk.Label(frame, text="Login", style="Secondary.Header.TLabel")
        lbl_login.grid(sticky="W", pady=(20, 5))

        lbl_instruction = ttk.Label(frame, text="Zum Fortfahren bitte Einloggen", style="Secondary.TLabel")
        lbl_instruction.grid(sticky="W")

        lbl_user = ttk.Label(frame, text="Benutzer:In", style="Secondary.TLabel")
        lbl_user.grid(sticky="W", pady=(30, 0))

        cmb_user = ttk.Combobox(frame, textvariable=self.user_selected)
        for employee in self.controller.db.get_employees():
            self.login_users[f"{employee.first_name} {employee.last_name}"] = employee.data_base_id
        cmb_user["values"] = [user_name for user_name in self.login_users.keys()]
        cmb_user.current(0)
        cmb_user["state"] = "readonly"
        cmb_user.bind("<<ComboboxSelected>>", self.handle_user_selection)
        cmb_user.grid()

        lbl_pw = ttk.Label(frame, text="Passwort", style="Secondary.TLabel")
        lbl_pw.grid(sticky="W", pady=(10, 0))

        self.ent_pw = ttk.Entry(frame, show="*", textvariable=self.pw_given)
        self.ent_pw.grid(sticky="EW")
        self.ent_pw.bind("<Return>", lambda event: self.login_check())
        self.pw_given.trace("w", lambda a, b, c, d=self: self.on_change())

        lbl_error = ttk.Label(frame, textvariable=self.error_text, style="Secondary.Error.TLabel")
        lbl_error.grid(sticky="W")

        btn_login = BLImageButtonLabel(frame,
                                       self.login_check,
                                       "assets/buttons/login_01.png",
                                       "assets/buttons/login_02.png")
        btn_login.grid(pady=(20, 20), sticky="E")

        for child in frame.winfo_children():
            child.grid_configure(padx=20)

        self.ent_pw.focus()

    def handle_user_selection(self, event):
        print(self.user_selected.get())
        self.ent_pw.focus()  # does not seem to have an effect

    def on_change(self):
        """Remove error text when user changes the password entry field"""
        self.error_text.set("")

    def login_check(self):
        """Check whether user can login with given information"""

        # get user from frame
        user = self.user_selected.get()
        user_database_id = self.login_users[user]

        # get target password from data base
        sql = "SELECT * FROM Passwoerter WHERE ID = ?"
        row = self.controller.db.select_single_query(query=sql, arguments=[user_database_id])
        target_pw = row["Passwort"]

        # compare passwords
        if verify_password(target_pw, self.pw_given.get()):
            print(f"login successful for {user}")
            self.controller.current_user = user
            self.controller.logged_in = True
            self.pw_given.set("")
            self.controller.menu()

            self.next_function()  # change view to next frame
            self.controller.full_screen_window()
            self.controller.bl_logger.info(f"Passed login attempt for {self.controller.current_user}.")

        else:
            self.pw_given.set("")
            self.error_text.set("Falsches Passwort")
            self.ent_pw.focus_set()
            self.controller.bl_logger.warning(f"Failed login attempt for {user}.")





