# test_flow.py
# Runs a complete rental cycle from registration through to payment and repair.
# Execute from inside the scooter_rental/ folder: python3 test_flow.py

import os
import sys

# Make sure imports work when run directly
sys.path.insert(0, os.path.dirname(__file__))

from system import RentalSystem
from models.user import Admin


# ------------------------------------------------------------------
# Helper — prints PASS or FAIL for each check
# ------------------------------------------------------------------

def check(label, condition):
    if condition:
        print("  PASS:", label)
    else:
        print("  FAIL:", label)


# ------------------------------------------------------------------
# Helper — wipe data files so the test always starts clean
# ------------------------------------------------------------------

def clear_data_files():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    files = [
        "users.json", "scooters.json", "stations.json",
        "rentals.json", "reservations.json", "payments.json",
        "maintenance.json"
    ]
    for filename in files:
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            os.remove(path)


# ==================================================================
# MAIN TEST
# ==================================================================

print("=" * 50)
print("Scooter Rental System — Full Flow Test")
print("=" * 50)

# -- Setup ----------------------------------------------------------
print("\n[Setup] Clearing old data and creating system...")
clear_data_files()
system = RentalSystem()

# Manually insert an admin user for this test session
admin = Admin("admin-001", "Admin User", "admin@test.com", "admin123")
system._users["admin-001"] = admin
system.save_data()
print("  System created.")


# -- Step 1: Add a station ------------------------------------------
print("\n[Step 1] Adding a station...")
station, msg = system.add_station("City Centre", 51.5, -0.1, 5)
check("Station created", station is not None)
check("Station has capacity 5", station.get_capacity() == 5)
station_id = station.get_station_id()


# -- Step 2: Add scooters -------------------------------------------
print("\n[Step 2] Adding scooters...")
s1, msg = system.add_scooter("standard", 100, station_id)
s2, msg = system.add_scooter("premium",  100, station_id)
check("Standard scooter added",        s1 is not None)
check("Premium scooter added",         s2 is not None)
check("Station now has 2 scooters",    len(station.get_scooter_ids()) == 2)
check("Scooter 1 status is available", s1.get_status() == "available")


# -- Step 3: Register a member --------------------------------------
print("\n[Step 3] Registering a member...")
member, msg = system.register_user("Alice", "alice@test.com", "pass123", "wallet")
check("Member registered",           member is not None)
check("Member role is 'member'",     member.get_role() == "member")
check("Duplicate email rejected",    system.register_user("X", "alice@test.com", "x")[0] is None)


# -- Step 4: Login --------------------------------------------------
print("\n[Step 4] Logging in...")
logged_in, msg = system.login("alice@test.com", "pass123")
check("Login succeeds with correct password", logged_in is not None)
check("Login fails with wrong password",      system.login("alice@test.com", "wrong")[0] is None)


# -- Step 5: Browse available scooters ------------------------------
print("\n[Step 5] Browsing scooters...")
available = system.get_available_scooters()
check("Two scooters are available", len(available) == 2)


# -- Step 6: Reserve a scooter -------------------------------------
print("\n[Step 6] Reserving scooter 1...")
user_id = member.get_user_id()
scooter_id = s1.get_scooter_id()
reservation, msg = system.reserve_scooter(user_id, scooter_id)
check("Reservation created",              reservation is not None)
check("Reservation status is confirmed",  reservation.get_status() == "confirmed")
check("Scooter 1 is now reserved",        s1.get_status() == "reserved")
check("Cannot reserve again (not avail)", system.reserve_scooter(user_id, scooter_id)[0] is None)


# -- Step 7: Start rental from reservation -------------------------
print("\n[Step 7] Starting rental from reservation...")
res_id = reservation.get_reservation_id()
rental, msg = system.start_rental(user_id, scooter_id, station_id, reservation_id=res_id)
check("Rental created",                   rental is not None)
check("Rental status is active",          rental.get_status() == "active")
check("Scooter 1 is now in_use",          s1.get_status() == "in_use")
check("Station has 1 scooter left",       len(station.get_scooter_ids()) == 1)
check("Reservation is converted",         reservation.get_status() == "converted")


# -- Step 8: End rental --------------------------------------------
print("\n[Step 8] Ending rental...")
rental_id = rental.get_rental_id()
success, msg = system.end_rental(rental_id, station_id, "wallet")
check("Rental ended successfully",        success is True)
check("Rental status is completed",       rental.get_status() == "completed")
check("Scooter 1 is available again",     s1.get_status() == "available")
check("Scooter 1 back at station",        s1.get_current_station_id() == station_id)
check("Station has 2 scooters again",     len(station.get_scooter_ids()) == 2)
check("Cost is non-negative",             rental.get_total_cost() >= 0)
check("Payment ID is set",                rental.get_payment_id() is not None)


# -- Step 9: View rental history -----------------------------------
print("\n[Step 9] Viewing rental history...")
history = system.get_rental_history(user_id)
check("History contains 1 rental",       len(history) == 1)
check("History rental matches",          history[0].get_rental_id() == rental_id)


# -- Step 10: Report a fault ---------------------------------------
print("\n[Step 10] Reporting a fault on scooter 2...")
scooter2_id = s2.get_scooter_id()
record, msg = system.report_fault(user_id, scooter2_id, "Brake feels loose")
check("Maintenance record created",      record is not None)
check("Scooter 2 is now maintenance",    s2.get_status() == "maintenance")
check("Cannot reserve a maint. scooter", system.reserve_scooter(user_id, scooter2_id)[0] is None)


# -- Step 11: Admin sets maintenance on scooter 1 ------------------
print("\n[Step 11] Admin flagging scooter 1 for maintenance...")
rec2, msg = system.set_maintenance(s1.get_scooter_id(), "Wheel wobble", "admin-001")
check("Second maintenance record created", rec2 is not None)
check("Scooter 1 is now maintenance",      s1.get_status() == "maintenance")


# -- Step 12: Admin completes repair -------------------------------
print("\n[Step 12] Admin completing repair on scooter 2...")
record_id = record.get_record_id()
success, msg = system.complete_repair(record_id, station_id)
check("Repair completed successfully",   success is True)
check("Scooter 2 is available again",    s2.get_status() == "available")
check("Scooter 2 docked at station",     s2.get_current_station_id() == station_id)


# -- Step 13: View reports -----------------------------------------
print("\n[Step 13] Admin viewing reports...")
report = system.get_reports()
check("Report has scooter counts",       "total_scooters" in report)
check("Total scooters is 2",             report["total_scooters"] == 2)
check("1 scooter available",             report["available"] == 1)
check("1 scooter in maintenance",        report["maintenance"] == 1)
check("1 completed rental",             report["completed_rentals"] == 1)
check("Revenue is non-negative",         report["total_revenue"] >= 0)


# -- Done ----------------------------------------------------------
print("\n" + "=" * 50)
print("Test complete.")
print("=" * 50)
