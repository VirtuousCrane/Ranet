from contextlib import nullcontext
import PySide6
import errno
import os

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from dataclasses import dataclass
from typing import *
import csv

# For testing purposes
from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QPushButton, QApplication, QLabel
import sys

@dataclass
class MediaChannel:
	"""
	A MediaChannel represents an Http Live Stream (HLS) station.
	The information contained within an MediaChannel object includes:
	
	name : str
		The name of the MediaChannel (if present)
	url : str
		The URL to the MediaChannel
	"""
	name : str
	url : str

class MediaChannelPlaylistParser:
	def __init__(self, path: str = None):
		self.list_idx = 0
		self.station_list: list[MediaChannel] = []
		
		if path is not None:
			self.load(path)
	
	def load(self, path: str):
		"""Parses a Master Playlist and loads it into the program"""
		if not os.path.exists(path):
			raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
		
		f = open(path)
		line = f.readline()

		while line:
			if "#EXTINF" in line:
				name = line.split(",")[-1].strip()
				url = f.readline().strip()
				self.station_list.append(MediaChannel(name, url))
			line = f.readline()
		f.close()
	
	def get_list(self) -> list[MediaChannel]:
		"""Returns a list containing MediaChannel objects"""
		return self.station_list
	
	def get_current(self) -> MediaChannel:
		"""Returns the current media channel"""
		return self.station_list[self.list_idx]
	
	def get_next(self) -> MediaChannel:
		"""Returns the next media channel in the list"""
		self.list_idx += 1
		if self.list_idx > len(self.station_list) - 1:
			self.list_idx = 0
		
		return self.station_list[self.list_idx]
	
	def get_prev(self) -> MediaChannel:
		"""Returns the previous media channel in the list"""
		self.list_idx -= 1
		if self.list_idx < 0:
			self.list_idx = 0
		
		return self.station_list[self.list_idx]


class MediaChannelList:
	# Initializes with a csv file containing media channels
	def __init__(self, file_path):
		self.main_media_channels = []
		self.main_current_index = 0

		self.file_path = file_path
		self.setChannelsFromFile()

	def getNextChannel(self):
		# Empty list
		if len(self.main_media_channels) <= 0:
			return None
		
		# Increment index and loopback if reach end of list
		self.main_current_index += 1
		self.main_current_index %= len(self.main_media_channels)
		return self.main_media_channels[self.main_current_index]
		
	def getPreviousChannel(self):
		# Empty list
		if len(self.main_media_channels) <= 0:
			return None

		# Decrement index and loopback if reach start of list
		self.main_current_index -= 1
		self.main_current_index %= len(self.main_media_channels)
		return self.main_media_channels[self.main_current_index]

	def getCurrentChannel(self):
		# Empty list
		if len(self.main_media_channels) <= 0:
			return None
		
		return self.main_media_channels[self.main_current_index]

	def getChannelByIndex(self, inIndex):
		try:
			return self.main_media_channels[inIndex]
		except IndexError:
			print("Error at getChannelByIndex, by IndexError")
	
	# Return channels with substring of search_term ordered by substring index position
	def getChannelsBySearch(self, search_term):
		output = []
		temp = []

		# Generate list [media_channel, index_substring] that has substring
		for channel in self.main_media_channels:
			sub_str_index = channel.name.lower().find(search_term.lower())
			if sub_str_index >= 0: # substring search_term is in channel name
				temp.append([channel,sub_str_index])
		
		# Sort the list by substring index
		temp.sort(key=lambda x: x[1])

		# Prune out the substring index
		for channel_with_index in temp:
			output.append(channel_with_index[0])

		return output
		
	# get a list of media channels from csv file
	# private
	def parseChannelsFromFile(self, file_path):
		output = []

		with open(file_path,'r') as file:
			csv_reader = csv.reader(file)
			for line in csv_reader:
				temp_channel = MediaChannel(line[0],line[1])
				output.append(temp_channel)

		return output
	
	# private
	def setChannelsFromFile(self):
		if self.file_path is None:
			return
		else:
			self.main_media_channels = self.parseChannelsFromFile(self.file_path)
		

class VideoPlayer(QVideoWidget):
	def __init__(self):
		super(VideoPlayer, self).__init__()

		# Declaring Instance Variables
		self.is_playing = False
		self.is_fullscreen = False
		self.volume = 1.0
		
		# Creating the Media Player
		self.player = QMediaPlayer()
		
		# Configuring the Video and Audio output
		self.audio_output = QAudioOutput()
		self.player.setVideoOutput(self)
		self.player.setAudioOutput(self.audio_output)

		# Declaring the current station variable
		self.current_station : MediaChannel = None
	
	def set_media(self, source: MediaChannel) -> None:
		"""
		Sets the station of the Video Player
		
		PARAMETERS
		----------
		source : HLSStation
			An HLSStation object which represents the station
		"""
		self.player.setSource(QUrl(source.url))
		self.current_station = source
	
	def play(self) -> bool:
		"""Plays the Http Live Stream (HLS)"""
		if self.current_station is None:
			print("No Media Selected!")
			return False
		
		if self.is_playing:
			return True
		
		self.player.play()
		self.is_playing = True

		return self.is_playing

	def pause(self) -> bool:
		"""Pauses the stream"""
		if not self.is_playing:
			return False
		
		self.player.pause()
		self.is_playing = False

		return self.is_playing

	def stop(self) -> bool:
		"""Stops the stream"""
		if not self.is_playing:
			return False
		
		self.player.stop()
		self.is_playing = False

		return self.is_playing
	
	def toggle(self) -> bool:
		"""Toggles the player"""
		if self.is_playing:
			return self.pause()
		return self.play()
	
	def set_volume(self, volume : float) -> None:
		"""
		Sets the volume of the stream

		PARAMETERS
		----------
		volume : float
			The target volume. The value must be between 0.0 and 1.0
		"""
		self.volume = volume
		self.audio_output.setVolume(self.volume)
	
	def increment_volume(self):
		"""Increments the volume by 0.1"""
		vol = self.volume + 0.1
		if vol >= 1.0:
			self.volume = 1.0
		
		self.set_volume(self.volume)
	
	def decrement_volume(self):
		"""Decrements the volume by 0.1"""
		print("DEC")
		vol = self.volume - 0.1
		if vol <= 0.0:
			self.volume = 0.0
		
		self.set_volume(self.volume)
	
	def set_fullscreen(self):
		"""Sets the video to fullscreen"""
		if self.is_fullscreen:
			return self.is_fullscreen
		
		self.setFullScreen(True)
		self.is_fullscreen = True
	
	def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
		"""ESC -> Escapes from fullscreen"""
		key = event.key()
		if key == Qt.Key_Escape and self.is_fullscreen:
			self.setFullScreen(False)
			self.is_fullscreen = False

# DELETE ME. FOR REFERENCE ONLY.
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# HOW TO LOAD .m3u FILES
		self.playlist = MediaChannelPlaylistParser("./assets/iptv/th.m3u")
		self.stream = self.playlist.get_current()

		self.build_ui()
	
	def build_ui(self):
		self.setFixedSize(500, 520)

		self.video_frame = QFrame(self)
		self.video_frame.setFixedSize(500, 510)
		self.video_layout = QVBoxLayout(self.video_frame)

		self.player = VideoPlayer()

		self.play_btn = QPushButton("Play")
		self.play_btn.clicked.connect(self.play)

		self.next_channel_btn = QPushButton("Next Channel")
		self.next_channel_btn.clicked.connect(self.next_channel)

		self.fullscreen_btn = QPushButton("Fullscreen")
		self.fullscreen_btn.clicked.connect(self.player.set_fullscreen)

		self.channel_lbl = QLabel("")
		self.channel_lbl.setFixedHeight(10)

		self.video_layout.addWidget(self.player)
		self.video_layout.addWidget(self.play_btn)
		self.video_layout.addWidget(self.next_channel_btn)
		self.video_layout.addWidget(self.fullscreen_btn)
		self.video_layout.addWidget(self.channel_lbl)

		self.show()
	
	def play(self):
		self.player.pause()
		self.player.set_media(self.stream)
		self.channel_lbl.setText(self.stream.name)
		self.player.play()
	
	def next_channel(self):
		self.stream = self.playlist.get_next()
		self.play()

if __name__ == "__main__":
	app = QApplication(sys.argv)

	win = MainWindow()
	sys.exit(app.exec_())