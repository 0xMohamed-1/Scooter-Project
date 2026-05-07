# payment.py
# Records a payment transaction linked to a rental.
# Method values: "wallet"
# Status values: "pending", "completed", "failed", "refunded"


class Payment:

    def __init__(self, payment_id, rental_id, user_id, amount, method, timestamp):
        self._payment_id = payment_id
        self._rental_id = rental_id
        self._user_id = user_id
        self._amount = amount       # float — total charged
        self._method = method
        self._timestamp = timestamp # datetime object
        self._status = "pending"

    # --- Getters ---

    def get_payment_id(self):
        return self._payment_id

    def get_rental_id(self):
        return self._rental_id

    def get_user_id(self):
        return self._user_id

    def get_amount(self):
        return self._amount

    def get_method(self):
        return self._method

    def get_timestamp(self):
        return self._timestamp

    def get_status(self):
        return self._status

    # --- Status changes ---

    def complete(self):
        self._status = "completed"

    def fail(self):
        self._status = "failed"

    def refund(self):
        self._status = "refunded"

    def to_dict(self):
        return {
            "payment_id": self._payment_id,
            "rental_id": self._rental_id,
            "user_id": self._user_id,
            "amount": self._amount,
            "method": self._method,
            "timestamp": str(self._timestamp),
            "status": self._status
        }
