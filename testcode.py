from msilib.schema import Media
from src.video_player import MediaChannelShelf, FavoriteMediaChannelShelf, HLSPlaylistParser, VideoPlayer, MediaChannelShelf
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QApplication
import sys

# DELETE ME. FOR REFERENCE ONLY.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # HOW TO LOAD .m3u FILES
        self.shelf = MediaChannelShelf("assets/all_tv_channel.csv")
        self.stream = self.shelf
        self.player 
        print(self.stream)

        self.build_ui()
    
    def build_ui(self):
        # Setting the UI window size
        self.resize(1920, 1120)
        self.widget = QWidget(self)
        self.widget_layout = QVBoxLayout(self)

        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.widget_layout)

        # Setting the video frame (screen) size
        self.video_frame = QFrame(self)
        self.video_frame.resize(1920, 1080)
        
        self.video_frame_vbox = QVBoxLayout(self)
        self.video_frame.setLayout(self.video_frame_vbox)

        # WORSHIP ME. I MADE THIS BIT CROSS-PLATFORM WITH 2 BACKENDS.
        self.player = VideoPlayer()
        self.video_frame_vbox.addWidget(self.player)

        # The Channel Label
        self.channel_lbl = QLabel("")
        self.channel_lbl.setFixedHeight(10)

        # Packing
        self.widget_layout.addWidget(self.video_frame)
        self.show()
        
class MyRanet:
    def __init__(self):
        self.video_player = VideoPlayer()
        self.media_shelf = MediaChannelShelf("assets/all_tv_channel.csv")
        self.gui = 

    def
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = MainWindow()


    sys.exit(app.exec_())
