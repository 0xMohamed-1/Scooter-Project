# report_fault_frame.py
# Lets a member select a scooter and submit a fault report.

import tkinter as tk
from tkinter import messagebox


class ReportFaultFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._scooter_ids = []
        self._build()

    def _build(self):
        tk.Label(self, text="Report a Fault", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 5))
        tk.Label(self, text="Select the faulty scooter, describe the problem, then submit.",
                 font=("Arial", 11), bg="#f0f0f0").pack(pady=(0, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=10,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)

        self._load_scooters()

        # Description field
        desc_frame = tk.Frame(self, bg="#f0f0f0")
        desc_frame.pack(fill="x", padx=30, pady=8)

        tk.Label(desc_frame, text="Description:", font=("Arial", 12),
                 bg="#f0f0f0").pack(anchor="w")
        self._desc_entry = tk.Entry(desc_frame, font=("Arial", 12))
        self._desc_entry.pack(fill="x", pady=(4, 0))

        btn_frame = tk.Frame(self, bg="#f0f0f0")
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Submit Report", width=18, font=("Arial", 12),
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

        scooters = self._system.get_all_scooters()
        if not scooters:
            self._listbox.insert("end", "  No scooters in the system.")
            self._scooter_ids.append(None)
        else:
            for scooter in scooters:
                sid    = scooter.get_scooter_id()[:8]
                stype  = scooter.get_type()
                status = scooter.get_status()
                self._listbox.insert("end", "{:<10} {:<10} {}".format(sid, stype, status))
                self._scooter_ids.append(scooter.get_scooter_id())

    def _on_submit(self):
        selection = self._listbox.curselection()
        if not selection:
            messagebox.showerror("No Selection", "Please select a scooter.")
            return

        index = selection[0]
        scooter_id = self._scooter_ids[index]
        if scooter_id is None:
            messagebox.showerror("Invalid Selection", "Please select a scooter row.")
            return

        description = self._desc_entry.get().strip()
        if not description:
            messagebox.showerror("Missing Description", "Please describe the fault.")
            return

        user_id = self._app.current_user.get_user_id()
        record, msg = self._system.report_fault(user_id, scooter_id, description)

        if record is None:
            messagebox.showerror("Error", msg)
        else:
            messagebox.showinfo("Report Submitted",
                "Fault reported. The scooter has been flagged for maintenance.")
            from gui.member_dashboard import MemberDashboardFrame
            self._app.show_frame(MemberDashboardFrame)

    def _go_back(self):
        from gui.member_dashboard import MemberDashboardFrame
        self._app.show_frame(MemberDashboardFrame)
