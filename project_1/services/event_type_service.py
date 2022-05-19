from repositories.event_type_repo import EventTypeRepo


class EventTypeService:
    def __init__(self, event_type_repo: EventTypeRepo):
        self.event_type_repo = event_type_repo

    def get_all_types(self):
        return self.event_type_repo.get_all_types()

    def get_event_type(self, type_id):
        return self.event_type_repo.get_type_by_id(type_id)
