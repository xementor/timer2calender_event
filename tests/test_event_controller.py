import json
import tempfile
import unittest
from datetime import datetime
from app.models.Event import Event

from app.controllers.EventController import EventController


class TestEventController(unittest.TestCase):
    def setUp(self):
        self.controller = EventController("resource/test_events.json")

    def test_add_event(self):
        event = Event(
            title="Test Event",
            start_time=datetime(2023, 3, 25, 14, 30),
            end_time=datetime(2023, 3, 25, 16, 30),
            description="This is a test event."
        )
        self.controller.save_event_to_json(event)
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Test Event")

    def test_remove_event(self):
        event = Event(
            title="Test Event",
            start_time=datetime(2023, 3, 25, 14, 30),
            end_time=datetime(2023, 3, 25, 16, 30),
            description="This is a test event.",
        )
        self.controller.save_event_to_json(event.get_event_api_format())
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events), 1)

        self.controller.remove_event(event)
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events), 0)


    def test_backup_events(self):
        event1 = Event(
            title="Test Event 1",
            start_time=datetime(2023, 3, 25, 14, 30),
            end_time=datetime(2023, 3, 25, 16, 30),
            description="This is a test event.",
        )
        event2 = Event(
            title="Test Event 2",
            start_time=datetime(2023, 3, 26, 10, 0),
            end_time=datetime(2023, 3, 26, 12, 0),
            description="This is another test event.",
        )

        self.controller.save_event_to_json(event1)
        self.controller.save_event_to_json(event2)

        # Test backup when internet is available
        self.controller.backup_events()
        events = self.controller.get_events_from_db()
        self.assertEqual(len(events), 0)

   


    def tearDown(self):
        # remove any events added during the test
        events = self.controller.get_events_from_db()
        for event in events:
            self.controller.remove_event(event)
