import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

# Color For Testing Layout and etc
class Color(QWidget):
    def __init__(self, color):
        QWidget.__init__(self, None)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

# class ChannelWave(QWidget):
#     def __init__(self):
#         QWidget.__init__(self, None)
#         self.channel_wave_layout = QVBoxLayout()
#         # self.channel_wave_layout.SetFixedSize(360,100)

#         self.channel_layout = QVBoxLayout()
#         # self.channel_layout.SetFixedSize(360, 80)

#         self.testing = QLabel(self)
#         self.testing.setText("Testing")

#         self.channel_layout.addWidget(self.testing)

#         self.channel_wave_layout.addLayout(self.channel_layout)

class CreateMenuBar(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.menu_bar = self.menuBar()
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

        self.menu_bar.addMenu(file_menu)

        # EditMenu Section
        edit_menu = QMenu("&Edit", self)
        ### EditMenu Action List
        self.theme_action = QAction("&Theme", self)

        edit_menu.addAction(self.theme_action)

        self.menu_bar.addMenu(edit_menu)

        # RecordMenu Section
        record_menu = QMenu("&Record", self)
        ### RecordMenu Action List
        self.start_recording_action = QAction("&Start Recording", self)
        self.stop_recording_action = QAction("&Stop Recording", self)
        self.go_to_folder_action = QAction("&Go To Folder", self)

        record_menu.addAction(self.start_recording_action)
        record_menu.addAction(self.stop_recording_action)
        record_menu.addAction(self.go_to_folder_action)

        self.menu_bar.addMenu(record_menu)
        

class MainGuiWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Ranet")
        self.setGeometry(0,0,360, 220)

        self.create_menu_bar = CreateMenuBar()
        self.setMenuBar(self.create_menu_bar.menu_bar)

# Other Widget

        main_layout = QVBoxLayout()

# Channel and Wave

        channel_wave_layout = QVBoxLayout()

        wave_container = QLabel(self)
        wave_container.setText("Wave Image")
        wave_container.setStyleSheet("background-color: red;")
        wave_container.setGeometry(0, 40, 360, 80)

        channel_name = QLabel(self)
        channel_name.setAlignment(Qt.AlignCenter)
        channel_name.setStyleSheet("background-color: green;")
        channel_name.setGeometry(0, 120, 360, 24)
        channel_name.setText("Channel Name")

        channel_num = QLineEdit(self)
        channel_num.setAlignment(Qt.AlignCenter)
        channel_num.setGeometry(122, 64, 116, 32)
        channel_num.setStyleSheet("font-size: 24px;")
        channel_num.setText("128.48")


        channel_wave_layout.addWidget(wave_container)
        channel_wave_layout.addWidget(channel_name)
        channel_wave_layout.addWidget(channel_num)

        main_layout.addLayout(channel_wave_layout)



# Show
        self.setLayout(main_layout)
        self.show()


# Temporary // Testing

def main():
    app = QApplication(sys.argv)

    w = MainGuiWindow()
    w.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())