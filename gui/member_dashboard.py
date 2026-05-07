# member_dashboard.py
# Main hub for a logged-in member.

import tkinter as tk
from tkinter import messagebox


class MemberDashboardFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        user = self._app.current_user

        tk.Label(self, text="Member Dashboard",
                 font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(30, 5))
        tk.Label(self, text="Welcome, " + user.get_name(),
                 font=("Arial", 13), bg="#f0f0f0").pack(pady=(0, 5))
        tk.Label(self, text="Wallet Balance: AED {:.2f}".format(user.get_wallet_balance()),
                 font=("Arial", 11), bg="#f0f0f0", fg="#2a7a2a").pack(pady=(0, 20))

        # 2-column grid of action buttons
        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack()

        buttons = [
            ("Browse Scooters",    self._browse_scooters),
            ("View Stations",      self._view_stations),
            ("Reserve Scooter",    self._reserve_scooter),
            ("Start Rental",       self._start_rental),
            ("End Active Rental",  self._end_rental),
            ("Rental History",     self._rental_history),
            ("Report Fault",       self._report_fault),
            ("Logout",             self._logout),
        ]

        for i in range(len(buttons)):
            label, command = buttons[i]
            row = i // 2
            col = i % 2
            tk.Button(btn_frame, text=label, width=22, font=("Arial", 12),
                      command=command).grid(row=row, column=col, padx=15, pady=8)

    def _browse_scooters(self):
        from gui.browse_scooters_frame import BrowseScootersFrame
        self._app.show_frame(BrowseScootersFrame)

    def _view_stations(self):
        from gui.view_stations_frame import ViewStationsFrame
        self._app.show_frame(ViewStationsFrame)

    def _reserve_scooter(self):
        from gui.reserve_frame import ReserveFrame
        self._app.show_frame(ReserveFrame)

    def _start_rental(self):
        from gui.start_rental_frame import StartRentalFrame
        self._app.show_frame(StartRentalFrame)

    def _end_rental(self):
        from gui.end_rental_frame import EndRentalFrame
        self._app.show_frame(EndRentalFrame)

    def _rental_history(self):
        from gui.history_frame import HistoryFrame
        self._app.show_frame(HistoryFrame)

    def _report_fault(self):
        from gui.report_fault_frame import ReportFaultFrame
        self._app.show_frame(ReportFaultFrame)

    def _logout(self):
        self._app.current_user = None
        from gui.login_frame import LoginFrame
        self._app.show_frame(LoginFrame)
