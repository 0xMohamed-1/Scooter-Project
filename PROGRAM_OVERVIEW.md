# Scooter Rental System — Program Overview

---

## Mind Map

```
                        SCOOTER RENTAL SYSTEM
                               │
          ┌────────────────────┼───────────────────────┐
          │                    │                       │
       MODELS             CONTROLLER                   GUI
    (data layer)         (system.py)              (tkinter views)
          │                    │                       │
    ┌─────┴──────┐        16 Use Cases            ┌────┴────┐
    │            │             │                  │         │
  Entities   Transactions   ┌──┴──┐            Screens   Navigation
    │            │          │     │                │     (show_frame)
  User       Rental       Auth  Admin             Frames
  Scooter    Reservation    │     │                │
  Station    Payment       Login  Manage           Login
  Location   Maintenance   Reg   Scooters         Dashboards
                           Browse Stations       Action screens
                           Reserve Repair
                           Rent   Reports
                          History
```

---

## 1. High-Level Architecture

The system follows a **3-layer architecture** (similar to MVC):

| Layer | Files | Responsibility |
|---|---|---|
| **Model** | `models/` | Domain objects with state and basic behaviour |
| **Controller** | `system.py` | All business logic, data persistence, use-case orchestration |
| **View** | `gui/` | tkinter screens — display data and capture user input |

**Entry point:** `main.py` instantiates `App` (the tkinter window) and starts the event loop.

**Persistence:** All data is stored as flat JSON files in the `data/` folder. The system loads everything into in-memory Python dicts on startup and writes back after every change. No database or ORM is used.

---

## 2. Folder & File Structure

```
Scooter-Project-main/
│
├── main.py                  ← Entry point
├── system.py                ← RentalSystem controller (business logic + persistence)
│
├── models/
│   ├── user.py              ← User, Guest, RegisteredMember, Admin
│   ├── scooter.py           ← Scooter, StandardScooter, PremiumScooter
│   ├── station.py           ← Station (docking hub)
│   ├── location.py          ← Location value object (Google Maps URL)
│   ├── rental.py            ← Rental lifecycle record
│   ├── reservation.py       ← Reservation (15-min hold)
│   ├── payment.py           ← Payment transaction record
│   └── maintenance.py       ← MaintenanceRecord (fault → repair)
│
├── gui/
│   ├── app.py               ← Main tkinter window + frame navigation
│   ├── login_frame.py       ← Login screen
│   ├── register_frame.py    ← New account registration
│   ├── guest_dashboard.py   ← Read-only view for unregistered visitors
│   ├── member_dashboard.py  ← Member hub (navigation only)
│   ├── admin_dashboard.py   ← Admin hub (navigation only)
│   ├── browse_scooters_frame.py
│   ├── view_stations_frame.py
│   ├── reserve_frame.py
│   ├── start_rental_frame.py
│   ├── end_rental_frame.py
│   ├── history_frame.py
│   ├── report_fault_frame.py
│   ├── manage_scooters_frame.py
│   ├── manage_stations_frame.py
│   ├── set_maintenance_frame.py
│   ├── complete_repair_frame.py
│   └── reports_frame.py
│
└── data/
    ├── users.json
    ├── scooters.json
    ├── stations.json
    ├── rentals.json
    ├── reservations.json
    ├── payments.json
    └── maintenance.json
```

---

## 3. Domain Models

### 3.1 User Hierarchy (Inheritance)

```
User  (base — user_id, name, email, password)
 ├── Guest            → can only browse; no login required
 ├── RegisteredMember → can reserve, rent, view history, report faults
 │                      + payment_method ("card" / "wallet")
 │                      + rental_history (list of rental IDs)
 └── Admin            → can manage fleet, stations, maintenance, view reports
```

Each class overrides `get_role()` and `to_dict()` for JSON serialisation.

---

### 3.2 Scooter Hierarchy (Polymorphism)

```
Scooter  (base — scooter_id, battery_level, status, current_station_id)
 │  cost_per_minute() → 0.0  (overridden by subclasses)
 ├── StandardScooter  → cost_per_minute() = $0.50 / min
 └── PremiumScooter   → cost_per_minute() = $1.00 / min
```

**Status values:** `available` → `reserved` → `in_use` → `maintenance`

Battery drains at **1% per minute** of ride time (simulated on `end_rental`).

---

### 3.3 Station

Each Station has:
- `name`, `capacity` (max docked scooters), `location` (a `Location` object)
- `scooter_ids` — list of currently docked scooter IDs
- `is_full()` — enforced before every drop-off or add

**Location** is a value object that wraps a Google Maps URL.

---

### 3.4 Transaction Models

| Model | Key Fields | Status Lifecycle |
|---|---|---|
| **Rental** | user_id, scooter_id, start/end time, cost, payment_id | `active` → `completed` / `cancelled` |
| **Reservation** | user_id, scooter_id, created_at, expires_at (15 min) | `pending` → `confirmed` → `converted` / `expired` / `cancelled` |
| **Payment** | rental_id, user_id, amount, method | `pending` → `completed` / `failed` / `refunded` |
| **MaintenanceRecord** | scooter_id, reported_by, description, resolved_at | `reported` → `in_progress` → `resolved` |

---

## 4. RentalSystem Controller — Use Cases

`system.py` maps directly to the system's use cases. Every public method follows the same contract: it returns a `(result, message)` tuple where `result` is `None` / `False` on failure, or the object / `True` on success.

```
RentalSystem
 │
 ├── Auth
 │    ├── register_user(name, email, password, payment_method)   [UC1]
 │    └── login(email, password)                                  [UC4]
 │
 ├── Browse / View
 │    ├── get_all_scooters()                                      [UC2]
 │    ├── get_available_scooters()                                [UC2]
 │    └── get_all_stations()                                      [UC3]
 │
 ├── Reservation
 │    ├── reserve_scooter(user_id, scooter_id)                   [UC5]
 │    └── cancel_reservation(reservation_id)                      [UC6]
 │
 ├── Rental
 │    ├── start_rental(user_id, scooter_id, station_id, res_id?) [UC7]
 │    ├── end_rental(rental_id, end_station_id, payment_method)  [UC8]
 │    │    ├── _calculate_cost(start, end, rate)                 [UC9]
 │    │    └── _process_payment(rental_id, user_id, cost, method)[UC10]
 │    └── get_rental_history(user_id)                             [UC11]
 │
 ├── Maintenance
 │    ├── report_fault(user_id, scooter_id, description)         [UC12]
 │    ├── set_maintenance(scooter_id, description, admin_id)     [UC15]
 │    └── complete_repair(record_id, station_id)                  [UC16]
 │
 ├── Admin — Fleet Management
 │    ├── add_scooter(type, battery, station_id)                 [UC13]
 │    ├── remove_scooter(scooter_id)                             [UC13]
 │    ├── add_station(name, maps_url, capacity)                   [UC14]
 │    └── remove_station(station_id)                             [UC14]
 │
 └── Reports
      └── get_reports()  → fleet counts + revenue summary
```

---

## 5. GUI — Screen Navigation Map

```
App starts
    │
    ▼
LoginFrame ──────────────────────────┐
    │                                │
    ├─ [Login as Admin]              │
    │       └──► AdminDashboard      │
    │                 ├── ManageScootersFrame
    │                 ├── ManageStationsFrame
    │                 ├── SetMaintenanceFrame
    │                 ├── CompleteRepairFrame
    │                 ├── ReportsFrame
    │                 └── [Logout] ──────────────────┐
    │                                                 │
    ├─ [Login as Member]                              │
    │       └──► MemberDashboard                      │
    │                 ├── BrowseScootersFrame          │
    │                 ├── ViewStationsFrame            │
    │                 ├── ReserveFrame                 │
    │                 ├── StartRentalFrame             │
    │                 ├── EndRentalFrame               │
    │                 ├── HistoryFrame                 │
    │                 ├── ReportFaultFrame             │
    │                 └── [Logout] ──────────────────►─┤
    │                                                   │
    └─ [Continue as Guest]                             │
            └──► GuestDashboard (read-only)            │
                      ├── shows all scooters           │
                      ├── shows all stations           │
                      ├── [Register] ─► RegisterFrame ─┘
                      └── [Logout] ──────────────────►─┘
                                                       │
                                               back to LoginFrame
```

**Navigation pattern:** `App.show_frame(FrameClass)` destroys the current screen and mounts a fresh one. All frames receive the shared `App` and `RentalSystem` instances so they can read state and call operations.

---

## 6. Key Business Rules

| Rule | Where enforced |
|---|---|
| Reservation expires after 15 minutes | `Reservation.is_expired()` checked in `start_rental()` |
| Scooter cannot be rented if not `available` or `reserved` | `start_rental()` guards |
| Station capacity checked before drop-off | `end_rental()` calls `station.is_full()` |
| Scooter under `in_use` cannot be removed or flagged for maintenance | `remove_scooter()`, `set_maintenance()` guards |
| Station with docked scooters cannot be deleted | `remove_station()` guard |
| Cost = duration (minutes) × scooter rate | `_calculate_cost()` |
| Payment is created and immediately marked `completed` (simulated) | `_process_payment()` |
| Fault report automatically flags scooter as `maintenance` and removes it from its station | `report_fault()` |

---

## 7. Data Persistence Flow

```
App startup
    │
    ▼
RentalSystem.__init__()
    │
    ├── _load_users()       reads users.json       → self._users   dict
    ├── _load_scooters()    reads scooters.json    → self._scooters dict
    ├── _load_stations()    reads stations.json    → self._stations dict
    ├── _load_rentals()     reads rentals.json     → self._rentals  dict
    ├── _load_reservations()reads reservations.json→ self._reservations dict
    ├── _load_payments()    reads payments.json    → self._payments  dict
    └── _load_maintenance() reads maintenance.json → self._maintenance dict

After every write operation:
    save_data() serialises all 7 dicts back to their JSON files using to_dict()
```

All IDs are **UUID v4** strings generated by `_new_id()`. Datetime fields are stored as ISO-format strings and parsed back on load.

---

## 8. OOP Concepts Used

| Concept | Where |
|---|---|
| **Inheritance** | `User → Guest / RegisteredMember / Admin`; `Scooter → Standard / Premium` |
| **Polymorphism** | `cost_per_minute()` and `get_type()` overridden in scooter subclasses; `get_role()` and `to_dict()` in user subclasses |
| **Encapsulation** | All model attributes are `_private`; accessed only through getter/setter methods |
| **Composition** | `Station` contains a `Location` object; `Rental` references IDs to User, Scooter, Station, Payment |
| **Single Responsibility** | Each model owns only its own state; `RentalSystem` owns all cross-entity logic |

---

## 9. Summary

The **Scooter Rental System** is a desktop application that simulates a city-wide e-scooter fleet. It supports three user roles with role-specific dashboards, a full rental lifecycle from reservation to payment, an automated fault-reporting pipeline that pulls scooters out of service, and an admin panel for fleet and station management backed by live JSON reports. All data persists between sessions through a set of flat JSON files read on startup and written after every operation.
