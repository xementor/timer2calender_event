import datetime
from datetime import timedelta
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QTime, Qt, QElapsedTimer

from app.controllers.EventController import EventController
from app.models.Event import Event
from app.views.DialogWindow import DialogWindow

from utils import format_duration

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(10, 10, 40, 40)

        layout = QVBoxLayout()

        font = QFont('Arial', 12, QFont.Bold)
        self.label = QLabel()
        self.setStyleSheet("background-color:transparent;")
        self.label.setStyleSheet("color: green")
        self.label.setAlignment(Qt.AlignCenter)

        self.label.setFont(font)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.second = 0
        self.clock_running = True
        self.start_time = datetime.datetime.utcnow()

        # window configuration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Timer")
    
        self.dragging = False
        self.offset = None
        self.my_timer = QElapsedTimer()
        self.resetted = False
        self.title = "Lol"

        # controller
        self.event_controller = EventController()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Start timer when left mouse button is pressed
            self.my_timer.start()
            event.accept()

        if event.button() == Qt.RightButton:
            self.reset()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            elapsed_time = self.my_timer.elapsed()

            if elapsed_time > 20:
                if self.dragging:
                    self.dragging = False
                else:
                    self.runFunction()
            else:
                self.runFunction()
                
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
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
        
        if delta > timedelta(minutes=10):
            self.open_dialog_window()
            event = Event(self.title, start, end_time)
            self.event_controller.save_event_to_json(event)
            self.event_controller.backup_events()

        self.second = 0
        self.label.setText('0')
        self.resetted = True

    
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
        self.second += 1
        label_time = format_duration(self.second)

        self.label.setText(label_time)

  

    def open_dialog_window(self):
        self.dialog = DialogWindow(self)
        self.dialog.exec_()
        
        self.title = self.dialog.get_text()


    



