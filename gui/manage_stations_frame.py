# manage_stations_frame.py
# Admin screen to add and remove stations.

import tkinter as tk
from tkinter import messagebox
import webbrowser


class ManageStationsFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._station_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="Manage Stations", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(15, 8))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=8,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_stations()

        btn_row = tk.Frame(self, bg="#f0f0f0")
        btn_row.pack(pady=(6, 4))

        tk.Button(btn_row, text="Open in Maps", width=18, font=("Arial", 11),
                  command=self._on_open_maps).pack(side="left", padx=6)
        tk.Button(btn_row, text="Remove Selected Station", width=22, font=("Arial", 11),
                  command=self._on_remove).pack(side="left", padx=6)

        # Add new station form
        add_frame = tk.LabelFrame(self, text="  Add New Station  ",
                                  font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=6)
        add_frame.pack(fill="x", padx=30, pady=(4, 8))

        for col_idx, label in enumerate(["Name:", "Google Maps URL:", "Capacity:"]):
            tk.Label(add_frame, text=label, bg="#f0f0f0", font=("Arial", 11)).grid(
                row=col_idx, column=0, sticky="e", padx=6, pady=4)

        self._entry_name = tk.Entry(add_frame, width=36, font=("Arial", 11))
        self._entry_name.grid(row=0, column=1, pady=4, padx=(0, 10))

        self._entry_url = tk.Entry(add_frame, width=36, font=("Arial", 11))
        self._entry_url.grid(row=1, column=1, pady=4, padx=(0, 10))

        self._entry_cap = tk.Entry(add_frame, width=36, font=("Arial", 11))
        self._entry_cap.grid(row=2, column=1, pady=4, padx=(0, 10))

        tk.Button(add_frame, text="Add Station", font=("Arial", 11),
                  command=self._on_add).grid(row=3, column=0, columnspan=2, pady=6)

        tk.Button(self, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).pack(pady=6)

    def _load_stations(self):
        self._listbox.delete(0, "end")
        self._station_ids = []

        header = "{:<24} {:<10} {:<12} {}".format(
            "Name", "Capacity", "Free Slots", "Scooters")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 55)
        self._station_ids.append(None)
        self._station_ids.append(None)

        for station in self._system.get_all_stations():
            name   = station.get_name()[:22]
            cap    = str(station.get_capacity())
            free   = str(station.get_available_count())
            docked = str(len(station.get_scooter_ids()))
            self._listbox.insert("end", "{:<24} {:<10} {:<12} {}".format(
                name, cap, free, docked))
            self._station_ids.append(station.get_station_id())

    def _selected_station(self):
        selection = self._listbox.curselection()
        if not selection:
            return None, "No Selection", "Select a station first."
        station_id = self._station_ids[selection[0]]
        if station_id is None:
            return None, "Invalid Selection", "Select a station row."
        station = next(
            (s for s in self._system.get_all_stations()
             if s.get_station_id() == station_id), None
        )
        return station, None, None

    def _on_open_maps(self):
        station, err_title, err_msg = self._selected_station()
        if station is None:
            messagebox.showerror(err_title, err_msg)
            return
        url = station.get_location().get_maps_url()
        if not url:
            messagebox.showerror("No URL", "This station has no Maps URL.")
            return
        webbrowser.open(url)

    def _on_remove(self):
        station, err_title, err_msg = self._selected_station()
        if station is None:
            messagebox.showerror(err_title, err_msg)
            return
        success, msg = self._system.remove_station(station.get_station_id())
        if not success:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Removed", "Station removed.")
            self._load_stations()

    def _on_add(self):
        name    = self._entry_name.get().strip()
        url     = self._entry_url.get().strip()
        cap_str = self._entry_cap.get().strip()

        if not name or not url or not cap_str:
            messagebox.showerror("Missing Fields", "Please fill in all fields.")
            return

        try:
            cap = int(cap_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Capacity must be a whole number.")
            return

        self._system.add_station(name, url, cap)
        messagebox.showinfo("Added", "Station '{}' added.".format(name))
        self._entry_name.delete(0, "end")
        self._entry_url.delete(0, "end")
        self._entry_cap.delete(0, "end")
        self._load_stations()

    def _go_back(self):
        from gui.admin_dashboard import AdminDashboardFrame
        self._app.show_frame(AdminDashboardFrame)
