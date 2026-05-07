# set_maintenance_frame.py
# Admin screen to flag a scooter for maintenance.

import tkinter as tk
from tkinter import messagebox


class SetMaintenanceFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._scooter_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="Set Maintenance", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 5))
        tk.Label(self, text="Select a scooter, enter a description, then confirm.",
                 font=("Arial", 11), bg="#f0f0f0").pack(pady=(0, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=11,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_scooters()

        desc_frame = tk.Frame(self, bg="#f0f0f0")
        desc_frame.pack(fill="x", padx=30, pady=8)

        tk.Label(desc_frame, text="Reason / Description:", font=("Arial", 12),
                 bg="#f0f0f0").pack(anchor="w")
        self._desc_entry = tk.Entry(desc_frame, font=("Arial", 12))
        self._desc_entry.pack(fill="x", pady=(4, 0))

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Set Maintenance", width=18, font=("Arial", 12),
                  command=self._on_submit).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Back", width=14, font=("Arial", 12),
                  command=self._go_back).grid(row=0, column=1, padx=10)

    def _load_scooters(self):
        self._listbox.delete(0, "end")
        self._scooter_ids = []

        header = "{:<10} {:<10} {}".format("ID", "Type", "Status")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 36)
        self._scooter_ids.append(None)
        self._scooter_ids.append(None)

        # Show only scooters that are not already under maintenance
        for scooter in self._system.get_all_scooters():
            if scooter.get_status() != "maintenance":
                sid   = scooter.get_scooter_id()[:8]
                stype = scooter.get_type()
                status = scooter.get_status()
                self._listbox.insert("end", "{:<10} {:<10} {}".format(sid, stype, status))
                self._scooter_ids.append(scooter.get_scooter_id())

    def _on_submit(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a scooter.")
            return

        scooter_id = self._scooter_ids[selection[0]]
        if scooter_id is None:
            messagebox.showerror("Invalid Selection", "Please select a scooter row.")
            return

        description = self._desc_entry.get().strip()
        if not description:
            messagebox.showerror("Missing Description", "Please enter a reason.")
            return

        admin_id = self._app.current_user.get_user_id()
        record, msg = self._system.set_maintenance(scooter_id, description, admin_id)

        if record is None:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Done", "Scooter flagged for maintenance.")
            from gui.admin_dashboard import AdminDashboardFrame
            self._app.show_frame(AdminDashboardFrame)

    def _go_back(self):
        from gui.admin_dashboard import AdminDashboardFrame
        self._app.show_frame(AdminDashboardFrame)
