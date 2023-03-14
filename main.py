import sys
from PyQt5.QtWidgets import QApplication
from app.views.MainWindow import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())