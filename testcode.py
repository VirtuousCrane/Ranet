from msilib.schema import Media
from src.video_player import MediaChannelShelf, FavoriteMediaChannelShelf, HLSPlaylistParser, VideoPlayer, MediaChannelShelf
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QApplication
import sys

# DELETE ME. FOR REFERENCE ONLY.
class MainWindow(QWidget):
    def __init__(self, video_player):
        super().__init__()

        self.player = video_player # This is also a QFrame
        self.vbox = QVBoxLayout(self)

        
        self.vbox.addWidget(self.player)

        self.setLayout(self.vbox)
        self.show()
        
class MyRanet:
    def __init__(self):
        self.app = QApplication()
        self.video_player = VideoPlayer()
        self.media_shelf = MediaChannelShelf("assets/all_tv_channel.csv")
        self.gui = MainWindow(self.video_player)

        # Setting a channel
        self.video_player.set_media(self.media_shelf.get_current_channel())
        print(self.media_shelf.get_current_channel())

    def start(self):
        self.gui.show()
        self.app.exec()

    def play(self):
        self.video_player.play()
        

if __name__ == "__main__":
    my_ranet = MyRanet()
    my_ranet.start()


