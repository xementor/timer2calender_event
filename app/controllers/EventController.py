from ast import List
import json
import os
import datetime
from datetime import timedelta
import requests

from app.controllers.api import calender_api
from app.models.Event import Event

class EventController:
    def __init__(self):
        self.db_location = "resource/events.json"
        self.events = self.get_events_from_db()
    
    def __init__(self, db_location):
        self.db_location = db_location
        self.events = self.get_events_from_db()

    def remove_event(self, event):
        print(event)
        self.events.remove(event)
        with open(self.db_location, "w") as f:
            json.dump([e for e in self.events], f, indent=4)

    def get_events_from_db(self) -> list:
        events = []
        if not os.path.exists(self.db_location):
            return events

        try:
            with open(self.db_location, "r") as f:
                events = json.load(f)
                return events
        except json.decoder.JSONDecodeError:
            events = []
            return events
        
    

    def save_event_to_json(self, event: Event):
        if not bool(event.title):
            return
        try:
            with open(self.db_location, "r+") as f:
                data = json.load(f)
        except FileNotFoundError:
            # create new file with list containing the new event object
            data = [event.get_event_api_format()]
            with open(self.db_location, "w") as f:
                json.dump(data, f, indent=4)
        else:
            # file exists and is not empty, append new event object to list
            data.append(event.get_event_api_format())
            with open(self.db_location, "w") as f:
                json.dump(data, f, indent=4)

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