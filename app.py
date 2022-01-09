import logging
import tkinter as tk
from tkinter import ttk
from databases.backups import Backup
from databases.database import Database
from frames.boilerplate import Boilerplate
from frames.change_password import ChangePassword
from frames.database_operations.creating_data import AddParticipant, AddCoach, AddJobcenter, AddLanguageSkills, \
    OverviewParticipant
from frames.database_operations.reading_data import ReadParticipants, ReadCoaches, ReadJobcenter
from frames.invoice import Invoice
from frames.login import Login
from frames.time_tracking import TimeTrackingDataSelection, TimeTrackingDataPreview
from frames.windows import set_dpi_awareness
from frames import dashboard
from logging_bl.logs import BLLogger
from design.colors import bl_colors
import design.fonts as bl_fonts
from utils.helpers import MessageWindow


class BeginnerLuftApp(tk.Tk):

    def __init__(self, starting_frame=Login, *args, **kwargs):
        super(BeginnerLuftApp, self).__init__(*args, **kwargs)

        self.title("BeginnerLuft APP")
        self.full_screen_window()

        # initialize data base
        self.db = Database(database_path="../Database/test_database.db")

        # create a logging object
        self.bl_logger = BLLogger()
        self.add_logging_handlers()

        # initialize a Backup class that allows for creating backups of the database
        self.backup_machine = Backup(self.bl_logger, original_file_path=self.db.database_path)
        self.backup_machine.create_backup()

        # login tracking
        self.current_user = None
        self.logged_in = False

        # patch to picture gallery
        self.pic_gallery_path = "../Assets"

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

        add_language_skills = AddLanguageSkills(
            parent=self.container,
            controller=self,
        )
        add_language_skills.grid(row=0, column=0, sticky="NSEW")

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

        dashboard_frame = dashboard.Dashboard(
            parent=self.container,
            controller=self,
        )
        dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        database_create_dashboard_frame = dashboard.DatabaseCreateDashboard(
            parent=self.container,
            controller=self,
        )
        database_create_dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        database_read_dashboard_frame = dashboard.DatabaseReadDashboard(
            parent=self.container,
            controller=self,
        )
        database_read_dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        database_update_dashboard_frame = dashboard.DatabaseUpdateDashboard(
            parent=self.container,
            controller=self,
        )
        database_update_dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        database_delete_dashboard_frame = dashboard.DatabaseDeleteDashboard(
            parent=self.container,
            controller=self,
        )
        database_delete_dashboard_frame.grid(row=0, column=0, sticky="NSEW")

        database_operations_dashboard_frame = dashboard.DatabaseOperationsDashboard(
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
            next_function=lambda: self.show_frame(dashboard.Dashboard)
        )
        login_frame.grid(row=0, column=0, sticky="NSEW")

        overview_participant_frame = OverviewParticipant(
            parent=self.container,
            controller=self,
        )
        overview_participant_frame.grid(row=0, column=0, sticky="NSEW")

        read_coaches_frame = ReadCoaches(
            parent=self.container,
            controller=self,
        )
        read_coaches_frame.grid(row=0, column=0, sticky="NSEW")

        read_jobcenter_frame = ReadJobcenter(
            parent=self.container,
            controller=self,
        )
        read_jobcenter_frame.grid(row=0, column=0, sticky="NSEW")

        read_participant_frame = ReadParticipants(
            parent=self.container,
            controller=self,
        )
        read_participant_frame.grid(row=0, column=0, sticky="NSEW")


        tt_data_selection_frame = TimeTrackingDataSelection(
            parent=self.container,
            controller=self,
        )
        tt_data_selection_frame.grid(row=0, column=0, sticky="NSEW")

        tt_data_preview_frame = TimeTrackingDataPreview(
            parent=self.container,
            controller=self,
        )
        tt_data_preview_frame.grid(row=0, column=0, sticky="NSEW")

        # Allow for switching between frames
        self.frames = {
            AddCoach: add_coach_frame,
            AddJobcenter: add_jobcenter_frame,
            AddLanguageSkills: add_language_skills,
            AddParticipant: add_participant_frame,
            Boilerplate: boilerplate_frame,
            ChangePassword: change_pw_frame,
            dashboard.Dashboard: dashboard_frame,
            dashboard.DatabaseCreateDashboard: database_create_dashboard_frame,
            dashboard.DatabaseReadDashboard: database_read_dashboard_frame,
            dashboard.DatabaseUpdateDashboard: database_update_dashboard_frame,
            dashboard.DatabaseDeleteDashboard: database_delete_dashboard_frame,
            dashboard.DatabaseOperationsDashboard: database_operations_dashboard_frame,
            Invoice: invoice_frame,
            Login: login_frame,
            OverviewParticipant: overview_participant_frame,
            ReadCoaches: read_coaches_frame,
            ReadJobcenter: read_jobcenter_frame,
            ReadParticipants: read_participant_frame,
            TimeTrackingDataSelection: tt_data_selection_frame,
            TimeTrackingDataPreview: tt_data_preview_frame,
        }

        # starting frame
        self.starting_frame = AddParticipant
        if self.starting_frame != Login:
            self.logged_in = True  # automatic log-in for testing purposes only, remove later

        self.show_frame(self.starting_frame)

        self.menu()

    def show_frame(self, container, refresh: bool = False) -> None:
        if self.logged_in or container == Login:
            print(container)
            print(refresh)
            if refresh:
                # run a refresh method of the frame if it has one
                method = getattr(container, "refresh", None)
                if callable(method):
                    self.frames[container].refresh()

            frame = self.frames[container]
            frame.tkraise()
        else:
            MessageWindow(
                controller=self,
                message_header="Login erforderlich",
                message="Bitte einloggen, um die APP zu nutzen.",
                alert=True
            )

    def nav_to_login(self):
        self.show_frame(Login)

    def nav_to_dashboard(self):
        self.show_frame(dashboard.Dashboard)

    def nav_to_database_operations(self):
        self.show_frame(dashboard.DatabaseOperationsDashboard)


        
    def nav_to_password_change(self):
        self.frames[ChangePassword].refresh()
        self.show_frame(ChangePassword)

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
        self.style.configure("Secondary.Title.TLabel", background=bl_colors["bg secondary"],
                             foreground=bl_colors["fg primary"])
        self.style.configure("Secondary.Error.TLabel", background=bl_colors["bg secondary"],
                             foreground="red", font=bl_fonts.bl_font_error)
        self.style.configure("Secondary.Emphasize.TLabel", background=bl_colors["bg secondary"],
                             foreground="red")
        self.style.configure("Clickable.Secondary.TLabel", foreground=bl_colors["fg blue"])
        self.style.configure("Bold.Clickable.Secondary.TLabel", font=bl_fonts.bl_font_bold)
        self.style.configure("Testing.TLabel", background=bl_colors["bg testing"], foreground=bl_colors["fg testing"])

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

        self.style.configure("TEntry", )
        self.style.configure("Error.TEntry", foreground="red")

        self.style.configure(
            "TCheckbutton",
            background=bl_colors["bg secondary"]
        )

        self.style.configure("Error.TEntry", foreground="red")

    def menu(self):
        """Create a menu"""

        if self.current_user is None:
            return

        menubar = tk.Menu(self)

        # Navigation menu
        nav_menu = tk.Menu(menubar)
        nav_menu.add_command(label="Dashboard", command=self.nav_to_dashboard)
        nav_menu.add_separator()
        nav_menu.add_command(label="Datenbankoperationen", command=self.nav_to_database_operations)
        nav_menu.add_command(label="Zeiterfassung", command=lambda container=TimeTrackingDataSelection: self.show_frame(container))
        nav_menu.add_command(label="Rechnungserstellung", command=lambda container=Invoice: self.show_frame(container))
        menubar.add_cascade(label="Navigation", menu=nav_menu)

        # User menu
        user_menu = tk.Menu(menubar)
        user_menu.add_command(label="Passwort ändern", command=self.nav_to_password_change)
        user_menu.add_command(label="Logout", command=lambda reopen=False: self.logout(reopen))
        menubar.add_cascade(label=self.current_user, menu=user_menu)

        self.config(menu=menubar)

    def logout(self, reopen: bool = True):
        """Log the current user out and return to Login screen"""
        self.bl_logger.info(f"Successful logout of {self.current_user}")
        self.destroy()

        if reopen:
            # re-open the application
            self.__init__(starting_frame=Login)
            self.mainloop()

    def add_logging_handlers(self):
        """Add handlers that will allow logging functionality"""

        self.bl_logger.add_file_handler(
            log_file="../Output/Log files/BL_log.log",
            log_format="%(levelname)s: %(msg)s\n"
                       "%(filename)s - %(funcName)s - line nr %(lineno)s - %(asctime)s\n",
            level=logging.INFO,
            mode="a"
        )

        self.bl_logger.add_console_handler(
            log_format="%(levelname)s: %(msg)s\n"
                       "%(filename)s - %(funcName)s - line nr %(lineno)s - %(asctime)s - logger defined in: %(name)s\n",
            level=logging.DEBUG
        )

    def full_screen_window(self):
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))  # sets screen to full size


if __name__ == '__main__':
    app = BeginnerLuftApp()
    app.mainloop()
