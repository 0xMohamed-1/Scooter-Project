# manage_scooters_frame.py
# Admin screen to add and remove scooters.

import tkinter as tk
from tkinter import messagebox


class ManageScootersFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._scooter_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="Manage Scooters", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(15, 8))

        # Scooter list
        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 10), height=8,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_scooters()

        tk.Button(self, text="Remove Selected Scooter", width=24, font=("Arial", 11),
                  command=self._on_remove).pack(pady=(6, 4))

        # Add new scooter form
        add_frame = tk.LabelFrame(self, text="  Add New Scooter  ",
                                  font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=6)
        add_frame.pack(fill="x", padx=30, pady=(4, 8))

        tk.Label(add_frame, text="Type:", bg="#f0f0f0", font=("Arial", 11)).grid(
            row=0, column=0, sticky="e", padx=6, pady=4)
        self._type_var = tk.StringVar(value="standard")
        tk.OptionMenu(add_frame, self._type_var, "standard", "premium").grid(
            row=0, column=1, sticky="w", pady=4)

        tk.Label(add_frame, text="Battery (0-100):", bg="#f0f0f0", font=("Arial", 11)).grid(
            row=0, column=2, sticky="e", padx=6, pady=4)
        self._battery_entry = tk.Entry(add_frame, width=6, font=("Arial", 11))
        self._battery_entry.insert(0, "100")
        self._battery_entry.grid(row=0, column=3, pady=4)

        tk.Label(add_frame, text="Station:", bg="#f0f0f0", font=("Arial", 11)).grid(
            row=1, column=0, sticky="e", padx=6, pady=4)
        self._station_var = tk.StringVar()
        self._station_menu = tk.OptionMenu(add_frame, self._station_var, "")
        self._station_menu.config(width=18, font=("Arial", 11))
        self._station_menu.grid(row=1, column=1, columnspan=2, sticky="w", pady=4)
        self._refresh_station_menu()

        tk.Button(add_frame, text="Add Scooter", font=("Arial", 11),
                  command=self._on_add).grid(row=1, column=3, padx=6, pady=4)

        tk.Button(self, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).pack(pady=6)

    def _load_scooters(self):
        self._listbox.delete(0, "end")
        self._scooter_ids = []

        header = "{:<10} {:<10} {:<14} {:<9} {}".format(
            "ID", "Type", "Status", "Battery", "Station")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 60)
        self._scooter_ids.append(None)
        self._scooter_ids.append(None)

        for scooter in self._system.get_all_scooters():
            sid     = scooter.get_scooter_id()[:8]
            stype   = scooter.get_type()
            status  = scooter.get_status()
            battery = str(scooter.get_battery_level()) + "%"
            station_id = scooter.get_current_station_id()
            station_obj = self._system.get_station(station_id) if station_id else None
            station_label = station_obj.get_name() if station_obj else "out/maint."
            line = "{:<10} {:<10} {:<14} {:<9} {}".format(
                sid, stype, status, battery, station_label)
            self._listbox.insert("end", line)
            self._scooter_ids.append(scooter.get_scooter_id())

    def _refresh_station_menu(self):
        # Rebuild station dropdown from current stations
        menu = self._station_menu["menu"]
        menu.delete(0, "end")
        self._station_name_to_id = {}
        for station in self._system.get_all_stations():
            name = station.get_name()
            self._station_name_to_id[name] = station.get_station_id()
            menu.add_command(label=name, command=lambda n=name: self._station_var.set(n))
        stations = self._system.get_all_stations()
        if stations:
            self._station_var.set(stations[0].get_name())
        else:
            self._station_var.set("")

    def _on_remove(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Select a scooter to remove.")
            return
        scooter_id = self._scooter_ids[selection[0]]
        if scooter_id is None:
            messagebox.showerror("Invalid Selection", "Select a scooter row.")
            return
        success, msg = self._system.remove_scooter(scooter_id)
        if not success:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Removed", "Scooter removed.")
            self._load_scooters()

    def _on_add(self):
        scooter_type = self._type_var.get()
        battery_str  = self._battery_entry.get().strip()
        station_name = self._station_var.get()

        if not battery_str.isdigit() or not (0 <= int(battery_str) <= 100):
            messagebox.showerror("Invalid Input", "Battery must be a number between 0 and 100.")
            return

        station_id = self._station_name_to_id.get(station_name)
        if not station_id:
            messagebox.showerror("No Station", "Please select a valid station.")
            return

        scooter, msg = self._system.add_scooter(scooter_type, int(battery_str), station_id)
        if scooter is None:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Added", "Scooter added successfully.")
            self._load_scooters()
            self._refresh_station_menu()

    def _go_back(self):
        from gui.admin_dashboard import AdminDashboardFrame
        self._app.show_frame(AdminDashboardFrame)
