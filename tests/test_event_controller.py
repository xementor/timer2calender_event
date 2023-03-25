import os
import unittest
from datetime import datetime
from app.models.Event import Event


from app.controllers.EventController import EventController


class TestEventController(unittest.TestCase):
    def setUp(self):
        self.db_location = "resource/test_events.json"
        self.controller = EventController(self.db_location)

    def test_add_event(self):
        print("test add")
        event = Event(
            title="Test Event",
            start_time=datetime(2023, 3, 25, 14, 30),
            end_time=datetime(2023, 3, 25, 16, 30),
            description="This is a test event."
        )
        self.controller.save_event_to_json(event)
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].get('id'), event.id)

    def test_remove_event(self):
        event = Event(
            title="Test Event",
            start_time=datetime(2023, 3, 25, 14, 30),
            end_time=datetime(2023, 3, 25, 16, 30),
            description="This is a test event.",
        )

        event2 = Event(
            title="Test Event",
            start_time=datetime(2023, 3, 25, 14, 30),
            end_time=datetime(2023, 3, 25, 16, 30),
            description="This is a test event.",
        )
        self.controller.save_event_to_json(event)
        self.controller.save_event_to_json(event2)
        events = self.controller.get_events_from_db()

        # when
        self.assertEqual(len(events), 2)

        self.controller.remove_event(event2.id)
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events), 1)

        self.controller.remove_event(event.id)
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events), 0)

        # self.controller.remove_event(event)
        # events = self.controller.get_events_from_db()
        # self.assertEqual(len(events), 0)
    

    def tearDown(self):
        os.remove(self.db_location)
