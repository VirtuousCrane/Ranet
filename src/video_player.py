from contextlib import nullcontext
import PySide6
import errno
import vlc
import sys
import os

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from dataclasses import dataclass
from typing import *
import csv

from src.connection import connection_check_hls, ConnectionStatus

# For testing purposes
from PySide6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QPushButton, QApplication, QLabel, QWidget
import sys

@dataclass
class HLSStation:
	"""
	A HLSStation represents an Http Live Stream (HLS) station.
	The information contained within an HLSStation object includes:
	
	name : str
		The name of the HLS Station (if present)
	url : str
		The URL to the HLS
	"""
	name : str
	url : str

class HLSPlaylistParser:
	def __init__(self, path: str = None):
		self.list_idx = 0
		self.station_list: list[HLSStation] = []
		
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
				self.station_list.append(HLSStation(name, url))
			line = f.readline()
		f.close()
	
	def get_list(self) -> list[HLSStation]:
		"""Returns a list containing HLSStation objects"""
		return self.station_list
	
	def get_current(self) -> HLSStation:
		"""Returns the current station"""
		return self.station_list[self.list_idx]
	
	def get_next(self) -> HLSStation:
		"""Returns the next station in the list"""
		self.list_idx += 1
		if self.list_idx > len(self.station_list) - 1:
			self.list_idx = 0
		
		return self.station_list[self.list_idx]
	
	def get_prev(self) -> HLSStation:
		"""Returns the previous station in the list"""
		self.list_idx -= 1
		if self.list_idx < 0:
			self.list_idx = 0
		
		return self.station_list[self.list_idx]

class MediaChannelShelf:
	# Initializes with a csv file containing media channels
	def __init__(self, file_path):
		self.main_media_channels = []
		self.main_current_index = 0

		self.file_path = file_path
		self.set_channels_from_file()

	def get_next_channel(self):
		# Empty list
		if len(self.main_media_channels) <= 0:
			return None
		
		# Increment index and loopback if reach end of list
		self.main_current_index += 1
		self.main_current_index %= len(self.main_media_channels)
		return self.main_media_channels[self.main_current_index]
		
	def get_previous_channel(self):
		# Empty list
		if len(self.main_media_channels) <= 0:
			return None

		# Decrement index and loopback if reach start of list
		self.main_current_index -= 1
		self.main_current_index %= len(self.main_media_channels)
		return self.main_media_channels[self.main_current_index]

	def get_current_channel(self):
		# Empty list
		if len(self.main_media_channels) <= 0:
			return None
		
		return self.main_media_channels[self.main_current_index]

	def get_channel_by_index(self, inIndex):
		try:
			return self.main_media_channels[inIndex]
		except IndexError:
			print("Error at getChannelByIndex, by IndexError")
	
	# Return channels with substring of search_term ordered by substring index position
	def get_channels_by_search(self, search_term):
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

	def get_channel_by_search_index(self, search_term, index):
		searched_media_channels = self.get_channels_by_search(search_term)
		try:
			return searched_media_channels[index]
		except IndexError:
			return None
		
	# get a list of media channels from csv file
	# private
	def parse_channels_from_file(self, file_path : str) -> list:
		output = []

		with open(file_path,'r') as file:
			csv_reader = csv.reader(file)
			for line in csv_reader:
				temp_channel = HLSStation(line[0],line[1])
				output.append(temp_channel)

		return output
	
	# private
	def set_channels_from_file(self) -> None:
		if self.file_path is None:
			return
		else:
			self.main_media_channels = self.parse_channels_from_file(self.file_path)

	# private
	def get_media_channels_list(self) -> list:
		return self.main_media_channels

class FavoriteMediaChannelShelf(MediaChannelShelf):
	
	def add_media_channel(self, in_channel : HLSStation) -> None:
		if not (self.is_media_channel_in_list(in_channel)): 
			self.main_media_channels.append(in_channel)
		self.save_media_channels_to_file()
	
	def is_media_channel_in_list(self, in_channel : HLSStation) -> bool:
		return in_channel in self.main_media_channels
	
	def delete_media_channel(self, in_channel : HLSStation) -> None:
		if (self.is_media_channel_in_list(in_channel)):
			self.main_media_channels.remove(in_channel)
		self.save_media_channels_to_file()

	#private
	def save_media_channels_to_file(self) -> None:
		with open(self.file_path, 'w', newline='') as file:
			csv_writer = csv.writer(file)
			for media_channel in self.main_media_channels:
				csv_writer.writerow([media_channel.name, media_channel.url])

class VideoPlayer(QFrame):
	def __init__(self): 
		super(VideoPlayer, self).__init__()
		
		# Declaring Instance Variables
		self.platform = sys.platform
		self.is_playing = False
		self.is_fullscreen = False
		self.volume = 1.0

		print(self.platform)
		
		# Declaring the current station variable
		self.current_station : HLSStation = None	   
		
		# Creating the Media Player according to the platform
		if self.platform.startswith('linux'):
			layout = QVBoxLayout(self)
			self.setLayout(layout)
			
			self.videoWidget = QVideoWidget()
			self.player = QMediaPlayer()
			layout.addWidget(self.videoWidget)
		
			# Configuring the Video and Audio output
			self.audio_output = QAudioOutput()
			self.player.setVideoOutput(self.videoWidget)
			self.player.setAudioOutput(self.audio_output)

		elif self.platform == "win32":			  
			self.instance = vlc.Instance()
			self.player = self.instance.media_player_new()

			self.player.set_hwnd(self.winId())

	def set_media(self, source: HLSStation) -> None:
		"""
		Sets the station of the Video Player
		
		PARAMETERS
		----------
		source : HLSStation
			An HLSStation object which represents the station
		"""
		self.stop()
		self.current_station = source
		print(self.check_media_availability())

		# Example code: (To be decided if this should be implemented)
		#if self.check_media_availability() != ConnectionStatus.OK:
		#	// Creates popup
		#	return None

		if self.platform.startswith("linux"):
			self.player.setSource(QUrl(source.url))
		elif self.platform == "win32":
			self.media = self.instance.media_new(source.url)
			self.player.set_media(self.media)
		self.play()
	
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
		print(self.is_playing)
		if self.is_playing:
			return self.stop()
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
		if self.platform.startswith("linux"):
			self.audio_output.setVolume(self.volume)
		elif self.platform == "win32":
			self.player.audio_set_volume(int(self.volume * 100))
		print(f"Current Volume: {int(self.volume * 100)}")
	
	def increment_volume(self):
		"""Increments the volume by 0.1"""
		vol = self.volume + 0.1
		self.volume = vol
		if vol >= 1.0:
			self.volume = 1.0
		
		self.set_volume(self.volume)
	
	def decrement_volume(self):
		"""Decrements the volume by 0.1"""
		vol = self.volume - 0.1
		self.volume = vol
		if vol <= 0.0:
			self.volume = 0.0
		
		self.set_volume(self.volume)
	
	def set_fullscreen(self):
		"""Sets the video to fullscreen"""
		if self.is_fullscreen:
			return self.is_fullscreen
		
		if self.platform.startswith("linux"):
			self.setFullScreen(True)
		elif self.platform == "win32":
			# TODO: FULLSCREEN in windows doesn't work yet
			self.player.toggle_fullscreen()
		
		self.is_fullscreen = True
	
	def check_media_availability(self) -> ConnectionStatus:
		"""
		Checks if the HTTP Live Stream (HLS) is available

		Returns
		-------
		ConnectionStatus
			The availability of the HLS.
			Returns ConnectionStatus.OK is fine.
			Returns ConnectionStatus.ERR otherwise.
		"""
		if self.current_station is None:
			return ConnectionStatus.ERR
		
		return connection_check_hls(self.current_station.url)
	
	def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
		"""ESC -> Escapes from fullscreen"""
		key = event.key()
		if key == Qt.Key_Escape and self.is_fullscreen:
			if self.platform.startswith("linux"):
				self.setFullScreen(False)
			elif self.platform == "win32":
				self.player.toggle_fullscreen()
			
			self.is_fullscreen = False

# DELETE ME. FOR REFERENCE ONLY.
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# HOW TO LOAD .m3u FILES
		self.playlist = HLSPlaylistParser("./assets/iptv/th.m3u")
		self.stream = self.playlist.get_current()
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

		# Buttons
		self.play_btn = QPushButton("Toggle Play")
		self.play_btn.clicked.connect(self.toggle)

		self.next_channel_btn = QPushButton("Next Channel")
		self.next_channel_btn.clicked.connect(self.next_channel)

		self.fullscreen_btn = QPushButton("Fullscreen")
		self.fullscreen_btn.clicked.connect(self.player.set_fullscreen)

		self.increment_volume_btn = QPushButton("Increment Volume")
		self.increment_volume_btn.clicked.connect(self.player.increment_volume)

		self.decrement_volume_btn = QPushButton("Decrement Volume")
		self.decrement_volume_btn.clicked.connect(self.player.decrement_volume)

		# The Channel Label
		self.channel_lbl = QLabel("")
		self.channel_lbl.setFixedHeight(10)

		# Packing
		self.widget_layout.addWidget(self.video_frame)
		self.widget_layout.addWidget(self.play_btn)
		self.widget_layout.addWidget(self.next_channel_btn)
		self.widget_layout.addWidget(self.fullscreen_btn)
		self.widget_layout.addWidget(self.increment_volume_btn)
		self.widget_layout.addWidget(self.decrement_volume_btn)
		self.widget_layout.addWidget(self.channel_lbl)

		self.play()
		self.show()
	
	def play(self):
		self.player.pause()
		self.player.set_media(self.stream)
		self.channel_lbl.setText(self.stream.name)
		self.player.play()

	def toggle(self):
		self.player.toggle()
	
	def next_channel(self):
		self.stream = self.playlist.get_next()
		self.play()
    
if __name__ == "__main__":
	app = QApplication(sys.argv)

	win = MainWindow()
	sys.exit(app.exec_())
