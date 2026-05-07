# complete_repair_frame.py
# Admin screen to mark a maintenance record as resolved and return the scooter.

import tkinter as tk
from tkinter import messagebox


class CompleteRepairFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._record_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="Complete Repair", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 5))
        tk.Label(self, text="Select an open maintenance record, choose a return station.",
                 font=("Arial", 11), bg="#f0f0f0").pack(pady=(0, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=10,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_records()

        form = tk.Frame(self, bg="#f0f0f0")
        form.pack(pady=10)

        tk.Label(form, text="Return to station:", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=0, column=0, sticky="e", padx=10)

        self._station_var = tk.StringVar()
        self._station_name_to_id = {}
        station_names = []
        for station in self._system.get_all_stations():
            if not station.is_full():
                station_names.append(station.get_name())
                self._station_name_to_id[station.get_name()] = station.get_station_id()

        if station_names:
            self._station_var.set(station_names[0])
        else:
            station_names = ["(no stations available)"]
            self._station_var.set(station_names[0])

        dropdown = tk.OptionMenu(form, self._station_var, *station_names)
        dropdown.config(font=("Arial", 12), width=22)
        dropdown.grid(row=0, column=1)

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Complete Repair", width=18, font=("Arial", 12),
                  command=self._on_complete).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Back", width=14, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=1, padx=10)

    def _load_records(self):
        self._listbox.delete(0, "end")
        self._record_ids = []

        header = "{:<10} {:<10} {:<18} {}".format(
            "Record", "Scooter", "Reported At", "Description")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 60)
        self._record_ids.append(None)
        self._record_ids.append(None)

        records = self._system.get_all_maintenance_records()
        open_records = []
        for rec in records:
            if rec.get_status() != "resolved":
                open_records.append(rec)

        if not open_records:
            self._listbox.insert("end", "  No open maintenance records.")
            self._record_ids.append(None)
        else:
            for rec in open_records:
                rid   = rec.get_record_id()[:8]
                sid   = rec.get_scooter_id()[:8]
                date  = str(rec.get_reported_at())[:16]
                desc  = rec.get_description()[:20]
                self._listbox.insert("end", "{:<10} {:<10} {:<18} {}".format(
                    rid, sid, date, desc))
                self._record_ids.append(rec.get_record_id())

    def _on_complete(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a maintenance record.")
            return

        record_id = self._record_ids[selection[0]]
        if record_id is None:
            messagebox.showerror("Invalid Selection", "Please select a record row.")
            return

        station_name = self._station_var.get()
        station_id = self._station_name_to_id.get(station_name)
        if not station_id:
            messagebox.showerror("No Station", "Please select a valid return station.")
            return

        success, msg = self._system.complete_repair(record_id, station_id)
        if not success:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Done", "Repair completed. Scooter is now available.")
            from gui.admin_dashboard import AdminDashboardFrame
            self._app.show_frame(AdminDashboardFrame)

    def _go_back(self):
        from gui.admin_dashboard import AdminDashboardFrame
        self._app.show_frame(AdminDashboardFrame)
