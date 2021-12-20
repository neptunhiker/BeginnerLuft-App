from tkinter import ttk
import tkinter as tk

from frames.start import Entry
from frames.password import Password
from tools.helpers import hash_password, verify_password
from widgets.buttons import BLButton


class Login(ttk.Frame):
    """A login frame"""

    def __init__(self, parent, controller, next_function):
        super().__init__(parent)
        self["style"] = "Secondary.TFrame"
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.next_function = next_function
        self.controller.geometry("600x400")
        self.login_users = {}

        # NAV TOP FRAME
        nav_top_frame = ttk.Frame(self)
        nav_top_frame.grid(row=0, column=0, sticky="EW")
        nav_top_frame.columnconfigure(0, weight=1)

        header = ttk.Label(
            nav_top_frame,
            text="BeginnerLuft",
            style="Header.TLabel",
            justify="center",
            anchor="center"
        )
        header.grid(pady=10)

        # CONTENT FRAME
        self.content_frame = ttk.Frame(self, style="Secondary.TFrame")
        self.content_frame.grid(row=1, column=0, sticky="NSEW")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        self.error_text = tk.StringVar()
        self.user_selected = tk.StringVar()
        self.pw_given = tk.StringVar()
        self.ent_pw = None

        self.widgets()

        # NAV BOTTOM FRAME
        nav_bottom_frame = ttk.Frame(self, height=50)
        nav_bottom_frame.grid(row=2, column=0, sticky="NESW")
        nav_bottom_frame.rowconfigure(0, weight=1)

    def widgets(self):
        """Create labels and entry widgets"""

        frame = ttk.Frame(self.content_frame, style="Secondary.TFrame")
        frame.grid()
        frame.columnconfigure(0, weight=1)
        # frame.rowconfigure(0, weight=1)

        lbl_login = ttk.Label(frame, text="Login", style="Secondary.Header.TLabel")
        lbl_login.grid(sticky="W", pady=(10, 5))

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
        self.ent_pw.bind("<Return>", self.login_check)
        self.pw_given.trace("w", lambda a, b, c, d=self: self.on_change())

        lbl_error = ttk.Label(frame, textvariable=self.error_text, style="Secondary.Error.TLabel")
        lbl_error.grid(sticky="W")

        btn_login = BLButton(frame, text="Login -->")
        btn_login.grid(pady=(20, 10), sticky="E")
        btn_login.bind("<Button-1>", self.login_check)

        for child in frame.winfo_children():
            child.grid_configure(padx=20)

        cmb_user.focus()

    def handle_user_selection(self, event):
        print(self.user_selected.get())
        self.ent_pw.focus()  # does not seem to have an effect

    def on_change(self):
        """Remove error text when user changes the password entry field"""
        self.error_text.set("")

    def login_check(self, event):
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

            # to be continued
            # this is a workaround for a refresh function - not good, refactor!
            self.controller.frames[Password].destroy()
            new_pw_frame = Password(
                parent=self.controller.container,
                controller=self.controller,
                back_function=lambda: self.controller.show_frame(Entry)
            )
            new_pw_frame.grid(row=0, column=0, sticky="NSEW")
            self.controller.frames[Password] = new_pw_frame

            self.next_function()  # change view to next frame
            self.controller.full_screen_window()

        else:
            self.pw_given.set("")
            self.error_text.set("Falsches Passwort")
            self.ent_pw.focus_set()





