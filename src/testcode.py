from re import S
from typing import *
from dataclasses import dataclass
import vlc
import threading
import xml.etree.ElementTree as ET
from src.radio import RadioTracker, Radio



@dataclass
class RadioStation:
	"""A dataclass to store information about a radio station"""
	name: str
	url: str
	type: str

class MyRadioPlayer:
	"""
	A class used to play the internet radio
	"""

	def __init__(self, station: RadioStation = None, volume: int = 50):
		"""
		Parameters
		----------
		station : RadioStation
			The data of the station to be played.
		volume : int
			The audio's volume
		"""
		# Intialize variable
		self.station = station

		self.is_playing = False


		# VLC media instance and player
		self.instance = vlc.Instance('--input-repeat=-1', '--no-video')
		self.player = self.instance.media_player_new()

		if self.station is not None:
			self.media = self.instance.media_new(self.station.url)
			self.player.set_media(self.media)


	def play(self):
		"""Spawns a thread, calls __play_stream() to play the radio"""
		self.player.play()
		self.is_playing = True


	def __play_stream(self):
		"""Plays the radio"""


	def stop(self):
		"""Pauses the radio stream and kills the thread"""	
		self.player.stop()
		self.is_playing = False


	def change_station(self, station: RadioStation):
		"""
		Stops the current stream and switch to a new station

		Parameters
		----------
		station : RadioStation
			The station to change to
		"""
		self.player.stop()
		self.station = station
		self.media = self.instance.media_new(self.station.url)
		self.player.set_media(self.media)

	def get_station_name(self) -> str:
		"""Returns the current station's name"""
		assert self.station is not None, "No station specified"
		return self.station.name

	def get_station_url(self) -> str:
		"""Returns the current station's stream url"""
		assert self.station is not None, "No station specified"
		return self.station.url

	def get_station_media_type(self) -> str:
		"""Returns the current station stream's media type"""
		assert self.station is not None, "No station specified"
		return self.station.type

	def set_volume(self, volume: int):
		"""
		Sets the volume of the player

		Parameters
		----------
		volume : int
			The volume of the audio
		"""
		self.volume = volume

	def toggle(self):
		if self.is_playing:
			self.stop()
		else:
			self.play()

class MyRadio:
	def __init__(self, gui=None):
		self.radio_tracker = RadioTracker()
		self.radio_player = MyRadioPlayer(self.radio_tracker.get_current_station())
		self.gui = gui

	def play(self):
		print("Playing radio")
		self.radio_player.play()
		self.update_gui()

	def stop(self):
		print("Stopping the radio")
		self.radio_player.stop()
		self.update_gui()

	def toggle(self):
		print("Toggle radio, play if stop, stop if play")
		self.radio_player.toggle()
		self.update_gui()
        
	def next_channel(self):
		print("Switching to next possible radio channel")
		self.radio_tracker.increment_index()
		self.radio_player.change_station(self.radio_tracker.get_current_station())
		self.update_gui()

	def previous_channel(self):
		print("Switching to previous possible radio channel")
		self.radio_tracker.decrement_index()
		self.radio_player.change_station(self.radio_tracker.get_current_station())
		self.update_gui()

	def display_current_channel(self):
		print("Display info of current radio channel")
		print(f"Name: {self.radio_player.get_station_name()} Url: {self.radio_player.get_station_url()} Media type:{self.radio_player.get_station_media_type()}")

	def update_gui(self):
		if self.gui is None:
			print("GUI is none, cannot update GUI")
		else:
			self.gui.set_channel_name(self.radio_player.get_station_name())

	def get_radio_player(self):
		return self.radio_player
		

