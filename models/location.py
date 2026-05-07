# location.py
# A simple value object that stores a Google Maps URL for a station's location.


class Location:

    def __init__(self, maps_url, station_id=None):
        self._maps_url = maps_url
        self._station_id = station_id  # None for a standalone coordinate

    # --- Getters ---

    def get_maps_url(self):
        return self._maps_url

    def get_station_id(self):
        return self._station_id

    # --- Setter ---

    def set_station_id(self, station_id):
        self._station_id = station_id

    def to_dict(self):
        return {
            "maps_url": self._maps_url,
            "station_id": self._station_id
        }
