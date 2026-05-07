# view_stations_frame.py
# Read-only view of all stations for members.

import tkinter as tk
import webbrowser


class ViewStationsFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._stations = []  # ordered list matching listbox rows (offset by 2 for header/sep)
        self._build()

    def _build(self):
        tk.Label(self, text="All Stations", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=14,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)
        self._listbox.bind("<<ListboxSelect>>", self._on_select)

        self._load_stations()

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=15)

        self._maps_btn = tk.Button(btn_frame, text="Open in Google Maps", width=22,
                                   font=("Arial", 12), state="disabled",
                                   command=self._open_maps)
        self._maps_btn.grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=1, padx=10)

    def _load_stations(self):
        self._listbox.delete(0, "end")
        self._stations = []
        header = "{:<24} {:<10} {:<12} {}".format(
            "Name", "Capacity", "Free Slots", "Scooters Docked")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 60)

        stations = self._system.get_all_stations()
        if not stations:
            self._listbox.insert("end", "  No stations in the system.")
        else:
            for station in stations:
                name  = station.get_name()[:22]
                cap   = str(station.get_capacity())
                free  = str(station.get_available_count())
                docked = str(len(station.get_scooter_ids()))
                line = "{:<24} {:<10} {:<12} {}".format(name, cap, free, docked)
                self._listbox.insert("end", line)
                self._stations.append(station)

    def _on_select(self, _event):
        selection = self._listbox.curselection()
        if not selection:
            return
        idx = selection[0] - 2  # subtract header and separator rows
        if 0 <= idx < len(self._stations):
            self._maps_btn.config(state="normal")
        else:
            self._maps_btn.config(state="disabled")

    def _open_maps(self):
        selection = self._listbox.curselection()
        if not selection:
            return
        idx = selection[0] - 2
        if 0 <= idx < len(self._stations):
            url = self._stations[idx].get_location().get_maps_url()
            webbrowser.open(url)

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
