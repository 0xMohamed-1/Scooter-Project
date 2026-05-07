# browse_scooters_frame.py
# Read-only view of all scooters for members.

import tkinter as tk
from tkinter import messagebox
import webbrowser


class BrowseScootersFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._scooter_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="All Scooters", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=14,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_scooters()

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Open Station in Maps", width=22, font=("Arial", 12),
                  command=self._on_open_maps).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Back", width=14, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=1, padx=10)

    def _load_scooters(self):
        self._listbox.delete(0, "end")
        self._scooter_ids = []

        header = "{:<10} {:<10} {:<14} {:<9} {}".format(
            "ID", "Type", "Status", "Battery", "Station")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 60)
        self._scooter_ids.append(None)
        self._scooter_ids.append(None)

        scooters = self._system.get_all_scooters()
        if not scooters:
            self._listbox.insert("end", "  No scooters in the system.")
            self._scooter_ids.append(None)
        else:
            for scooter in scooters:
                sid        = scooter.get_scooter_id()[:8]
                stype      = scooter.get_type()
                status     = scooter.get_status()
                battery    = str(scooter.get_battery_level()) + "%"
                station_id = scooter.get_current_station_id()
                station_obj = self._system.get_station(station_id) if station_id else None
                station_label = station_obj.get_name() if station_obj else "on ride"
                line = "{:<10} {:<10} {:<14} {:<9} {}".format(
                    sid, stype, status, battery, station_label)
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

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
