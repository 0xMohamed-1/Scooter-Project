# models/__init__.py
# Makes all model classes available with a single import.

from .location import Location
from .user import User, Guest, RegisteredMember, Admin
from .scooter import Scooter, StandardScooter, PremiumScooter
from .station import Station
from .rental import Rental
from .reservation import Reservation
from .maintenance import MaintenanceRecord
from .payment import Payment
