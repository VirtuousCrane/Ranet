from typing import *
from dataclasses import dataclass
import vlc
import threading

@dataclass
class RadioStation:
	"""A dataclass to store information about a radio station"""
	name: str
	url: str
	type: str

class RadioPlayer:
	"""
	A class used to play the internet radio
	"""

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
		self.station = station
		self.volume = volume
		self.radio_thread = None

		# Thread Flags
		self.is_playing = False
		self.thread_spawned = False
		self.thread_finished = True

		# VLC media instance and player
		self.instance = vlc.Instance('--input-repeat=-1', '--no-video')
		self.player = self.instance.media_player_new()

		if self.station is not None:
			self.media = self.instance.media_new(self.station.url)
			self.player.set_media(self.media)

	def play(self):
		"""Spawns a thread, calls play_stream() to play the radio"""

		assert self.station is not None, "No station specified"

		if not self.thread_spawned:
			self.radio_thread = threading.Thread(target=self.play_stream)
			self.radio_thread.start()
			self.thread_spawned = True
			self.thread_finished = False

	def play_stream(self):
		"""Plays the radio"""

		assert self.station is not None, "No station specified"

		self.is_playing = True
		self.player.play()

		# The main radio play loop
		while(True):
			if not self.is_playing:
				break
			self.player.audio_set_mute(False)
			self.player.audio_set_volume(self.volume)

		# Pauses the player and sets the thread flag
		self.player.stop()
		self.thread_finished = True

	def stop(self):
		"""Pauses the radio stream and kills the thread"""

		# Checks if a thread exists
		if self.radio_thread is None:
			return

		# Signals the thread to stop working
		self.is_playing = False
		while(not self.thread_finished):
			pass

		# Joins thread and reset the thread flags
		self.radio_thread.join()
		self.thread_spawned = False
		self.thread_finished = False

	def set_station(self, station: RadioStation):
		"""
		Stops the current stream and sets a new station

		Parameters
		----------
		station : RadioStation
			The new station to set to
		"""

		if not self.thread_finished:
			self.stop()

		self.station = station
		self.media = self.instance.media_new(self.station.url)
		self.player.set_media(self.media)

	def change_station(self, station: RadioStation):
		"""
		Stops the current stream and switch to a new station

		Parameters
		----------
		station : RadioStation
			The station to change to
		"""

		self.set_station(station)
		self.play()

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

