from datetime import datetime
import uuid


class Event:
    def __init__(self, title, start_time, end_time, description: str = "This Event added by api"):
        self.id = str(uuid.uuid4())
        self.title: str = title
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.description = description

    def tojson(self):
        return { 
            "id": self.id,
            "api": {
                "summary": self.title,
                "description": self.description,
                'start': {
                    'dateTime':  self.start_time.isoformat() + 'Z',
                    'timeZone': "Asia/Dhaka",
                },
                'end': {
                    'dateTime': self.end_time.isoformat() + 'Z',
                    'timeZone': "Asia/Dhaka",
                }
            }
        }

    