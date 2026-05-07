# main.py
# Entry point — creates the App window and starts the event loop.

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
