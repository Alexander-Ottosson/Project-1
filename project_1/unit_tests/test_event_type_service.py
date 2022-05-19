import unittest

from exceptions.resource_not_found import ResourceNotFound
from models.event_type import EventType
from repositories.event_type_repo import EventTypeRepo
from services.event_type_service import EventTypeService


class TestEventTypeService(unittest.TestCase):
    etr = EventTypeRepo()
    ets = EventTypeService(etr)

    def test_get_all_types(self):
        types = self.etr.get_all_types()
        self.assertEqual(len(types), 6)

    def test_get_type(self):
        event_type = self.etr.get_type_by_id(1)
        self.assertEqual(event_type, EventType(
            type_id=1,
            name='University Course',
            coverage=0.8
        ))

    def test_neg_get_type(self):
        try:
            event_type = self.etr.get_type_by_id(100)
        except ResourceNotFound as e:
            self.assertEqual(e.message, 'Event Type Not Found')
