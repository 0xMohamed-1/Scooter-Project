# manage_wallet_frame.py
# Admin frame for viewing and setting member wallet balances.

import tkinter as tk
from tkinter import messagebox


class ManageWalletFrame(tk.Frame):

    def __init__(self, app, system):
        super().__init__(app, bg="#f0f0f0")
        self._app = app
        self._system = system
        self._members = []       # ordered list matching listbox rows
        self._selected_user = None
        self._build()

    def _build(self):
        tk.Label(self, text="Manage Wallets", font=("Arial", 18, "bold"),
                 bg="#f0f0f0").pack(pady=(20, 5))
        tk.Label(self, text="Select a member to set their wallet balance.",
                 font=("Arial", 11), bg="#f0f0f0").pack(pady=(0, 10))

        list_frame = tk.Frame(self, bg="#f0f0f0")
        list_frame.pack(fill="both", expand=True, padx=30)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self._listbox = tk.Listbox(list_frame, font=("Courier", 11), height=10,
                                   yscrollcommand=scrollbar.set)
        self._listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self._listbox.yview)
        self._listbox.bind("<<ListboxSelect>>", self._on_select)

        self._load_members()

        form_frame = tk.Frame(self, bg="#f0f0f0")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="New Balance (AED):", font=("Arial", 12),
                 bg="#f0f0f0").grid(row=0, column=0, padx=8, sticky="e")
        self._balance_var = tk.StringVar()
        self._balance_entry = tk.Entry(form_frame, textvariable=self._balance_var,
                                       font=("Arial", 12), width=12)
        self._balance_entry.grid(row=0, column=1, padx=8)

        self._set_btn = tk.Button(form_frame, text="Set Balance", width=14,
                                  font=("Arial", 12), state="disabled",
                                  command=self._set_balance)
        self._set_btn.grid(row=0, column=2, padx=8)

        self._msg_label = tk.Label(self, text="", font=("Arial", 11), bg="#f0f0f0")
        self._msg_label.pack()

        tk.Button(self, text="Back", width=18, font=("Arial", 12),
                  command=self._go_back).pack(pady=10)

    def _load_members(self):
        self._listbox.delete(0, "end")
        self._members = []
        header = "{:<20} {:<26} {}".format("Name", "Email", "Wallet (AED)")
        self._listbox.insert("end", header)
        self._listbox.insert("end", "-" * 58)

        members = self._system.get_all_members()
        if not members:
            self._listbox.insert("end", "  No registered members.")
        else:
            for m in members:
                name    = m.get_name()[:18]
                email   = m.get_email()[:24]
                balance = "{:.2f}".format(m.get_wallet_balance())
                line = "{:<20} {:<26} {}".format(name, email, balance)
                self._listbox.insert("end", line)
                self._members.append(m)

    def _on_select(self, _event):
        selection = self._listbox.curselection()
        if not selection:
            return
        idx = selection[0] - 2
        if 0 <= idx < len(self._members):
            self._selected_user = self._members[idx]
            self._balance_var.set("{:.2f}".format(self._selected_user.get_wallet_balance()))
            self._set_btn.config(state="normal")
            self._msg_label.config(text="")
        else:
            self._selected_user = None
            self._set_btn.config(state="disabled")

    def _set_balance(self):
        if self._selected_user is None:
            return
        raw = self._balance_var.get().strip()
        try:
            amount = float(raw)
        except ValueError:
            self._msg_label.config(text="Please enter a valid number.", fg="red")
            return

        ok, msg = self._system.set_user_wallet_balance(
            self._selected_user.get_user_id(), amount)
        if ok:
            self._msg_label.config(
                text="Wallet updated for {}.".format(self._selected_user.get_name()),
                fg="green")
            self._load_members()
            self._set_btn.config(state="disabled")
            self._selected_user = None
        else:
            self._msg_label.config(text=msg, fg="red")

    def _go_back(self):
        from gui.admin_dashboard import AdminDashboardFrame
        self._app.show_frame(AdminDashboardFrame)
