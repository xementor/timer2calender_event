from datetime import datetime


class Event:
    def __init__(self, title, start_time, end_time, description: str = "This Event added by api"):
        self.title: str = title
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        self.description = description

    def get_event_api_format(self):
        return {
            "summary": self.title,
            "description": self.description,
            'start': {
                'dateTime':  self.start_time.isoformat() + 'Z',
                'timeZone': "Asia/Dhaka",
            },
            'end': {
                'dateTime': self.end_time.isoformat()  + 'Z',
                'timeZone': "Asia/Dhaka",
            }
        }

    