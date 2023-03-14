import json
import os
import datetime
from datetime import timedelta
import requests

from app.controllers.api import calender_api
from app.models.Event import Event

class EventController:
    def __init__(self):
        self.events = []
        self.db_location = "resource/events.json"

    def remove_event(self, event):
        self.events.remove(event)

    def get_events_from_db(self):
        if not os.path.exists(self.db_location):
            return []

        with open(self.db_location, "r") as f:
            events = []
            for line in f:
                event = json.loads(line)
                events.append(event)
        return events

    def save_event_to_json(self, event: Event):
        with open(self.db_location, "a") as f:
            json.dump(event.get_event_api_format(), f)
            f.write("\n")

    def backup_events(self):
        events = self.get_events_from_db()
        for event in events:
            try:
                requests.get("http://www.google.com")
                res = calender_api(event)
                if res is not None and res == "confirmed":
                    self.remove_event(event)
                print("data is backed up")
            except requests.ConnectionError:
                print("Data is not backed up")
                return