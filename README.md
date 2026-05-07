# Scooter Rental System

A desktop application for managing a scooter rental service, built with Python and Tkinter. The system supports three roles — Guest, Member, and Admin — each with their own dashboard and capabilities.

---

## Features

### Guest
- Browse available scooters and view station locations without an account
- Register for a new account (receives a **$10.00 welcome gift** in their wallet)

### Member
- Browse available scooters (Standard and Premium)
- View docking stations and their capacity
- Reserve a scooter in advance
- Start and end rentals
- Pay for rentals directly from the wallet balance
- View full rental history
- Report scooter faults

### Admin
- Add, edit, and remove scooters from the fleet
- Manage docking stations
- Send scooters for maintenance and mark repairs as complete
- View system-wide reports (rentals, revenue, faults)
- Manage member wallet balances

---

## Scooter Types

| Type     | Rate         |
|----------|--------------|
| Standard | $0.50 / min  |
| Premium  | $1.00 / min  |

Rental cost is calculated automatically based on duration. Battery drains at 1% per minute of use.

---

## Wallet System

- Every new member starts with **$10.00** complimentary credit.
- All payments are made from the wallet balance.
- If the wallet balance is insufficient to cover a rental, the rental cannot be ended until the balance is topped up by an admin.
- Admins can adjust any member's wallet balance from the Manage Wallets panel.

---

## Project Structure

```
scooter-project/
├── main.py                  # Entry point
├── system.py                # Core business logic (RentalSystem)
├── test_flow.py             # End-to-end functional test
├── models/
│   ├── scooter.py           # Scooter, StandardScooter, PremiumScooter
│   ├── station.py           # DockingStation
│   ├── user.py              # User, RegisteredMember, Admin
│   ├── rental.py            # Rental
│   ├── reservation.py       # Reservation
│   ├── payment.py           # Payment
│   ├── maintenance.py       # MaintenanceRecord
│   └── location.py          # Location helper
├── gui/
│   ├── app.py               # Main Tkinter App window
│   ├── login_frame.py       # Login screen
│   ├── register_frame.py    # Registration screen
│   ├── guest_dashboard.py   # Guest home
│   ├── member_dashboard.py  # Member home
│   ├── admin_dashboard.py   # Admin home
│   ├── browse_scooters_frame.py
│   ├── view_stations_frame.py
│   ├── reserve_frame.py
│   ├── start_rental_frame.py
│   ├── end_rental_frame.py
│   ├── history_frame.py
│   ├── report_fault_frame.py
│   ├── manage_scooters_frame.py
│   ├── manage_stations_frame.py
│   ├── manage_wallet_frame.py
│   ├── set_maintenance_frame.py
│   ├── complete_repair_frame.py
│   └── reports_frame.py
└── data/
    ├── users.json           # Persisted user accounts
    ├── scooters.json        # Fleet data
    ├── stations.json        # Station data
    ├── rentals.json         # Rental records
    ├── reservations.json    # Reservation records
    └── payments.json        # Payment transactions
```

---

## Getting Started

### Requirements
- Python 3.8+
- Tkinter (included with standard Python on Windows and macOS)

### Run the app

```bash
python main.py
```

### Run the test suite

```bash
python test_flow.py
```

---

## Data Persistence

All data is stored locally as JSON files in the `data/` directory. The system loads data on startup and saves automatically after every state-changing operation.
