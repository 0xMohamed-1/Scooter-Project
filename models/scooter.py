# scooter.py
# Defines the Scooter base class and its two subtypes.
# Status values: "available", "reserved", "in_use", "maintenance"


class Scooter:
    # Base class — cost_per_minute() is overridden in subclasses (polymorphism)

    def __init__(self, scooter_id, battery_level, status, current_station_id):
        self._scooter_id = scooter_id
        self._battery_level = battery_level      # integer 0-100
        self._status = status                    # one of the four string values above
        self._current_station_id = current_station_id  # None when out on a ride

    # --- Getters ---

    def get_scooter_id(self):
        return self._scooter_id

    def get_battery_level(self):
        return self._battery_level

    def get_status(self):
        return self._status

    def get_current_station_id(self):
        return self._current_station_id

    # --- Setters ---

    def set_battery_level(self, level):
        self._battery_level = level

    def set_status(self, status):
        self._status = status

    def set_current_station_id(self, station_id):
        self._current_station_id = station_id

    # --- Behaviour ---

    def get_type(self):
        # Overridden by subclasses to return "standard" or "premium"
        return "scooter"

    def cost_per_minute(self):
        # Overridden by subclasses — base returns 0.0 as a default
        return 0.0

    def drain_battery(self, duration_minutes):
        # Decrease battery by 1% per minute, never below 0
        drain = int(duration_minutes)
        self._battery_level = max(0, self._battery_level - drain)

    def to_dict(self):
        return {
            "scooter_id": self._scooter_id,
            "type": "scooter",
            "battery_level": self._battery_level,
            "status": self._status,
            "current_station_id": self._current_station_id
        }


class StandardScooter(Scooter):
    # Economy scooter — $0.50 per minute

    def __init__(self, scooter_id, battery_level, status, current_station_id):
        super().__init__(scooter_id, battery_level, status, current_station_id)

    def get_type(self):
        return "standard"

    def cost_per_minute(self):
        return 0.50

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "standard"
        return data


class PremiumScooter(Scooter):
    # Premium scooter — $1.00 per minute

    def __init__(self, scooter_id, battery_level, status, current_station_id):
        super().__init__(scooter_id, battery_level, status, current_station_id)

    def get_type(self):
        return "premium"

    def cost_per_minute(self):
        return 1.00

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "premium"
        return data
