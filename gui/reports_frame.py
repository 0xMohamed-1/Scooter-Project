# reports_frame.py
# Admin screen showing aggregated system statistics.

import tkinter as tk


class ReportsFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        tk.Label(self, text="System Reports", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(30, 20))

        report = self._system.get_reports()

        # Display each stat as a labelled row
        stats = [
            ("Total Scooters",    str(report["total_scooters"])),
            ("Available",         str(report["available"])),
            ("In Use",            str(report["in_use"])),
            ("Reserved",          str(report["reserved"])),
            ("Under Maintenance", str(report["maintenance"])),
            ("Total Stations",    str(report["total_stations"])),
            ("Completed Rentals", str(report["completed_rentals"])),
            ("Total Revenue",     "${:.2f}".format(report["total_revenue"])),
        ]

        stats_frame = tk.Frame(self, bg="#f0f0f0")
        stats_frame.pack()

        for i in range(len(stats)):
            label_text, value_text = stats[i]
            tk.Label(stats_frame, text=label_text + ":", font=("Arial", 13),
                     bg="#f0f0f0", anchor="e", width=22).grid(
                row=i, column=0, padx=(0, 10), pady=6, sticky="e")
            tk.Label(stats_frame, text=value_text, font=("Arial", 13, "bold"),
                     bg="#f0f0f0", anchor="w", width=10).grid(
                row=i, column=1, pady=6, sticky="w")

        tk.Button(self, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).pack(pady=30)

    def _go_back(self):
        from gui.admin_dashboard import AdminDashboardFrame
        self._app.show_frame(AdminDashboardFrame)
