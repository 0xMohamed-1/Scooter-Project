# history_frame.py
# Shows a member's completed rental history.

import tkinter as tk


class HistoryFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._build()

    def _build(self):
        tk.Label(self, text="Rental History", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=14,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_history()

        tk.Button(self, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).pack(pady=15)

    def _load_history(self):
        self._listbox.delete(0, "end")

        user_id = self._app.current_user.get_user_id()
        rentals = self._system.get_rental_history(user_id)

        if not rentals:
            self._listbox.insert("end", "  No rental history yet.")
            return

        header = "{:<17} {:<10} {:<10} {}".format("Date", "Scooter", "Cost", "Status")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 55)

        for rental in rentals:
            date    = str(rental.get_start_time())[:16]
            sid     = rental.get_scooter_id()[:8]
            cost    = "${:.2f}".format(rental.get_total_cost())
            status  = rental.get_status()
            line = "{:<17} {:<10} {:<10} {}".format(date, sid, cost, status)
            self._listbox.insert("end", line)

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
