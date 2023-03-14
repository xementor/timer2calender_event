class Event:
    def __init__(self, title, start_time, end_time):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def get_event_api_format(self):
        return {
            "summary": self.title,
            "description": "this event added by api",
            'description': 'this event added by api',
            'start': {
                'dateTime':  self.start_time,
                'timeZone': "Asia/Dhaka",
            },
            'end': {
                'dateTime': self.end_time,
                'timeZone': "Asia/Dhaka",
            }
        }

    