# importing required librarie
import sys
import datetime
from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt
import requests

from api_f import calender_api

class Window(QWidget):

    def __init__(self):
        super().__init__()

        # setting geometry of main window
        self.setGeometry(10, 10, 40, 40)

        # creating a vertical layout
        layout = QVBoxLayout()

        # creating font object
        font = QFont('Arial', 12, QFont.Bold)

        # creating a label object
        self.label = QLabel()
        self.button = QPushButton("Stop")
        self.resetButton = QPushButton("Reset")
        self.button.setStyleSheet(
            'QPushButton {background-color: red; color: black;}')

        # setting center alignment to the label
        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(font)

        # adding label to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.resetButton)

        # setting the layout to main window
        self.setLayout(layout)

        # creating a timer object
        self.timer = QTimer(self)

        # adding action to timer
        self.timer.timeout.connect(self.showTime)

        # update the timer every second
        self.timer.start(1000)
        self.second = 0
        self.clock_running = True
        self.start_time = datetime.datetime.utcnow()

        self.button.clicked.connect(self.resume_time)
        self.resetButton.clicked.connect(self.reset)
        self.resetButton.setEnabled(False)
        self.events = []

    def reset(self):
        # TODO: add second to the start time
        delta = timedelta(seconds=self.second)
        future = self.start_time + delta
        start = self.start_time.isoformat() + 'Z'
        end_time = future.isoformat() + 'Z'

        event = self.get_event(start, end_time, "Lol")
        if delta > timedelta(minutes=1):
            # TODO: add to the sync que
            # self.create_event(event)
            self.events.append(event)
            self.create_event()
        self.resetButton.setEnabled(False)
        self.second = 0
        self.label.setText('0')

    def changeButton(self):
        if self.clock_running:
            self.button.setStyleSheet(
                'QPushButton {background-color: green; color: white;}')
            self.button.setText("Start")
            self.clock_running = False
        else:
            self.button.setText('Stop')
            self.button.setStyleSheet(
                'QPushButton {background-color: red; color: black;}')
            self.clock_running  = True

		

    def resume_time(self):
        if self.clock_running:
            self.button.setStyleSheet(
                'QPushButton {background-color: green; color: white;}')
            self.timer.stop()
            self.button.setText("Start")
            self.clock_running = False
            self.resetButton.setEnabled(True)
        else:
            self.timer.start(1000)
            self.button.setText('Stop')
            self.clock_running = True
            self.button.setStyleSheet(
                'QPushButton {background-color: red; color: black;}')

    # method called by timer
    def showTime(self):
        current_time = QTime.currentTime()
        # converting QTime object to string
        self.second += 1
        label_time = self.format_duration(self.second)

        # showing it to the label
        self.label.setText(label_time)

    def format_duration(self, seconds):
        hours = seconds // 3600  # Get the number of hour
        minutes = (seconds % 3600) // 60  # Get the number of minutes
        seconds = (seconds % 3600) % 60  # Get the number of seconds
        # Format the time string
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        return time_str

    def get_event(self, start, end, task):
        event = {
            'summary': task,
            'description': 'this event added by api',
            'start': {
                'dateTime': datetime.datetime.utcnow().isoformat() + 'Z',
                'timeZone': "Asia/Dhaka",
            },
            'end': {
                'dateTime': '2023-02-26T17:55:20.894917Z',
                'timeZone': "Asia/Dhaka",
            }
        }
        return event
    
    async def create_event(self):
        try:
            # Try making a request to a known website to check for internet connectivity
            requests.get("http://www.google.com")
            
            # If there is internet connectivity, make all the API calls in the request queue
            while self.events:
                data = self.events.pop(0)
                await calender_api(event)
            # Wait for a few seconds before checking for internet connectivity again
            print('data is backed up')
        except requests.ConnectionError:
            # If there is no internet connectivity, append the request data to the request queue
            print('Data is not backed up')


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.show()

# start the app
App.exit(App.exec_())
