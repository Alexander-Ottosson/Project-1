class Supervisor:
    def __init__(
            self,
            supervisor_id=0,
            subordinate_id=0
    ):
        self.supervisor_id = supervisor_id
        self.subordinate_id = subordinate_id

    def json(self):
        return {
            'supervisorId': self.supervisor_id,
            'subordinateId': self.subordinate_id
        }

    def __repr__(self):
        return str(self.json())
