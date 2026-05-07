# user.py
# Defines the User base class and three subtypes: Guest, RegisteredMember, Admin.


class User:
    # Base class for all users

    def __init__(self, user_id, name, email, password):
        self._user_id = user_id
        self._name = name
        self._email = email
        self._password = password  # stored as plain text (course assignment only)

    # --- Getters ---

    def get_user_id(self):
        return self._user_id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_role(self):
        # Overridden in subclasses
        return "user"

    def check_password(self, pw):
        # Returns True if the given password matches the stored one
        return self._password == pw

    def to_dict(self):
        return {
            "user_id": self._user_id,
            "name": self._name,
            "email": self._email,
            "password": self._password,
            "role": self.get_role()
        }


class Guest(User):
    # An unregistered visitor — can browse but cannot rent

    def get_role(self):
        return "guest"

    def browse_scooters(self, system):
        # Ask the system for the full scooter list
        return system.get_all_scooters()

    def view_stations(self, system):
        # Ask the system for the full station list
        return system.get_all_stations()


class RegisteredMember(User):
    # A logged-in member who can reserve and rent scooters

    def __init__(self, user_id, name, email, password, payment_method="wallet"):
        super().__init__(user_id, name, email, password)
        self._payment_method = payment_method
        self._rental_history = []              # list of rental IDs
        self._wallet_balance = 0.0             # AED balance set by admin

    def get_role(self):
        return "member"

    def get_payment_method(self):
        return self._payment_method

    def set_payment_method(self, method):
        self._payment_method = method

    def get_wallet_balance(self):
        return self._wallet_balance

    def set_wallet_balance(self, amount):
        self._wallet_balance = round(float(amount), 2)

    def get_rental_history(self):
        return self._rental_history

    def add_rental_to_history(self, rental_id):
        # Called after a rental is completed
        self._rental_history.append(rental_id)

    def to_dict(self):
        data = super().to_dict()
        data["payment_method"] = self._payment_method
        data["wallet_balance"] = self._wallet_balance
        data["rental_history"] = self._rental_history
        return data


class Admin(User):
    # An administrator who manages the fleet, stations, and maintenance

    def get_role(self):
        return "admin"
