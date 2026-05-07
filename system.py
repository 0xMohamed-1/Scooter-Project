# system.py
# RentalSystem is the main controller.
# It holds all data in memory as dictionaries, loads from JSON on startup,
# and saves back to JSON after every change.

import json
import os
import uuid
from datetime import datetime, timedelta

from models.user import Guest, RegisteredMember, Admin
from models.scooter import StandardScooter, PremiumScooter
from models.station import Station
from models.location import Location
from models.rental import Rental
from models.reservation import Reservation
from models.maintenance import MaintenanceRecord
from models.payment import Payment

# Data folder sits next to system.py
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

USERS_FILE        = os.path.join(DATA_DIR, "users.json")
SCOOTERS_FILE     = os.path.join(DATA_DIR, "scooters.json")
STATIONS_FILE     = os.path.join(DATA_DIR, "stations.json")
RENTALS_FILE      = os.path.join(DATA_DIR, "rentals.json")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.json")
PAYMENTS_FILE     = os.path.join(DATA_DIR, "payments.json")
MAINTENANCE_FILE  = os.path.join(DATA_DIR, "maintenance.json")


class RentalSystem:

    def __init__(self):
        # Each dict maps an object's ID to the object itself
        self._users        = {}
        self._scooters     = {}
        self._stations     = {}
        self._rentals      = {}
        self._reservations = {}
        self._payments     = {}
        self._maintenance  = {}

        # Make sure the data folder exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        self.load_data()

    # ------------------------------------------------------------------
    # JSON helpers
    # ------------------------------------------------------------------

    def _read_json(self, filepath):
        # Return the list stored in the file, or [] if the file doesn't exist yet
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r") as f:
            return json.load(f)

    def _write_json(self, filepath, data):
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _new_id(self):
        # Generate a unique ID string
        return str(uuid.uuid4())

    # ------------------------------------------------------------------
    # Load all data from JSON files
    # ------------------------------------------------------------------

    def load_data(self):
        self._load_users()
        self._load_scooters()
        self._load_stations()
        self._load_rentals()
        self._load_reservations()
        self._load_payments()
        self._load_maintenance()

    def _load_users(self):
        for d in self._read_json(USERS_FILE):
            role = d["role"]
            if role == "admin":
                user = Admin(d["user_id"], d["name"], d["email"], d["password"])
            elif role == "member":
                user = RegisteredMember(
                    d["user_id"], d["name"], d["email"], d["password"],
                    d.get("payment_method", "wallet")
                )
                user._rental_history = d.get("rental_history", [])
                user._wallet_balance = d.get("wallet_balance", 0.0)
            else:
                user = Guest(d["user_id"], d["name"], d["email"], d["password"])
            self._users[user.get_user_id()] = user

    def _load_scooters(self):
        for d in self._read_json(SCOOTERS_FILE):
            if d["type"] == "premium":
                scooter = PremiumScooter(
                    d["scooter_id"], d["battery_level"],
                    d["status"], d.get("current_station_id")
                )
            else:
                scooter = StandardScooter(
                    d["scooter_id"], d["battery_level"],
                    d["status"], d.get("current_station_id")
                )
            self._scooters[scooter.get_scooter_id()] = scooter

    def _load_stations(self):
        for d in self._read_json(STATIONS_FILE):
            loc = d["location"]
            location = Location(loc["maps_url"], loc.get("station_id"))
            station = Station(d["station_id"], d["name"], location, d["capacity"])
            station._scooter_ids = d.get("scooter_ids", [])
            self._stations[station.get_station_id()] = station

    def _load_rentals(self):
        for d in self._read_json(RENTALS_FILE):
            start = datetime.fromisoformat(d["start_time"])
            rental = Rental(d["rental_id"], d["user_id"], d["scooter_id"], start, d["start_station_id"])
            rental._end_time        = datetime.fromisoformat(d["end_time"]) if d.get("end_time") else None
            rental._end_station_id  = d.get("end_station_id")
            rental._total_cost      = d.get("total_cost", 0.0)
            rental._status          = d.get("status", "active")
            rental._payment_id      = d.get("payment_id")
            self._rentals[rental.get_rental_id()] = rental

    def _load_reservations(self):
        for d in self._read_json(RESERVATIONS_FILE):
            created = datetime.fromisoformat(d["created_at"])
            expires = datetime.fromisoformat(d["expires_at"])
            res = Reservation(d["reservation_id"], d["user_id"], d["scooter_id"], created, expires)
            res._status = d.get("status", "pending")
            self._reservations[res.get_reservation_id()] = res

    def _load_payments(self):
        for d in self._read_json(PAYMENTS_FILE):
            ts = datetime.fromisoformat(d["timestamp"])
            pay = Payment(d["payment_id"], d["rental_id"], d["user_id"], d["amount"], d["method"], ts)
            pay._status = d.get("status", "pending")
            self._payments[pay.get_payment_id()] = pay

    def _load_maintenance(self):
        for d in self._read_json(MAINTENANCE_FILE):
            reported = datetime.fromisoformat(d["reported_at"])
            rec = MaintenanceRecord(
                d["record_id"], d["scooter_id"], d["reported_by"],
                reported, d["description"]
            )
            rec._resolved_at = datetime.fromisoformat(d["resolved_at"]) if d.get("resolved_at") else None
            rec._status      = d.get("status", "reported")
            self._maintenance[rec.get_record_id()] = rec

    # ------------------------------------------------------------------
    # Save all data to JSON files

    # ------------------------------------------------------------------

    def save_data(self):
        user_list = []
        for u in self._users.values():
            user_list.append(u.to_dict())
        self._write_json(USERS_FILE, user_list)

        scooter_list = []
        for s in self._scooters.values():
            scooter_list.append(s.to_dict())
        self._write_json(SCOOTERS_FILE, scooter_list)

        station_list = []
        for s in self._stations.values():
            station_list.append(s.to_dict())
        self._write_json(STATIONS_FILE, station_list)

        rental_list = []
        for r in self._rentals.values():
            rental_list.append(r.to_dict())
        self._write_json(RENTALS_FILE, rental_list)

        reservation_list = []
        for r in self._reservations.values():
            reservation_list.append(r.to_dict())
        self._write_json(RESERVATIONS_FILE, reservation_list)

        payment_list = []
        for p in self._payments.values():
            payment_list.append(p.to_dict())
        self._write_json(PAYMENTS_FILE, payment_list)

        maintenance_list = []
        for m in self._maintenance.values():
            maintenance_list.append(m.to_dict())
        self._write_json(MAINTENANCE_FILE, maintenance_list)

    # ------------------------------------------------------------------
    # Use Case 1 — Register
    # ------------------------------------------------------------------

    def register_user(self, name, email, password, payment_method="wallet"):
        # Make sure no existing user has this email
        for user in self._users.values():
            if user.get_email() == email:
                return None, "An account with that email already exists."

        user_id = self._new_id()
        member = RegisteredMember(user_id, name, email, password, payment_method)
        member.set_wallet_balance(10.0)  # complimentary welcome gift
        self._users[user_id] = member
        self.save_data()
        return member, "OK"

    # ------------------------------------------------------------------
    # Use Case 4 — Login / Logout
    # ------------------------------------------------------------------

    def login(self, email, password):
        # Search for a matching email + password pair
        for user in self._users.values():
            if user.get_email() == email and user.check_password(password):
                return user, "OK"
        return None, "Incorrect email or password."

    # ------------------------------------------------------------------
    # Use Case 2 — Browse Scooters
    # ------------------------------------------------------------------

    def get_all_scooters(self):
        return list(self._scooters.values())

    def get_available_scooters(self):
        result = []
        for scooter in self._scooters.values():
            if scooter.get_status() == "available":
                result.append(scooter)
        return result

    # ------------------------------------------------------------------
    # Use Case 3 — View Stations
    # ------------------------------------------------------------------

    def get_all_stations(self):
        return list(self._stations.values())

    # ------------------------------------------------------------------
    # Use Case 5 — Reserve Scooter
    # ------------------------------------------------------------------

    def reserve_scooter(self, user_id, scooter_id):
        scooter = self._scooters.get(scooter_id)
        if scooter is None:
            return None, "Scooter not found."
        if scooter.get_status() != "available":
            return None, "Scooter is not available for reservation."
        if scooter.get_status() == "maintenance":
            return None, "Scooter is under maintenance."

        now = datetime.now()
        expires = now + timedelta(minutes=15)
        res_id = self._new_id()
        reservation = Reservation(res_id, user_id, scooter_id, now, expires)
        reservation.confirm()

        scooter.set_status("reserved")
        self._reservations[res_id] = reservation
        self.save_data()
        return reservation, "OK"

    # ------------------------------------------------------------------
    # Use Case 6 — Cancel Booking
    # ------------------------------------------------------------------

    def cancel_reservation(self, reservation_id):
        res = self._reservations.get(reservation_id)
        if res is None:
            return False, "Reservation not found."
        if res.get_status() not in ("pending", "confirmed"):
            return False, "This reservation cannot be cancelled."

        scooter = self._scooters.get(res.get_scooter_id())
        if scooter and scooter.get_status() == "reserved":
            scooter.set_status("available")

        res.cancel()
        self.save_data()
        return True, "OK"

    # ------------------------------------------------------------------
    # Use Case 7 — Start Rental
    # ------------------------------------------------------------------

    def start_rental(self, user_id, scooter_id, start_station_id, reservation_id=None):
        scooter = self._scooters.get(scooter_id)
        if scooter is None:
            return None, "Scooter not found."

        if reservation_id:
            # Starting from an existing reservation
            res = self._reservations.get(reservation_id)
            if res is None:
                return None, "Reservation not found."
            if res.is_expired():
                res.expire()
                scooter.set_status("available")
                self.save_data()
                return None, "Reservation has expired."
            if res.get_status() != "confirmed":
                return None, "Reservation is not in a valid state to start a rental."
            res.convert_to_rental()
        else:
            # Direct unlock — scooter must be available
            if scooter.get_status() != "available":
                return None, "Scooter is not available."

        # Remove from start station
        station = self._stations.get(start_station_id)
        if station:
            station.remove_scooter(scooter_id)

        scooter.set_status("in_use")
        scooter.set_current_station_id(None)

        rental_id = self._new_id()
        rental = Rental(rental_id, user_id, scooter_id, datetime.now(), start_station_id)
        self._rentals[rental_id] = rental
        self.save_data()
        return rental, "OK"

    # ------------------------------------------------------------------
    # Use Case 8 — End Rental
    # (includes Use Case 9: Calculate Cost and Use Case 10: Process Payment)
    # ------------------------------------------------------------------

    def end_rental(self, rental_id, end_station_id, payment_method):
        rental = self._rentals.get(rental_id)
        if rental is None:
            return False, "Rental not found."
        if rental.get_status() != "active":
            return False, "This rental is not active."

        # Business rule: the return station must have space
        station = self._stations.get(end_station_id)
        if station is None:
            return False, "Station not found."
        if station.is_full():
            return False, "That station is full — please choose a different one."

        scooter = self._scooters.get(rental.get_scooter_id())
        end_time = datetime.now()

        # Use Case 9 — Calculate cost
        cost = self._calculate_cost(rental.get_start_time(), end_time, scooter.cost_per_minute())

        # Use Case 10 — Process payment
        user = self._users.get(rental.get_user_id())
        if payment_method == "wallet":
            if user is None or user.get_role() != "member":
                return False, "Wallet payment requires a registered account."
            if user.get_wallet_balance() < cost:
                return False, "Insufficient wallet balance (${:.2f} available, ${:.2f} required).".format(
                    user.get_wallet_balance(), cost)
            user.set_wallet_balance(user.get_wallet_balance() - cost)
        payment = self._process_payment(rental_id, rental.get_user_id(), cost, payment_method)

        # Simulate battery drain (1% per minute)
        duration_minutes = (end_time - rental.get_start_time()).total_seconds() / 60
        scooter.drain_battery(duration_minutes)

        # Finalise the rental record
        rental.end_rental(end_time, end_station_id, cost)
        rental.set_payment_id(payment.get_payment_id())

        # Dock the scooter at the return station
        scooter.set_status("available")
        scooter.set_current_station_id(end_station_id)
        station.add_scooter(rental.get_scooter_id())

        # Add this rental to the member's history
        if user and user.get_role() == "member":
            user.add_rental_to_history(rental_id)

        self.save_data()
        return True, "OK"

    def _calculate_cost(self, start_time, end_time, rate):
        # Use Case 9 — duration in minutes times the per-minute rate
        duration_minutes = (end_time - start_time).total_seconds() / 60
        return round(duration_minutes * rate, 2)

    def _process_payment(self, rental_id, user_id, amount, method):
        # Use Case 10 — create a payment record and mark it completed immediately
        pay_id = self._new_id()
        payment = Payment(pay_id, rental_id, user_id, amount, method, datetime.now())
        payment.complete()
        self._payments[pay_id] = payment
        return payment

    # ------------------------------------------------------------------
    # Use Case 11 — View Rental History
    # ------------------------------------------------------------------

    def get_rental_history(self, user_id):
        user = self._users.get(user_id)
        if user is None or user.get_role() != "member":
            return []
        result = []
        for rental_id in user.get_rental_history():
            rental = self._rentals.get(rental_id)
            if rental:
                result.append(rental)
        return result

    # ------------------------------------------------------------------
    # Use Case 12 — Report Fault (extends Set Maintenance)
    # ------------------------------------------------------------------

    def report_fault(self, user_id, scooter_id, description):
        scooter = self._scooters.get(scooter_id)
        if scooter is None:
            return None, "Scooter not found."

        rec_id = self._new_id()
        record = MaintenanceRecord(rec_id, scooter_id, user_id, datetime.now(), description)
        self._maintenance[rec_id] = record

        # Automatically flag the scooter as under maintenance
        station_id = scooter.get_current_station_id()
        if station_id:
            station = self._stations.get(station_id)
            if station:
                station.remove_scooter(scooter_id)

        scooter.set_status("maintenance")
        scooter.set_current_station_id(None)

        self.save_data()
        return record, "OK"

    # ------------------------------------------------------------------
    # Use Case 13 — Manage Scooters (Admin)
    # ------------------------------------------------------------------

    def add_scooter(self, scooter_type, battery_level, station_id):
        station = self._stations.get(station_id)
        if station is None:
            return None, "Station not found."
        if station.is_full():
            return None, "Station is full."

        scooter_id = self._new_id()
        if scooter_type == "premium":
            scooter = PremiumScooter(scooter_id, battery_level, "available", station_id)
        else:
            scooter = StandardScooter(scooter_id, battery_level, "available", station_id)

        self._scooters[scooter_id] = scooter
        station.add_scooter(scooter_id)
        self.save_data()
        return scooter, "OK"

    def remove_scooter(self, scooter_id):
        scooter = self._scooters.get(scooter_id)
        if scooter is None:
            return False, "Scooter not found."
        if scooter.get_status() == "in_use":
            return False, "Cannot remove a scooter that is currently in use."

        # Un-dock from its station if needed
        station_id = scooter.get_current_station_id()
        if station_id:
            station = self._stations.get(station_id)
            if station:
                station.remove_scooter(scooter_id)

        del self._scooters[scooter_id]
        self.save_data()
        return True, "OK"

    # ------------------------------------------------------------------
    # Use Case 14 — Manage Stations (Admin)
    # ------------------------------------------------------------------

    def add_station(self, name, maps_url, capacity):
        station_id = self._new_id()
        location = Location(maps_url, station_id)
        station = Station(station_id, name, location, capacity)
        self._stations[station_id] = station
        self.save_data()
        return station, "OK"

    def remove_station(self, station_id):
        station = self._stations.get(station_id)
        if station is None:
            return False, "Station not found."
        if len(station.get_scooter_ids()) > 0:
            return False, "Cannot remove a station that still has scooters docked."
        del self._stations[station_id]
        self.save_data()
        return True, "OK"

    # ------------------------------------------------------------------
    # Use Case 15 — Set Maintenance (Admin)
    # ------------------------------------------------------------------

    def set_maintenance(self, scooter_id, description, admin_id):
        scooter = self._scooters.get(scooter_id)
        if scooter is None:
            return None, "Scooter not found."
        if scooter.get_status() == "in_use":
            return None, "Cannot flag a scooter that is currently in use."

        station_id = scooter.get_current_station_id()
        if station_id:
            station = self._stations.get(station_id)
            if station:
                station.remove_scooter(scooter_id)

        scooter.set_status("maintenance")
        scooter.set_current_station_id(None)

        rec_id = self._new_id()
        record = MaintenanceRecord(rec_id, scooter_id, admin_id, datetime.now(), description)
        self._maintenance[rec_id] = record
        self.save_data()
        return record, "OK"

    # ------------------------------------------------------------------
    # Use Case 16 — Complete Repair (Admin)
    # ------------------------------------------------------------------

    def complete_repair(self, record_id, station_id):
        record = self._maintenance.get(record_id)
        if record is None:
            return False, "Maintenance record not found."

        station = self._stations.get(station_id)
        if station is None:
            return False, "Station not found."
        if station.is_full():
            return False, "Station is full — choose a different station."

        scooter = self._scooters.get(record.get_scooter_id())
        if scooter:
            scooter.set_status("available")
            scooter.set_current_station_id(station_id)
            station.add_scooter(scooter.get_scooter_id())

        record.resolve(datetime.now())
        self.save_data()
        return True, "OK"

    # ------------------------------------------------------------------
    # View Reports (Admin)
    # ------------------------------------------------------------------

    def get_reports(self):
        # Count scooters by status
        available  = 0
        in_use     = 0
        reserved   = 0
        maintenance = 0
        for s in self._scooters.values():
            status = s.get_status()
            if status == "available":
                available += 1
            elif status == "in_use":
                in_use += 1
            elif status == "reserved":
                reserved += 1
            elif status == "maintenance":
                maintenance += 1

        # Count completed rentals and sum revenue
        completed_rentals = 0
        total_revenue = 0.0
        for r in self._rentals.values():
            if r.get_status() == "completed":
                completed_rentals += 1
                total_revenue += r.get_total_cost()

        return {
            "total_scooters":    len(self._scooters),
            "available":         available,
            "in_use":            in_use,
            "reserved":          reserved,
            "maintenance":       maintenance,
            "total_stations":    len(self._stations),
            "completed_rentals": completed_rentals,
            "total_revenue":     round(total_revenue, 2)
        }

    # ------------------------------------------------------------------
    # Lookup helpers (used by the GUI)
    # ------------------------------------------------------------------

    def get_scooter(self, scooter_id):
        return self._scooters.get(scooter_id)

    def get_station(self, station_id):
        return self._stations.get(station_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_rental(self, rental_id):
        return self._rentals.get(rental_id)

    def get_reservation(self, reservation_id):
        return self._reservations.get(reservation_id)

    def get_all_maintenance_records(self):
        return list(self._maintenance.values())

    def get_active_rental_for_user(self, user_id):
        # Find the one active rental belonging to this user, if any
        for rental in self._rentals.values():
            if rental.get_user_id() == user_id and rental.get_status() == "active":
                return rental
        return None

    def get_active_reservation_for_user(self, user_id):
        # Find any pending/confirmed reservation belonging to this user
        for res in self._reservations.values():
            if res.get_user_id() == user_id and res.get_status() in ("pending", "confirmed"):
                return res
        return None

    def get_all_members(self):
        return [u for u in self._users.values() if u.get_role() == "member"]

    # ------------------------------------------------------------------
    # Wallet management (Admin)
    # ------------------------------------------------------------------

    def set_user_wallet_balance(self, user_id, amount):
        user = self._users.get(user_id)
        if user is None or user.get_role() != "member":
            return False, "Member not found."
        if amount < 0:
            return False, "Balance cannot be negative."
        user.set_wallet_balance(amount)
        self.save_data()
        return True, "OK"
