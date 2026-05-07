# start_rental_frame.py
# Lets a member start a rental from an existing reservation or by direct unlock.

import tkinter as tk
from tkinter import messagebox
import webbrowser


class StartRentalFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._scooter_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="Start a Rental", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 10))

        user_id = self._app.current_user.get_user_id()
        self._reservation = self._system.get_active_reservation_for_user(user_id)

        # --- Section 1: From reservation ---
        res_frame = tk.LabelFrame(self, text="  Your Active Reservation  ",
                                  font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=8)
        res_frame.pack(fill="x", padx=30, pady=(0, 10))

        if self._reservation:
            scooter_id = self._reservation.get_scooter_id()
            scooter = self._system.get_scooter(scooter_id)
            info = "Scooter: {} ({})  |  Expires: {}".format(
                scooter_id[:8],
                scooter.get_type() if scooter else "?",
                str(self._reservation.get_expires_at())[:16]
            )
            tk.Label(res_frame, text=info, font=("Arial", 11), bg="#f0f0f0").pack(anchor="w")
            tk.Button(res_frame, text="Start from Reservation", width=22, font=("Arial", 11),
                      command=self._start_from_reservation).pack(pady=(6, 0))
        else:
            tk.Label(res_frame, text="You have no active reservation.",
                     font=("Arial", 11), fg="gray", bg="#f0f0f0").pack(anchor="w")

        # --- Section 2: Direct unlock ---
        unlock_frame = tk.LabelFrame(self, text="  Direct Unlock (no reservation)  ",
                                     font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=8)
        unlock_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

        tk.Label(unlock_frame, text="Select an available scooter:",
                 font=("Arial", 11), bg="#f0f0f0").pack(anchor="w")

        list_frame = tk.Frame(unlock_frame, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=7,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_available_scooters()

        btn_row = tk.Frame(unlock_frame, bg="#f0f0f0")
        btn_row.pack(pady=(6, 0))
        tk.Button(btn_row, text="Direct Unlock", width=18, font=("Arial", 11),
                  command=self._direct_unlock).pack(side="left", padx=6)
        tk.Button(btn_row, text="Open Station in Maps", width=20, font=("Arial", 11),
                  command=self._on_open_maps).pack(side="left", padx=6)

        tk.Button(self, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).pack(pady=10)

    def _load_available_scooters(self):
        self._listbox.delete(0, "end")
        self._scooter_ids = []

        header = "{:<10} {:<10} {:<9} {}".format("ID", "Type", "Battery", "Station")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 46)
        self._scooter_ids.append(None)
        self._scooter_ids.append(None)

        for scooter in self._system.get_available_scooters():
            sid     = scooter.get_scooter_id()[:8]
            stype   = scooter.get_type()
            battery = str(scooter.get_battery_level()) + "%"
            station_id = scooter.get_current_station_id()
            station_obj = self._system.get_station(station_id) if station_id else None
            station_label = station_obj.get_name() if station_obj else "-"
            line = "{:<10} {:<10} {:<9} {}".format(sid, stype, battery, station_label)
            self._listbox.insert("end", line)
            self._scooter_ids.append(scooter.get_scooter_id())

    def _on_open_maps(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Select a scooter first.")
            return
        scooter_id = self._scooter_ids[selection[0]]
        if scooter_id is None:
            messagebox.showerror("Invalid Selection", "Select a scooter row.")
            return
        scooter = self._system.get_scooter(scooter_id)
        station_id = scooter.get_current_station_id() if scooter else None
        station = self._system.get_station(station_id) if station_id else None
        if not station:
            messagebox.showerror("No Station", "This scooter is not at a station.")
            return
        url = station.get_location().get_maps_url()
        if not url:
            messagebox.showerror("No URL", "This station has no Maps URL.")
            return
        webbrowser.open(url)

    def _start_from_reservation(self):
        res = self._reservation
        scooter_id = res.get_scooter_id()
        scooter = self._system.get_scooter(scooter_id)
        start_station_id = scooter.get_current_station_id() if scooter else None

        user_id = self._app.current_user.get_user_id()
        rental, msg = self._system.start_rental(
            user_id, scooter_id, start_station_id, reservation_id=res.get_reservation_id()
        )
        if rental is None:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Rental Started", "Your rental has started. Enjoy your ride!")
            from gui.member_dashboard import MemberDashboardFrame
            self._app.show_frame(MemberDashboardFrame)

    def _direct_unlock(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a scooter.")
            return

        index = selection[0]
        scooter_id = self._scooter_ids[index]
        if scooter_id is None:
            messagebox.showerror("Invalid Selection", "Please select a scooter row.")
            return

        scooter = self._system.get_scooter(scooter_id)
        start_station_id = scooter.get_current_station_id()
        user_id = self._app.current_user.get_user_id()

        rental, msg = self._system.start_rental(user_id, scooter_id, start_station_id)
        if rental is None:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Rental Started", "Your rental has started. Enjoy your ride!")
            from gui.member_dashboard import MemberDashboardFrame
            self._app.show_frame(MemberDashboardFrame)

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
