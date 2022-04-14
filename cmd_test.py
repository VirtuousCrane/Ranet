"""
THIS FILE IS FOR TESTING PURPOSES ONLY
"""
from src.video_player import (MediaChannelShelf, FavoriteMediaChannelShelf,
								 HLSPlaylistParser, VideoPlayer,
								MediaChannelShelf)

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QApplication, QPushButton
import sys

# DELETE ME. FOR REFERENCE ONLY.
class MainWindow(QWidget):
	def __init__(self, video_player):
		super().__init__()

		self.player = video_player # This is also a QFrame
		self.vbox = QVBoxLayout(self)
		self.play_button = QPushButton("Play")
		self.stop_button = QPushButton("Stop")
		self.next_channel_button = QPushButton("Next channel")
		self.previous_channel_button = QPushButton("Previous channel")
		

		# Resizing the window
		self.player.resize(1000,1000)
		self.player.setMinimumSize(500,500)

		# Adding widgets
		self.vbox.addWidget(self.player)
		self.vbox.addWidget(self.play_button)
		self.vbox.addWidget(self.stop_button)
		self.vbox.addWidget(self.next_channel_button)
		self.vbox.addWidget(self.previous_channel_button)

		self.setLayout(self.vbox)
		self.show()

	def set_play_button_callback(self, callback):
		self.play_button.clicked.connect(callback)
	
	def set_next_channel_button_callback(self, callback):
		self.next_channel_button.clicked.connect(callback)

	def set_previous_channel_button_callback(self, callback):
		self.previous_channel_button.clicked.connect(callback)

	def set_stop_button_callback(self, callback):
		self.stop_button.clicked.connect(callback)
		
class MyRanet:
	def __init__(self):
		self.app = QApplication()
		self.video_player = VideoPlayer()
		self.media_shelf = MediaChannelShelf("assets/all_tv.csv")
		self.favorite_shelf = FavoriteMediaChannelShelf("assets/favorite_channel.csv")
		self.gui = MainWindow(self.video_player)

		# Setting a channel
		self.video_player.set_media(self.media_shelf.get_current_channel())
		print(self.media_shelf.get_current_channel())

		# Setting callback
		self.gui.set_play_button_callback(self.play)
		self.gui.set_stop_button_callback(self.stop)
		self.gui.set_next_channel_button_callback(self.next_channel)
		self.gui.set_previous_channel_button_callback(self.previous_channel)
		

	def start(self):
		self.gui.show()
		self.app.exec()
		self.play()

	def play(self):
		self.video_player.play()
		print("Playing")

	def stop(self):
		self.video_player.stop()
		print("Pausing")

	def next_channel(self):
		self.video_player.set_media(self.media_shelf.get_next_channel())
		print(self.media_shelf.get_current_channel())

	def previous_channel(self):
		self.video_player.set_media(self.media_shelf.get_previous_channel())
		print(self.media_shelf.get_current_channel())
				

if __name__ == "__main__":
	print("cmd test.py")
	my_ranet = MyRanet()
	my_ranet.start()


	
