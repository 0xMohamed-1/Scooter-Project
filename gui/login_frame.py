# login_frame.py
# First screen shown when the app starts.

import tkinter as tk
from tkinter import messagebox


class LoginFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        tk.Label(self, text="Scooter Rental System",
                 font=("Arial", 22, "bold"), bg="#f0f0f0").pack(pady=(50, 30))

        # Form — label and entry pairs aligned with grid
        form = tk.Frame(self, bg="#f0f0f0")
        form.pack()

        tk.Label(form, text="Email:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=8)
        self._email_entry = tk.Entry(form, width=28, font=("Arial", 12))
        self._email_entry.grid(row=0, column=1, pady=8)

        tk.Label(form, text="Password:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self._pw_entry = tk.Entry(form, width=28, font=("Arial", 12), show="*")
        self._pw_entry.grid(row=1, column=1, pady=8)

        # Error message — only shown when login fails
        self._error_label = tk.Label(self, text="", fg="red",
                                     bg="#f0f0f0", font=("Arial", 11))
        self._error_label.pack(pady=(4, 0))

        # Buttons
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=18)

        tk.Button(btn_frame, text="Login", width=22, font=("Arial", 12),
                  command=self._on_login).pack(pady=5)
        tk.Button(btn_frame, text="Register", width=22, font=("Arial", 12),
                  command=self._go_to_register).pack(pady=5)
        tk.Button(btn_frame, text="Continue as Guest", width=22, font=("Arial", 12),
                  command=self._go_to_guest).pack(pady=5)

    def _on_login(self):
        email    = self._email_entry.get().strip()
        password = self._pw_entry.get()

        if not email or not password:
            self._error_label.config(text="Please enter your email and password.")
            return

        user, msg = self._system.login(email, password)
        if user is None:
            self._error_label.config(text=msg)
            return

        self._app.current_user = user

        # Route to the right dashboard based on role
        if user.get_role() == "admin":
            from gui.admin_dashboard import AdminDashboardFrame
            self._app.show_frame(AdminDashboardFrame)
        else:
            from gui.member_dashboard import MemberDashboardFrame
            self._app.show_frame(MemberDashboardFrame)

    def _go_to_register(self):
        from gui.register_frame import RegisterFrame
        self._app.show_frame(RegisterFrame)

    def _go_to_guest(self):
        self._app.current_user = None
        from gui.guest_dashboard import GuestDashboardFrame
        self._app.show_frame(GuestDashboardFrame)
