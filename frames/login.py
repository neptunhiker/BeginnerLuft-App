from tkinter import ttk
import tkinter as tk

from frames.start import Entry
from frames.password import Password
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

        self.user_selected = tk.StringVar()
        self.pw_given = tk.StringVar()

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
        cmb_user["values"] = ("Beata Rozwadowska", "Lea Bergmann")
        cmb_user["state"] = "readonly"
        cmb_user.bind("<<ComboboxSelected>>", self.handle_user_selection)
        cmb_user.grid()

        lbl_pw = ttk.Label(frame, text="Passwort", style="Secondary.TLabel")
        lbl_pw.grid(sticky="W", pady=(10, 0))

        ent_pw = ttk.Entry(frame, show="*", textvariable=self.pw_given)
        ent_pw.grid(sticky="EW")

        btn_login = BLButton(frame, text="Login -->", command=self.login_check)
        btn_login.grid(pady=(20, 10), sticky="E")

        for child in frame.winfo_children():
            child.grid_configure(padx=20)

    def handle_user_selection(self, event):
        print(self.user_selected.get())

    def login_check(self):

        # get user from frame
        user = self.user_selected.get()

        # get target password from data base
        target_pw = "test"

        # hash password
        hashed_pw = self.pw_given.get() + "t"

        # compare passwords
        if target_pw == hashed_pw:
            print(f"login successful for {user}")
            self.controller.current_user = user


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
            print("Could not login")
            self.pw_given.set("")





