import unittest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction

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
    
    def test_left_double_click_minimize(self):
        QTest.mouseDClick(self.window, Qt.LeftButton)
        self.assertTrue(self.window.isMinimized())
    

    def test_right_click_menu(self):
        # Create a QMenu object for the right-click menu
        menu = QMenu(self.window)

        # Add a QAction for showing the events window
        show_events_action = QAction("Show Events", self.window)
        menu.addAction(show_events_action)

        # Simulate a right-click at position (100, 100) in the window
        QTest.mouseClick(self.window, Qt.RightButton)

        # Check that the menu is displayed
        # self.assertEqual(menu.isVisible(), True)

        # Check that the menu contains the "Show Events" action
        actions = menu.actions()
        # self.assertIn(show_events_action, actions)

if __name__ == '__main__':
    unittest.main()
