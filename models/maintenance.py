# maintenance.py
# Records a fault report and tracks its resolution.
# Status values: "reported", "in_progress", "resolved"


class MaintenanceRecord:

    def __init__(self, record_id, scooter_id, reported_by, reported_at, description):
        self._record_id = record_id
        self._scooter_id = scooter_id
        self._reported_by = reported_by    # user_id of the person who filed the report
        self._reported_at = reported_at    # datetime object
        self._description = description
        self._resolved_at = None           # set when repair is complete
        self._status = "reported"

    # --- Getters ---

    def get_record_id(self):
        return self._record_id

    def get_scooter_id(self):
        return self._scooter_id

    def get_reported_by(self):
        return self._reported_by

    def get_reported_at(self):
        return self._reported_at

    def get_description(self):
        return self._description

    def get_resolved_at(self):
        return self._resolved_at

    def get_status(self):
        return self._status

    # --- Status changes ---

    def start_repair(self):
        self._status = "in_progress"

    def resolve(self, resolved_at):
        # Mark the repair as done and record when it finished
        self._resolved_at = resolved_at
        self._status = "resolved"

    def to_dict(self):
        return {
            "record_id": self._record_id,
            "scooter_id": self._scooter_id,
            "reported_by": self._reported_by,
            "reported_at": str(self._reported_at),
            "description": self._description,
            "resolved_at": str(self._resolved_at) if self._resolved_at else None,
            "status": self._status
        }
