"""
THIS FILE IS FOR TESTING PURPOSES ONLY
"""
from src.video_player import (MediaChannelShelf, FavoriteMediaChannelShelf,
								 HLSPlaylistParser, VideoPlayer,
								MediaChannelShelf)

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QFrame, QLabel, QApplication, 
QPushButton, QListWidget, QListWidgetItem, QLineEdit, QComboBox)
import sys

# DELETE ME. FOR REFERENCE ONLY.
class MainWindow(QWidget):
	def __init__(self, video_player):
		super().__init__()

		self.player = video_player # This is also a QFrame
		self.vbox = QVBoxLayout(self)
		self.channel_name_label = QLabel("stud channel name")
		self.play_button = QPushButton("Play")
		self.stop_button = QPushButton("Stop")
		self.next_channel_button = QPushButton("Next channel")
		self.previous_channel_button = QPushButton("Previous channel")
		self.favorite_toggle_button = QPushButton("Favorite toggle")
		self.entry_bar = QLineEdit("")
		self.channel_list = QListWidget()
		self.favorite_combo_box = QComboBox()

		# Resizing the window
		self.player.resize(1000,1000)
		self.player.setMinimumSize(400,400)

		# Resizing the label
		self.channel_name_label.setFixedHeight(15)

		# Adding widgets
		self.vbox.addWidget(self.player)
		self.vbox.addWidget(self.channel_name_label)
		self.vbox.addWidget(self.play_button)
		self.vbox.addWidget(self.stop_button)
		self.vbox.addWidget(self.next_channel_button)
		self.vbox.addWidget(self.previous_channel_button)
		self.vbox.addWidget(self.favorite_toggle_button)
		self.vbox.addWidget(self.entry_bar)
		self.vbox.addWidget(self.channel_list)
		self.vbox.addWidget(self.favorite_combo_box)

		self.setLayout(self.vbox)
		self.show()
	
	def set_channel_name_label(self, in_text):
		self.channel_name_label.setText(in_text)

	def set_play_button_callback(self, callback):
		self.play_button.clicked.connect(callback)
	
	def set_next_channel_button_callback(self, callback):
		self.next_channel_button.clicked.connect(callback)

	def set_previous_channel_button_callback(self, callback):
		self.previous_channel_button.clicked.connect(callback)

	def set_stop_button_callback(self, callback):
		self.stop_button.clicked.connect(callback)

	def set_favorite_toggle_button_callback(self, callback):
		self.favorite_toggle_button.clicked.connect(callback)

	def set_channel_list(self, channels_name):
		self.channel_list.clear()
		for channel_name in channels_name:
			self.channel_list.addItem(QListWidgetItem(channel_name))

	def set_entry_bar_callback(self,callback):
		self.entry_bar.textEdited.connect(callback)

	def get_entry_bar_input(self) -> str:
		return self.entry_bar.text()

	def set_channel_list_callback(self,callback):
		self.channel_list.itemClicked.connect(callback)

	def get_channel_list_selection(self) -> str:
		return self.channel_list.currentItem().text()

	def set_favorite_list_callback(self, callback):
		self.favorite_combo_box.activated.connect(callback)

	def get_favorite_list_selection(self) -> str:
		return self.favorite_combo_box.currentText()

	def set_favorite_list(self, channels_name):
		self.favorite_combo_box.clear()
		for channel_name in channels_name:
			self.favorite_combo_box.addItem(channel_name)
	
		
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
		self.gui.set_favorite_toggle_button_callback(self.toggle_current_channel_favorite)
		self.gui.set_entry_bar_callback(self.update_gui)
		self.gui.set_channel_list_callback(self.select_current_channel_from_all_list)
		self.gui.set_favorite_list_callback(self.select_current_channel_from_favorite)
		
	def update_gui(self):
		self.gui.set_channel_name_label(self.video_player.get_current_station().name)
		self.gui.set_channel_list(self.media_shelf.get_channels_name_by_search(self.gui.get_entry_bar_input()))
		self.gui.set_favorite_list(self.favorite_shelf.get_channels_name_by_search("")) # The entire list
		
	def start(self):
		self.gui.show()
		self.app.exec()
		self.play()
		self.update_gui()

	def play(self):
		self.video_player.play()
		print("Playing")
		self.update_gui()

	def stop(self):
		self.video_player.stop()
		print("Stoping")
		self.update_gui()

	def next_channel(self):
		self.video_player.set_media(self.media_shelf.get_next_channel())
		print(self.media_shelf.get_current_channel())
		self.update_gui()

	def previous_channel(self):
		self.video_player.set_media(self.media_shelf.get_previous_channel())
		print(self.media_shelf.get_current_channel())
		self.update_gui()

	def add_current_channel_to_favorite(self):
		self.favorite_shelf.add_media_channel(self.video_player.get_current_station())
		self.update_gui()

	def delete_current_channel_from_favorite(self):
		self.favorite_shelf.delete_media_channel(self.video_player.get_current_station())
		self.update_gui()

	def toggle_current_channel_favorite(self):
		self.favorite_shelf.toggle_media_channel(self.video_player.get_current_station())
		self.update_gui()

	def select_current_channel_from_all_list(self):
		self.video_player.set_media(self.media_shelf.get_channel_by_name(self.gui.get_channel_list_selection()))
		self.media_shelf.set_main_current_index(self.video_player.get_current_station())
		self.update_gui()

	def select_current_channel_from_favorite(self):
		print(self.gui.get_favorite_list_selection())
		self.video_player.set_media(self.media_shelf.get_channel_by_name(self.gui.get_favorite_list_selection()))
		self.media_shelf.set_main_current_index(self.video_player.get_current_station())
		self.update_gui()

if __name__ == "__main__":
	print("cmd test.py")
	my_ranet = MyRanet()
	my_ranet.start()


	
