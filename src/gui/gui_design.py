import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

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

class CreateChannelWave(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.channel_wave_layout = QVBoxLayout()
        self.channel_handler = ControlChannelHandler()

# Wave Image Container
        wave_container = QLabel()
        wave_container.setText("Wave Image")
        wave_container.setStyleSheet("border: 1px solid black;")
        wave_container.setFixedSize(360,80)

# Channel Name Container
        channel_name = QLabel()
        channel_name.setAlignment(Qt.AlignCenter)
        channel_name.setStyleSheet("border: 1px solid black;")
        channel_name.setFixedSize(360, 24)
        self.current_channel_name = self.channel_handler.current_channel_name
        channel_name.setText(self.current_channel_name)
        
# Channel Number Container
        self.channel_num = QLineEdit(wave_container)
        self.channel_num.setAlignment(Qt.AlignCenter)
        self.channel_num.setFixedSize(116,32)
        self.channel_num.setStyleSheet("font-size: 24px; background-color: #eee")
        self.current_channel_num = self.channel_handler.current_channel_num
        self.channel_num.setText(self.current_channel_num)

        self.channel_wave_layout.addWidget(wave_container)
        self.channel_wave_layout.addWidget(channel_name)
        
class CreateControlBar(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.control_layout = QVBoxLayout()
        self.control_layout.setAlignment(Qt.AlignCenter)
        self.control_layout.setSpacing(8)

        self.control_button_layout = QHBoxLayout()
        self.control_button_layout.setAlignment(Qt.AlignCenter)
        self.control_button_layout.setContentsMargins(0,8,0,0)
        self.control_button_layout.setSpacing(8)

        self.control_clicked_handler = ControlClickHandler()

# Buttons Play, Next, Previous
    # Previous Button
        previous_button = QPushButton("Previous", self)
        previous_button.setFixedSize(44,44)
        previous_button.setStyleSheet("border-radius: 22; border: 2px solid black")
        previous_button.clicked.connect(self.control_clicked_handler.previousButtonClick)

        self.control_button_layout.addWidget(previous_button)

    # Play Button
        play_button = QPushButton("Play", self)
        play_button.setFixedSize(50,50)
        play_button.setStyleSheet("border-radius: 25; border: 2px solid black;")
        play_button.clicked.connect(self.control_clicked_handler.PlayPauseButtonClicked)

        self.control_button_layout.addWidget(play_button)
    
    # Next Button
        next_button = QPushButton("Next", self)
        next_button.setFixedSize(44,44)
        next_button.setStyleSheet("border-radius: 22; border: 2px solid black;")
        next_button.clicked.connect(self.control_clicked_handler.nextButtonClick)

        self.control_button_layout.addWidget(next_button)

        self.control_layout.addLayout(self.control_button_layout)

# Sound Volume Control
        self.volume_value = QSlider(Qt.Horizontal)
        self.volume_value.setFixedSize(154, 20)

        self.control_layout.addWidget(self.volume_value)

class MainGuiWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        self.setWindowTitle("Ranet")
        self.setGeometry(0,0,360,220)

        self.create_menu_bar = CreateMenuBar()
        self.setMenuBar(self.create_menu_bar.menu_bar)

# QWidget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignTop)

# Channel and Wave
        self.create_channel_wave = CreateChannelWave()
        main_layout.addLayout(self.create_channel_wave.channel_wave_layout)

    ### To be Able to OverLap the channel_num over wave_container we use setGeometry to set the co-ordinate.
        self.create_channel_wave.channel_num.setGeometry(122, 24, 116, 32)

# Control
        self.create_control = CreateControlBar()
        main_layout.addLayout(self.create_control.control_layout)
        
# Show
        self.setLayout(main_layout)
        self.show()

# Testing For GUI_API (WIP)
class ControlClickHandler(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
    # Set Default Status as True (Currently Playing)
        self.currently_playing = True

    # Toggle Status When Play or Pause Button is Clicked || callback function
    def PlayPauseButtonClicked(self):
        if self.currently_playing == True:
            self.currently_playing = False
            print(self.currently_playing)
        else: 
            self.currently_playing =True
            print(self.currently_playing)

    # Return Status whether the radio should be playing or pause
    def GetCurrentStatus(self):
        return self.currently_playing

    # CallBack Function when the previous button is clicked
    def previousButtonClick(self):
        print("Previous button Click")

    # CallBack Function when the next button is clicked
    def nextButtonClick(self):
        print("Next button Click")

class ControlChannelHandler(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
    # Initialize default channel number
        self.current_channel_num = "0"
    # Initialize default channel name
        self.current_channel_name = "Channel Name"

    def SetCurrentChannel(self, new_channel_num):
        self.channel_num.setText(new_channel_num)

    def GetCurrentChannel(self):
        return self.current_channel_num

    def SetCurrentChannelName(self, new_channel_name):
        self.channel_name.setText(new_channel_name)

    def GetCurrentChannelName(self):
        return self.current_channel_name

# CSS
CSS = """
    QSlider::handle:horizontal {
        background: black;
        border: 1px solid black;
        width: 24px;
        height: 8 px;
        border-radius: 4px;
    }
    QSlider::groove:horizontal {
        border: 1px solid black;
        height: 10px;
        background: #eee;
        margin: 0px;
        border-radius: 4px;
    }
    QPushButton::hover{
        background: lightgray;
    }
    QPushButton::hover:pressed{
        background: black;
    }
"""

# Temporary // Testing
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(CSS)

    w = MainGuiWindow()
    w.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())