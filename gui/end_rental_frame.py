# end_rental_frame.py
# Lets a member end their active rental and choose a return station.

import tkinter as tk
from tkinter import messagebox


class EndRentalFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._station_ids = []   # parallel to the station dropdown options
        self._build()

    def _build(self):
        tk.Label(self, text="End Active Rental", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(30, 15))

        user_id = self._app.current_user.get_user_id()
        self._rental = self._system.get_active_rental_for_user(user_id)

        if self._rental is None:
            # No active rental — just show a message and go back
            tk.Label(self, text="You have no active rental at the moment.",
                     font=("Arial", 13), bg="#f0f0f0").pack(pady=20)
            tk.Button(self, text="Back", width=18, font=("Arial", 12),
                      command=self._go_back).pack(pady=10)
            return

        # Show rental details
        scooter = self._system.get_scooter(self._rental.get_scooter_id())
        info_frame = tk.Frame(self, bg="#f0f0f0")
        info_frame.pack(pady=(0, 20))

        tk.Label(info_frame,
                 text="Scooter: {} ({})".format(
                     self._rental.get_scooter_id()[:8],
                     scooter.get_type() if scooter else "?"),
                 font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        tk.Label(info_frame,
                 text="Started: {}".format(str(self._rental.get_start_time())[:16]),
                 font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        tk.Label(info_frame,
                 text="Rate: ${}/min".format(
                     scooter.cost_per_minute() if scooter else "?"),
                 font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")

        # Station selection
        form = tk.Frame(self, bg="#f0f0f0")
        form.pack(pady=10)

        tk.Label(form, text="Return to station:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10, pady=8)

        self._station_var = tk.StringVar()
        station_names = self._build_station_list()
        if station_names:
            self._station_var.set(station_names[0])
        dropdown = tk.OptionMenu(form, self._station_var, *station_names)
        dropdown.config(font=("Arial", 12), width=22)
        dropdown.grid(row=0, column=1, pady=8)


        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="End Rental", width=18, font=("Arial", 12),
                  command=self._on_end).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Back", width=14, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=1, padx=10)

    def _build_station_list(self):
        # Build a list of station names that still have capacity
        self._station_ids = []
        names = []
        for station in self._system.get_all_stations():
            if not station.is_full():
                names.append(station.get_name())
                self._station_ids.append(station.get_station_id())
        return names

    def _on_end(self):
        selected_name = self._station_var.get()
        # Find the station_id that matches the selected name
        end_station_id = None
        for station in self._system.get_all_stations():
            if station.get_name() == selected_name:
                end_station_id = station.get_station_id()
                break

        if end_station_id is None:
            messagebox.showerror("Error", "Please select a valid return station.")
            return

        rental_id = self._rental.get_rental_id()

        success, msg = self._system.end_rental(rental_id, end_station_id, "wallet")
        if not success:
            messagebox.showerror("Error", msg)
        else:
            cost = self._rental.get_total_cost()
            messagebox.showinfo("Rental Ended",
                "Rental ended.\nTotal cost: ${:.2f}\nThank you!".format(cost))
            from gui.member_dashboard import MemberDashboardFrame
            self._app.show_frame(MemberDashboardFrame)

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
