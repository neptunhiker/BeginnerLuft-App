import tkinter as tk
from tkinter import ttk

from widgets.buttons import BLButton


class Password(ttk.Frame):
    """A Frame for password settings"""

    def __init__(self, parent: ttk.Frame, controller: tk.Tk, back_function):
        super(Password, self).__init__(parent)
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
            text="Passwort ändern",
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

        # lbl = ttk.Label(
        #     self.content_frame,
        #                 text=f"Content for {self.__class__.__name__}",
        # style="Secondary.TLabel")
        # lbl.grid()

        self.widgets()

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

    def widgets(self):
        """Create entry widgets and labels"""

        frame = ttk.Frame(self.content_frame, style="Secondary.TFrame")
        frame.grid(sticky="EW")
        frame.rowconfigure((0, 1, 2, 3), weight=1)
        frame.columnconfigure((0, 1), weight=1)

        lbl_user = ttk.Label(
            frame,
            text="Benutzer:in",
            style="Secondary.TLabel"
        )
        lbl_user.grid(row=0, column=0, sticky="E", pady=20)
        lbl_user_text = ttk.Label(
            frame,
            text=self.controller.current_user,
            style="Bold.Secondary.TLabel",
        )
        lbl_user_text.grid(row=0, column=1, sticky="W")
        lbl_user_text.configure()

        lbl_old_pw = ttk.Label(
            frame,
            text="Altes Passwort",
            style="Secondary.TLabel",
        )
        lbl_old_pw.grid(row=1, column=0, sticky="E")
        ent_old_pw = ttk.Entry(
            frame,
            show="*",
        )
        ent_old_pw.grid(row=1, column=1, sticky="W")
        ent_old_pw.focus()

        lbl_new_pw = ttk.Label(
            frame,
            text="Neues Passwort",
            style="Secondary.TLabel",
        )
        lbl_new_pw.grid(row=2, column=0, sticky="E")
        ent_new_pw = ttk.Entry(
            frame,
            show="*",
        )
        ent_new_pw.grid(row=2, column=1, sticky="W")

        lbl_repeat_new_password = ttk.Label(
            frame,
            text="Neues Passwort wiederholen",
            style="Secondary.TLabel",
        )
        lbl_repeat_new_password.grid(row=3, column=0, sticky="E")
        ent_repeat_new_pw = ttk.Entry(
            frame,
            show="*",
        )
        ent_repeat_new_pw.grid(row=3, column=1, sticky="W")

        for child in frame.winfo_children():
            child.grid_configure(padx=(5, 5))

        button = BLButton(frame, text="Passwort ändern!", command=self.change_pw)
        button.grid(row=4, column=0, columnspan=2, pady=(50, 0), ipadx=40)

    def change_pw(self):
        """Change password"""
        # to be continued
        print("trying to change the password")

        # check if old password is correct

        # check if new password has been entered twice in the same way

        # update database

        # if no error with data base show success screen

        # reroute to log in screen