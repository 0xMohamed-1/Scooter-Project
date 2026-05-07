# admin_dashboard.py
# Main hub for a logged-in admin.

import tkinter as tk
from tkinter import messagebox


class AdminDashboardFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        tk.Label(self, text="Admin Panel",
                 font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(30, 5))
        tk.Label(self, text="Manage the fleet, stations, and maintenance.",
                 font=("Arial", 12), bg="#f0f0f0").pack(pady=(0, 25))

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack()

        buttons = [
            ("Manage Scooters",  self._manage_scooters),
            ("Manage Stations",  self._manage_stations),
            ("Set Maintenance",  self._set_maintenance),
            ("Complete Repair",  self._complete_repair),
            ("View Reports",     self._view_reports),
            ("Manage Wallets",   self._manage_wallets),
            ("Logout",           self._logout),
        ]

        for i in range(len(buttons)):
            label, command = buttons[i]
            row = i // 2
            col = i % 2
            tk.Button(btn_frame, text=label, width=22, font=("Arial", 12),
                      command=command).grid(row=row, column=col, padx=15, pady=8)

    def _manage_scooters(self):
        from gui.manage_scooters_frame import ManageScootersFrame
        self._app.show_frame(ManageScootersFrame)

    def _manage_stations(self):
        from gui.manage_stations_frame import ManageStationsFrame
        self._app.show_frame(ManageStationsFrame)

    def _set_maintenance(self):
        from gui.set_maintenance_frame import SetMaintenanceFrame
        self._app.show_frame(SetMaintenanceFrame)

    def _complete_repair(self):
        from gui.complete_repair_frame import CompleteRepairFrame
        self._app.show_frame(CompleteRepairFrame)

    def _view_reports(self):
        from gui.reports_frame import ReportsFrame
        self._app.show_frame(ReportsFrame)

    def _manage_wallets(self):
        from gui.manage_wallet_frame import ManageWalletFrame
        self._app.show_frame(ManageWalletFrame)

    def _logout(self):
        self._app.current_user = None
        from gui.login_frame import LoginFrame
        self._app.show_frame(LoginFrame)
