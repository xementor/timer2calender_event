import unittest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from app.views.MainWindow import Window


class TestWindow(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.window = Window()

    def tearDown(self):
        self.window.close()

    def test_initial_state(self):
        self.assertTrue(self.window.clock_running)

    def test_resume_time(self):
        QTest.mouseClick(self.window, Qt.LeftButton)
        self.assertFalse(self.window.clock_running)
        QTest.mouseClick(self.window, Qt.LeftButton)
        self.assertTrue(self.window.clock_running)

    def test_reset(self):
        QTest.mouseClick(self.window, Qt.LeftButton)
        QTest.mouseClick(self.window, Qt.RightButton)
        self.assertEqual(self.window.second, 0)
        self.assertEqual(self.window.label.text(), "0")
        self.assertTrue(self.window.resetted)

if __name__ == '__main__':
    unittest.main()
