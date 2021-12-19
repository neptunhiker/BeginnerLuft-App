import tkinter as tk
from tkinter import ttk
from frames.boilerplate import Boilerplate
from frames.password import Password
from frames.start import Entry
from frames.windows import set_dpi_awareness
from design.colors import bl_colors
import design.fonts as bl_fonts


class BeginnerLuftApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super(BeginnerLuftApp, self).__init__(*args, **kwargs)

        self.title("BeginnerLuft APP")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))  # sets screen to full size

        # to be continued: login screen and adding current user here
        self.current_user = "Erika Musterfrau"

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
        container = ttk.Frame(self)
        container.grid(sticky="NSEW")
        container.grid_columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        starting_frame = Entry(
            parent=container,
            controller=self,
            next_screen=lambda event: self.show_frame(Password),
        )
        starting_frame.grid(row=0, column=0, sticky="NSEW")

        boilerplate_frame = Boilerplate(
            parent=container,
            controller=self,
            back_function=lambda: self.show_frame(Entry)
        )
        boilerplate_frame.grid(row=0, column=0, sticky="NSEW")

        password_frame = Password(
            parent=container,
            controller=self,
            back_function=lambda: self.show_frame(Entry)
        )
        password_frame.grid(row=0, column=0, sticky="NSEW")

        # Allow for switching between frames
        self.frames = {
            Entry: starting_frame,
            Boilerplate: boilerplate_frame,
            Password: password_frame,
        }

        self.show_frame(Entry)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def configure_styles(self):
        self["background"] = bl_colors["bg primary"]
        self.style.configure(
            "TLabel",
            font=bl_fonts.default_font,
            background=bl_colors["bg primary"],
            foreground=bl_colors["fg primary"],
        )

        self.style.configure("Title.TLabel", font=bl_fonts.bl_font_title)
        self.style.configure("Header.TLabel", font=bl_fonts.bl_font_header)
        self.style.configure("Secondary.TLabel", background=bl_colors["bg secondary"],foreground=bl_colors["fg primary"], )
        self.style.configure("Bold.Secondary.TLabel", font=bl_fonts.bl_font_bold)

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
            "Secondary.TFrame",
            background=bl_colors["bg secondary"]
        )

        self.style.configure(
            "Testing.TFrame",
            background=bl_colors["bg testing"],
        )

        self.style.configure(
            "TButton",
            background=bl_colors["bg secondary"]
        )


if __name__ == '__main__':
    app = BeginnerLuftApp()
    app.mainloop()
