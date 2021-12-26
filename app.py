import tkinter as tk
from tkinter import ttk
from databases.database import Database
from frames.boilerplate import Boilerplate
from frames.change_password import ChangePassword
from frames.dashboard import Dashboard, DatabaseOperationsDashboard
from frames.database_operations.adding_data import AddParticipant, AddCoach, AddJobcenter
from frames.invoice import Invoice
from frames.login import Login
from frames.password import Password
from frames.start import Entry
from frames.time_tracking import TimeTracking
from frames.windows import set_dpi_awareness
from design.colors import bl_colors
import design.fonts as bl_fonts
from tools.helpers import MessageWindow


class BeginnerLuftApp(tk.Tk):

    def __init__(self, starting_frame=Login, *args, **kwargs):
        super(BeginnerLuftApp, self).__init__(*args, **kwargs)

        self.title("BeginnerLuft APP")
        self.full_screen_window()

        # initialize data base
        self.db = Database(database_path="../Database/test_database.db")

        # login information
        self.current_user = None
        self.logged_in = False

        # starting frame
        self.starting_frame = starting_frame

        # set the style to clam to have more styling flexibility
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.configure_styles()
        set_dpi_awareness()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Available frames
        """Creates all frames available to the application"""
        # Main container frame
        self.container = ttk.Frame(self)
        self.container.grid(sticky="NSEW")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        starting_frame = Entry(
            parent=self.container,
            controller=self,
            next_screen=lambda event: self.show_frame(Dashboard),
        )
        starting_frame.grid(row=0, column=0, sticky="NSEW")

        add_coach_frame = AddCoach(
            parent=self.container,
            controller=self,
        )
        add_coach_frame.grid(row=0, column=0, sticky="NSEW")

        add_jobcenter_frame = AddJobcenter(
            parent=self.container,
            controller=self,
        )
        add_jobcenter_frame.grid(row=0, column=0, sticky="NSEW")

        add_participant_frame = AddParticipant(
            parent=self.container,
            controller=self,
        )
        add_participant_frame.grid(row=0, column=0, sticky="NSEW")

        boilerplate_frame = Boilerplate(
            parent=self.container,
            controller=self,
        )
        boilerplate_frame.grid(row=0, column=0, sticky="NSEW")

        change_pw_frame = ChangePassword(
            parent=self.container,
            controller=self,
        )
        change_pw_frame.grid(row=0, column=0, sticky="NSEW")

        dashboard_frame = Dashboard(
            parent=self.container,
            controller=self,
        )
        dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        database_operations_dashboard_frame = DatabaseOperationsDashboard(
            parent=self.container,
            controller=self,
        )
        database_operations_dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        invoice_frame = Invoice(
            parent=self.container,
            controller=self,
        )
        invoice_frame.grid(row=0, column=0, sticky="NSEW")

        login_frame = Login(
            parent=self.container,
            controller=self,
            next_function=lambda: self.show_frame(Entry)
        )
        login_frame.grid(row=0, column=0, sticky="NSEW")

        password_frame = Password(
            parent=self.container,
            controller=self,
            back_function=lambda: self.show_frame(Entry)
        )
        password_frame.grid(row=0, column=0, sticky="NSEW")

        time_tracking_frame = TimeTracking(
            parent=self.container,
            controller=self,
        )
        time_tracking_frame.grid(row=0, column=0, sticky="NSEW")

        # Allow for switching between frames
        self.frames = {
            AddCoach: add_coach_frame,
            AddJobcenter: add_jobcenter_frame,
            AddParticipant: add_participant_frame,
            Boilerplate: boilerplate_frame,
            ChangePassword: change_pw_frame,
            Dashboard: dashboard_frame,
            DatabaseOperationsDashboard: database_operations_dashboard_frame,
            Entry: starting_frame,
            Invoice: invoice_frame,
            Login: login_frame,
            Password: password_frame,
            TimeTracking: time_tracking_frame,
        }

        if self.starting_frame != Login:
            self.logged_in = True  # automatic log-in for testing purposes only, remove later

        self.show_frame(self.starting_frame)

        self.menu()

    def show_frame(self, container):
        if self.logged_in or container == Login:
            frame = self.frames[container]
            frame.tkraise()
        else:
            MessageWindow(
                message_header="Login erforderlich",
                message="Bitte einloggen, um die APP zu nutzen.",
                alert=True
            )

    def back_to_login(self):
        self.show_frame(Login)

    def back_to_dashboard(self):
        self.show_frame(Dashboard)

    def back_to_database_operations(self):
        self.show_frame(DatabaseOperationsDashboard)

    def configure_styles(self):
        self["background"] = bl_colors["bg primary"]
        self.style.configure(
            "TLabel",
            font=bl_fonts.default_font,
            background=bl_colors["bg primary"],
            foreground=bl_colors["fg primary"],
        )
        self.style.configure("Alert.TLabel", background="red")
        self.style.configure("Title.TLabel", font=bl_fonts.bl_font_title)
        self.style.configure("Header.TLabel", font=bl_fonts.bl_font_header)
        self.style.configure("Secondary.TLabel", background=bl_colors["bg secondary"],
                             foreground=bl_colors["fg primary"])
        self.style.configure("Bold.Secondary.TLabel", font=bl_fonts.bl_font_bold)
        self.style.configure("Secondary.Header.TLabel", background=bl_colors["bg secondary"],
                             foreground=bl_colors["fg primary"])
        self.style.configure("Secondary.Error.TLabel", background=bl_colors["bg secondary"],
                             foreground="red", font=bl_fonts.bl_font_error)
        self.style.configure("Secondary.Emphasize.TLabel", background=bl_colors["bg secondary"],
                             foreground="red")
        self.style.configure("Clickable.Secondary.TLabel", foreground=bl_colors["fg blue"])
        self.style.configure("Bold.Clickable.Secondary.TLabel", font=bl_fonts.bl_font_bold)
        self.style.configure(
            "Testing.TLabel",
            background=bl_colors["bg testing"],
            foreground=bl_colors["fg testing"],
        )

        self.style.configure(
            "TFrame",
            background=bl_colors["bg primary"],
        )

        self.style.configure(
            "Alert.TFrame",
            background="red",
        )

        self.style.configure(
            "Secondary.TFrame",
            background=bl_colors["bg secondary"]
        )

        self.style.configure(
            "Border.Secondary.TFrame",
            relief=tk.SOLID,
            bordercolor=bl_colors["fg primary"],
        )

        self.style.configure(
            "Grey.TFrame",
            background="#f6f4f3"
        )

        self.style.configure(
            "Testing.TFrame",
            background=bl_colors["bg testing"],
        )

        self.style.configure(
            "Testing2.TFrame",
            background="red",
        )

        self.style.configure(
            "TButton",
            background=bl_colors["bg secondary"]
        )

        self.style.configure("Error.TEntry", foreground="red")

    def menu(self):
        """Create a menu"""

        menubar = tk.Menu(self)

        # Navigation menu
        nav_menu = tk.Menu(menubar)
        nav_menu.add_command(label="Dashboard", command=self.back_to_dashboard)
        nav_menu.add_separator()
        nav_menu.add_command(label="Datenbankoperationen", command=self.back_to_database_operations)
        nav_menu.add_command(label="Zeiterfassung", command=lambda container=TimeTracking: self.show_frame(container))
        nav_menu.add_command(label="Rechnungserstellung", command=lambda container=Invoice: self.show_frame(container))

        # Settings menu
        settings_menu = tk.Menu(menubar)
        settings_menu.add_command(label="Passwort ändern", command=lambda container=ChangePassword: self.show_frame(container))
        settings_menu.add_command(label="Logout", command=self.logout)

        # cascading
        menubar.add_cascade(label="Navigation", menu=nav_menu)
        menubar.add_cascade(label="Einstellungen", menu=settings_menu)

        self.config(menu=menubar)

    def logout(self):
        """Log the current user out and return to Login screen"""
        self.destroy()
        self.__init__(starting_frame=Login)
        self.mainloop()

    def full_screen_window(self):
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))  # sets screen to full size


if __name__ == '__main__':
    app = BeginnerLuftApp()
    app.mainloop()
