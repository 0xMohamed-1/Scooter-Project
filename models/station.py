# station.py
# A physical docking station where scooters are parked and picked up.


class Station:

    def __init__(self, station_id, name, location, capacity):
        self._station_id = station_id
        self._name = name
        self._location = location    # a Location object
        self._capacity = capacity    # maximum number of scooters allowed
        self._scooter_ids = []       # list of scooter IDs currently docked here

    # --- Getters ---

    def get_station_id(self):
        return self._station_id

    def get_name(self):
        return self._name

    def get_location(self):
        return self._location

    def get_capacity(self):
        return self._capacity

    def get_scooter_ids(self):
        return self._scooter_ids

    # --- Scooter management ---

    def add_scooter(self, scooter_id):
        # Dock a scooter here — only if there is space
        if self.is_full():
            print("Station is full, cannot add scooter.")
            return False
        self._scooter_ids.append(scooter_id)
        return True

    def remove_scooter(self, scooter_id):
        # Remove a scooter when a member picks it up
        if scooter_id in self._scooter_ids:
            self._scooter_ids.remove(scooter_id)
            return True
        return False

    def is_full(self):
        # True when docked scooters reach the station's capacity
        return len(self._scooter_ids) >= self._capacity

    def get_available_count(self):
        # How many more scooters can still be docked here
        return self._capacity - len(self._scooter_ids)

    def to_dict(self):
        return {
            "station_id": self._station_id,
            "name": self._name,
            "location": self._location.to_dict(),
            "capacity": self._capacity,
            "scooter_ids": self._scooter_ids
        }
