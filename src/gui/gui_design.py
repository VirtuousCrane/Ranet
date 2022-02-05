import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

        

class MainGuiWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Ranet")
        self.setFixedSize(360, 220)

        menu_bar = self.menuBar()
        # FileMenu Section
        file_menu = QMenu("&File", self)
        ### FileMenu Action List
        self.play_action = QAction("&Play", self)
        self.pause_action = QAction("&Pause", self)
        self.next_action = QAction("&Next", self)
        self.previous_action = QAction("&Previous", self)
        self.favorite_action = QAction("&Favorite", self)

        file_menu.addAction(self.play_action)
        file_menu.addAction(self.pause_action)
        file_menu.addAction(self.next_action)
        file_menu.addAction(self.previous_action)
        file_menu.addAction(self.favorite_action)

        menu_bar.addMenu(file_menu)

        # EditMenu Section
        edit_menu = QMenu("&Edit", self)
        ### EditMenu Action List
        self.theme_action = QAction("&Theme", self)

        edit_menu.addAction(self.theme_action)

        menu_bar.addMenu(edit_menu)

        # RecordMenu Section
        record_menu = QMenu("&Record", self)
        ### RecordMenu Action List
        self.start_recording_action = QAction("&Start Recording", self)
        self.stop_recording_action = QAction("&Stop Recording", self)
        self.go_to_folder_action = QAction("&Go To Folder", self)

        record_menu.addAction(self.start_recording_action)
        record_menu.addAction(self.stop_recording_action)
        record_menu.addAction(self.go_to_folder_action)

        menu_bar.addMenu(record_menu)
        



# Temporary // Testing

def main():
    app = QApplication(sys.argv)

    w = MainGuiWindow()
    w.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())