# guest_dashboard.py
# Read-only view for unregistered guests.
# Shows all scooters and stations; offers Register and Logout buttons.

import tkinter as tk
from tkinter import ttk


class GuestDashboardFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        tk.Label(self, text="Welcome, Guest",
                 font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=(20, 5))
        tk.Label(self, text="Browse our scooters and stations below.",
                 font=("Arial", 11), bg="#f0f0f0").pack(pady=(0, 10))

        # Split into two side-by-side panels
        panels = tk.Frame(self, bg="#f0f0f0")
        panels.pack(fill="both", expand=True, padx=20)

        # --- Left panel: Scooters ---
        left = tk.Frame(panels, bg="#f0f0f0")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left, text="Scooters", font=("Arial", 13, "bold"),
                 bg="#f0f0f0").pack(anchor="w")

        scooter_cols = ("Type", "Status", "Battery")
        self._scooter_tree = ttk.Treeview(left, columns=scooter_cols,
                                          show="headings", height=10)
        for col in scooter_cols:
            self._scooter_tree.heading(col, text=col)
            self._scooter_tree.column(col, width=90, anchor="center")
        self._scooter_tree.pack(fill="both", expand=True)

        # --- Right panel: Stations ---
        right = tk.Frame(panels, bg="#f0f0f0")
        right.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(right, text="Stations", font=("Arial", 13, "bold"),
                 bg="#f0f0f0").pack(anchor="w")

        station_cols = ("Name", "Capacity", "Free Slots")
        self._station_tree = ttk.Treeview(right, columns=station_cols,
                                          show="headings", height=10)
        for col in station_cols:
            self._station_tree.heading(col, text=col)
            self._station_tree.column(col, width=100, anchor="center")
        self._station_tree.pack(fill="both", expand=True)

        # Populate both tables
        self._load_scooters()
        self._load_stations()

        # Bottom buttons
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Register", width=18, font=("Arial", 12),
                  command=self._go_to_register).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Logout", width=18, font=("Arial", 12),
                  command=self._logout).grid(row=0, column=1, padx=10)

    def _load_scooters(self):
        # Clear existing rows then re-insert from system
        for row in self._scooter_tree.get_children():
            self._scooter_tree.delete(row)

        for scooter in self._system.get_all_scooters():
            scooter_type = scooter.get_type()
            status       = scooter.get_status()
            battery      = str(scooter.get_battery_level()) + "%"
            self._scooter_tree.insert("", "end", values=(scooter_type, status, battery))

    def _load_stations(self):
        for row in self._station_tree.get_children():
            self._station_tree.delete(row)

        for station in self._system.get_all_stations():
            name      = station.get_name()
            capacity  = station.get_capacity()
            free      = station.get_available_count()
            self._station_tree.insert("", "end", values=(name, capacity, free))

    def _go_to_register(self):
        from gui.register_frame import RegisterFrame
        self._app.show_frame(RegisterFrame)

    def _logout(self):
        self._app.current_user = None
        from gui.login_frame import LoginFrame
        self._app.show_frame(LoginFrame)
