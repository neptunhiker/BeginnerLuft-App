import tkinter as tk
from tkinter import ttk
from frames.password import Password
from frames.start import Entry
from frames.windows import set_dpi_awareness
from design.colors import bl_colors
from design.fonts import bl_font_large


class BeginnerLuftApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        super(BeginnerLuftApp, self).__init__(*args, **kwargs)

        self.title("BeginnerLuft APP")
        self.geometry("600x400")

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

        password_frame = Password(
            parent=container,
            controller=self,
            back_function=lambda: self.show_frame(Entry)
        )
        password_frame.grid(row=0, column=0, sticky="NSEW")

        # Allow for switching between frames
        self.frames = {
            Entry: starting_frame,
            Password: password_frame
        }

        self.show_frame(Entry)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def configure_styles(self):

        self["background"] = bl_colors["bg primary"]
        self.style.configure(
            "TLabel",
            background=bl_colors["bg primary"],
            foreground=bl_colors["fg primary"],
        )

        self.style.configure(
            "Title.TLabel",
            font=bl_font_large,
        )

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
            "Testing.TFrame",
            background=bl_colors["bg testing"],
        )


if __name__ == '__main__':
    app = BeginnerLuftApp()
    app.mainloop()