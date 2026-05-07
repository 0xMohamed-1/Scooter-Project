# register_frame.py
# Registration screen — creates a new RegisteredMember account.

import re
import tkinter as tk
from tkinter import messagebox


class RegisterFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        tk.Label(self, text="Create an Account",
                 font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(40, 25))

        form = tk.Frame(self, bg="#f0f0f0")
        form.pack()

        tk.Label(form, text="Name:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self._name_entry = tk.Entry(form, width=28, font=("Arial", 12))
        self._name_entry.grid(row=0, column=1, pady=8)

        tk.Label(form, text="Email:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self._email_entry = tk.Entry(form, width=28, font=("Arial", 12))
        self._email_entry.grid(row=1, column=1, pady=8)

        tk.Label(form, text="Password:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self._pw_entry = tk.Entry(form, width=28, font=("Arial", 12), show="*")
        self._pw_entry.grid(row=2, column=1, pady=8)


        # Error message
        self._error_label = tk.Label(self, text="", fg="red",
                                     bg="#f0f0f0", font=("Arial", 11))
        self._error_label.pack(pady=(4, 0))

        # Submit / Back buttons side by side
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=18)

        tk.Button(btn_frame, text="Submit", width=16, font=("Arial", 12),
                  command=self._on_submit).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Back", width=16, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=1, padx=10)

    def _on_submit(self):
        name     = self._name_entry.get().strip()
        email    = self._email_entry.get().strip()
        password = self._pw_entry.get()
        if not name or not email or not password:
            self._error_label.config(text="Please fill in all fields.")
            return

        # regex: requires at least one non-@ char, then @, then a domain with a dot (e.g. user@example.com)
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self._error_label.config(text="Please enter a valid email address.")
            return

        member, msg = self._system.register_user(name, email, password, "wallet")
        if member is None:
            self._error_label.config(text=msg)
            return

        messagebox.showinfo("Success", "Account created! You've received $10.00 as a welcome gift in your wallet. Please log in.")
        from gui.login_frame import LoginFrame
        self._app.show_frame(LoginFrame)

    def _go_back(self):
        from gui.login_frame import LoginFrame
        self._app.show_frame(LoginFrame)
