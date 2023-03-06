# importing required librarie
import json
import os
import sys
import datetime
from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt, QElapsedTimer
import requests
from PyQt5 import QtWidgets


from api import calender_api
from dialog import Dialog

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
        # self.setStyleSheet("background-color:transparent;")
        self.label.setStyleSheet("color: green")
        # setting center alignment to the label
        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(font)

        # test
        self.testButton = QPushButton('Test', self)
        self.testButton.clicked.connect(self.test)

        # adding label to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.testButton)
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

        self.events = []

        # window configuration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Timer")
    
        self.dragging = False
        self.offset = None
        self.my_timer = QElapsedTimer()
        
        self.resetted = False
        self.title = "Lol"

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Start timer when left mouse button is pressed
            self.my_timer.start()
            event.accept()

        if event.button() == Qt.RightButton:
            self.reset()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Get elapsed time since left mouse button was pressed
            elapsed_time = self.my_timer.elapsed()

            if elapsed_time > 20:
                # Move window if left mouse button was held down for more than 20ms
                if self.dragging:
                    self.dragging = False
                else:
                    self.runFunction()
            else:
                # Run function if left mouse button was released before 20ms
                self.runFunction()
                
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # Move window if left mouse button is held down and mouse is moved
            if not self.dragging:
                self.dragging = True
                self.offset = event.pos()
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.showMinimized()
            event.accept()

    def runFunction(self):
        self.resume_time()

        
    def reset(self):
        if self.clock_running:
            return
        delta = timedelta(seconds=self.second)
        future = self.start_time + delta
        start = self.start_time.isoformat() + 'Z'
        end_time = future.isoformat() + 'Z'
        
        if delta < timedelta(minutes=10):
            self.open_dialog_window()
            event = self.get_event(start, end_time, self.title)
            self.save_event2json(event)
            self.backup_events()

        self.second = 0
        self.label.setText('0')
        self.resetted = True

    def save_event2json(self, event):
        # Save the event to a file
        with open('events.json', 'a') as f:
            json.dump(event, f)
            f.write('\n')  # Add a newline to separate the events
    
    def test(self):
        print('hi')
        self.readEvents()

    def readEvents(self):
        if not os.path.exists('events.json'):
            return
        
        with open('events.json', 'r') as f:
            events = []
            for line in f:
                event = json.loads(line)
                events.append(event)
        return events

    def removeEvent(self, event):
        # Remove the processed event from the file
        if not os.path.exists('events.json'):
            print('no file')
            return

        with open('events.json', 'r') as f:
            lines = f.readlines()
        with open('events.json', 'w') as f:
            for line in lines:
                if line.strip() != json.dumps(event):
                    f.write(line)

    def backup_events(self):
        # Read the events from the file
        events = self.readEvents()
        # Process each event
        for event in events:
            # Send a POST request with the event data
            try:
                requests.get("http://www.google.com")
                calender_api(event)
                self.removeEvent(event)
                print('data is backed up')
            except requests.ConnectionError:
                print('Data is not backed up')
            except Exception as e:
                print(f'Error processing event: {event}')
                print(str(e))
		

    def resume_time(self):
        if self.clock_running:
            self.timer.stop()
            self.label.setStyleSheet("color: red")
            self.clock_running = False
        else:
            self.timer.start(1000)
            self.label.setStyleSheet("color: green")
            self.clock_running = True
            if self.resetted:
                print('Starting new time')
                self.start_time = datetime.datetime.utcnow() 
                self.resetted = False
            

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
                'dateTime':  start,
                'timeZone': "Asia/Dhaka",
            },
            'end': {
                'dateTime': end,
                'timeZone': "Asia/Dhaka",
            }
        }
        return event
    
    def open_dialog_window(self):
        # Create a new window with a text field in it
        self.dialog = Dialog(self)
        self.dialog.exec_()
        
        self.title = self.dialog.get_text()


    


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# showing all the widgets
window.show()

# start the app
App.exit(App.exec_())
