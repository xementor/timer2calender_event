from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QDialog
from PyQt5.QtCore import pyqtSignal

class Dialog(QDialog):
    # This signal will be emitted when the user enters data in the text field


    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        # Create a text field and a button in the new window
        self.textField = QLineEdit(self)
        self.button = QPushButton('Send', self)
        self.button.clicked.connect(self.close_window)

        # Create a layout for the new window
        layout = QVBoxLayout()
        layout.addWidget(self.textField)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setGeometry(200, 200, 300, 200)

    def close_window(self):
        # Close the second window and return the text entered in the text field
        self.accept()

    def get_text(self):
        # Return the text entered in the text field
        return self.textField.text()