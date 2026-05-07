# rental.py
# Records one scooter rental from start to finish.
# Status values: "active", "completed", "cancelled"


class Rental:

    def __init__(self, rental_id, user_id, scooter_id, start_time, start_station_id):
        self._rental_id = rental_id
        self._user_id = user_id
        self._scooter_id = scooter_id
        self._start_time = start_time          # datetime object set when rental begins
        self._start_station_id = start_station_id
        self._end_time = None                  # set when rental ends
        self._end_station_id = None            # set when rental ends
        self._total_cost = 0.0
        self._status = "active"
        self._payment_id = None

    # --- Getters ---

    def get_rental_id(self):
        return self._rental_id

    def get_user_id(self):
        return self._user_id

    def get_scooter_id(self):
        return self._scooter_id

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_start_station_id(self):
        return self._start_station_id

    def get_end_station_id(self):
        return self._end_station_id

    def get_total_cost(self):
        return self._total_cost

    def get_status(self):
        return self._status

    def get_payment_id(self):
        return self._payment_id

    # --- Setters ---

    def set_payment_id(self, payment_id):
        self._payment_id = payment_id

    # --- Behaviour ---

    def end_rental(self, end_time, end_station_id, cost):
        # Finalise the rental with the end time, return station, and calculated cost
        self._end_time = end_time
        self._end_station_id = end_station_id
        self._total_cost = cost
        self._status = "completed"

    def cancel(self):
        self._status = "cancelled"

    def to_dict(self):
        # Convert datetime objects to strings for JSON storage
        start_str = str(self._start_time)
        end_str = str(self._end_time) if self._end_time else None
        return {
            "rental_id": self._rental_id,
            "user_id": self._user_id,
            "scooter_id": self._scooter_id,
            "start_time": start_str,
            "end_time": end_str,
            "start_station_id": self._start_station_id,
            "end_station_id": self._end_station_id,
            "total_cost": self._total_cost,
            "status": self._status,
            "payment_id": self._payment_id
        }
