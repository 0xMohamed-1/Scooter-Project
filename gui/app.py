# app.py
# Main application window.
# show_frame() destroys the current screen and replaces it with a new one.

import tkinter as tk
from system import RentalSystem


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Scooter Rental System")
        self.geometry("750x560")
        self.resizable(False, False)

        self._system = RentalSystem()
        self.current_user = None     # set on login, cleared on logout
        self._current_frame = None

        # Show the login screen first
        from gui.login_frame import LoginFrame
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class, **kwargs):
        # Tear down the current screen
        if self._current_frame is not None:
            self._current_frame.destroy()
        # Build and display the new screen
        frame = frame_class(self, self._system, **kwargs)
        frame.pack(fill="both", expand=True)
        self._current_frame = frame
