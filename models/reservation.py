# reservation.py
# Holds a scooter for a member for up to 15 minutes.
# Status values: "pending", "confirmed", "converted", "expired", "cancelled"

from datetime import datetime


class Reservation:

    def __init__(self, reservation_id, user_id, scooter_id, created_at, expires_at):
        self._reservation_id = reservation_id
        self._user_id = user_id
        self._scooter_id = scooter_id
        self._created_at = created_at   # datetime object
        self._expires_at = expires_at   # datetime object (created_at + 15 min)
        self._status = "pending"

    # --- Getters ---

    def get_reservation_id(self):
        return self._reservation_id

    def get_user_id(self):
        return self._user_id

    def get_scooter_id(self):
        return self._scooter_id

    def get_created_at(self):
        return self._created_at

    def get_expires_at(self):
        return self._expires_at

    def get_status(self):
        return self._status

    # --- Status changes ---

    def confirm(self):
        self._status = "confirmed"

    def cancel(self):
        self._status = "cancelled"

    def expire(self):
        self._status = "expired"

    def convert_to_rental(self):
        # Called when the member starts a rental from this reservation
        self._status = "converted"

    def is_expired(self):
        # Check if the 15-minute window has passed
        return datetime.now() > self._expires_at

    def to_dict(self):
        return {
            "reservation_id": self._reservation_id,
            "user_id": self._user_id,
            "scooter_id": self._scooter_id,
            "created_at": str(self._created_at),
            "expires_at": str(self._expires_at),
            "status": self._status
        }
