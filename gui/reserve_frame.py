# reserve_frame.py
# Lets a member reserve an available scooter.

import tkinter as tk
from tkinter import messagebox
import webbrowser


class ReserveFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._scooter_ids = []   # parallel list — index matches listbox row
        self._build()

    def _build(self):
        tk.Label(self, text="Reserve a Scooter", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 5))
        tk.Label(self, text="Select an available scooter and click Reserve.",
                 font=("Arial", 11), bg="#f0f0f0").pack(pady=(0, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=12,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_scooters()

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Reserve Selected", width=20, font=("Arial", 12),
                  command=self._on_reserve).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Open Station in Maps", width=20, font=("Arial", 12),
                  command=self._on_open_maps).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Back", width=14, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=2, padx=10)

    def _load_scooters(self):
        self._listbox.delete(0, "end")
        self._scooter_ids = []

        header = "{:<10} {:<10} {:<9} {}".format("ID", "Type", "Battery", "Station")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 50)
        self._scooter_ids.append(None)   # placeholder for header rows
        self._scooter_ids.append(None)

        available = self._system.get_available_scooters()
        if not available:
            self._listbox.insert("end", "  No scooters available right now.")
            self._scooter_ids.append(None)
        else:
            for scooter in available:
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

    def _on_reserve(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a scooter from the list.")
            return

        index = selection[0]
        scooter_id = self._scooter_ids[index]
        if scooter_id is None:
            messagebox.showerror("Invalid Selection", "Please select a scooter row, not the header.")
            return

        user_id = self._app.current_user.get_user_id()
        reservation, msg = self._system.reserve_scooter(user_id, scooter_id)

        if reservation is None:
            messagebox.showerror("Reservation Failed", msg)
        else:
            messagebox.showinfo("Reserved",
                "Scooter reserved! You have 15 minutes to start your rental.")
            from gui.member_dashboard import MemberDashboardFrame
            self._app.show_frame(MemberDashboardFrame)

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
