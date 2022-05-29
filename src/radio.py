from typing import *
from dataclasses import dataclass
from src.connection import *
from src.exceptions import *
from src.abstract_classes import MediaPlayer, MediaStation

import vlc
import xml.etree.ElementTree as ET

@dataclass
class RadioStation(MediaStation):
	"""A dataclass to store information about a radio station"""
	pass
#	name: str
#	url: str

class RadioPlayer(MediaPlayer):
	"""	A class used to play the internet radio	"""

	def __init__(self, station: RadioStation = None, volume: int = 100):
		"""
		Parameters
		----------
		station : RadioStation
			The data of the station to be played.
		volume : int
			The audio's volume
		"""

		# Variable Initialization
		self.station: RadioStation = station
		self.is_playing = False

		# VLC media instance and player
		self.instance = vlc.Instance('--input-repeat=-1', '--no-video')
		self.player = self.instance.media_player_new()

		if self.station is not None:
			self.media = self.instance.media_new(self.station.url)
			self.player.set_media(self.media)

	def play(self):
		self.player.play()
		self.is_playing = True

	def stop(self):	
		self.player.stop()
		self.is_playing = False

	def set_media(self, media: RadioStation):
		self.stop()
		self.station = media
		self.media = self.instance.media_new(self.station.url)
		self.player.set_media(self.media)
		self.play()

	def get_station_name(self) -> str:
		assert self.station is not None, "No station specified"
		return self.station.name

	def get_station_url(self) -> str:
		assert self.station is not None, "No station specified"
		return self.station.url

	def get_station_media_type(self) -> str:
		assert self.station is not None, "No station specified"
		return self.station.type
	
	def get_current_station(self) -> RadioStation:
		return self.station

	def set_volume(self, volume: int):
		self.player.audio_set_volume(volume)

	def toggle(self):
		if self.is_playing:
			self.stop()
		else:
			self.play()

	def get_is_playing(self):
		return self.is_playing

	def update_gui(self, in_gui):
		"""
		Update the channel name and play button

		PARAMETERS
		----------
		in_gui: MainGuiWindow 
		- The window to update
		"""
		if self.station is not None:
			in_gui.set_channel_name(self.station)

		if self.get_is_playing():
			in_gui.set_play_button_icon_to_pause()
		else:
			in_gui.set_play_button_icon_to_play()
		
		in_gui.update_favorite_btn()







