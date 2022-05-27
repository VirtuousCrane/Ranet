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

class RadioTracker(object):
	"""Loads Radio Stations from and XML file"""
	RADIO_STATIONS_XML_FILE_PATH = "assets/gnome-internet-radio-locator.xml"

	def __init__(self):
		self.radio_stations_list: List[RadioStation]  = []
		self.current_index = 0

		self.__initialize_radio_stations_list()

	def __initialize_radio_stations_list(self):
		"""Loads radio stations from an XML file and populate the radio station list"""
		tree = ET.parse(self.RADIO_STATIONS_XML_FILE_PATH)

		# Iterates through each station
		for station in tree.findall('station'):
			station_name = station.get("name")
			station_url = station.find("stream").get("uri")  # IDK why but the "url" is listed as "uri"

			# Creates a new RadioStation object and append it to the radio station list
			radio_station = RadioStation(station_name, station_url)
			self.radio_stations_list.append(radio_station)

	def increment_index(self):
		"""Changes the current index to point to the next radio station in the list"""
		self.current_index += 1
		self.current_index = self.current_index % len(self.radio_stations_list)


	def decrement_index(self):
		"""Changes the current index to point to the previous radio station in the list"""
		self.current_index -= 1
		self.current_index = self.current_index % len(self.radio_stations_list)

	def get_current_station(self) -> RadioStation:
		"""
		Returns a RadioStation object of the station currently being played

		Returns
		-------
		RadioStation
			The station being currently played
		"""
		return self.radio_stations_list[self.current_index]


class Radio(object):
	"""A high level abstraction that handles the operation of the radio"""
	def __init__(self, gui=None):
		self.radio_tracker = RadioTracker()
		self.radio_player = RadioPlayer(self.radio_tracker.get_current_station())
		self.gui = gui

		# Linking the radio model with the GUI callbacks
		if gui is not None:
			self.gui.set_play_button_callback(self.toggle)
			self.gui.set_previous_button_callback(self.previous_channel)
			self.gui.set_next_button_callback(self.next_channel)
			self.gui.set_volume_slider_callback(self.change_volume)
			self.gui.set_radio_player(self)

			self.change_volume()

	def play(self):
		"""Plays the radio"""
		print("Playing radio")
		self.radio_player.play()
		self.update_gui()

	def stop(self):
		"""Stops the radio"""
		print("Stopping the radio")
		self.radio_player.stop()
		self.update_gui()

	def toggle(self):
		"""Toggles the operation of the radio. If it's playing, stop, and vice versa"""
		print("Toggle radio, play if stop, stop if play")
		self.radio_player.toggle()
		self.update_gui()

	def next_channel(self):
		"""Switches to the next radio station"""
		print("Switching to next possible radio channel")
		self.radio_tracker.increment_index()
		self.radio_player.set_media(self.radio_tracker.get_current_station())
		self.update_gui()

	def previous_channel(self):
		"""Switches to the previous radio station"""
		print("Switching to previous possible radio channel")
		self.radio_tracker.decrement_index()
		self.radio_player.set_media(self.radio_tracker.get_current_station())
		self.update_gui()

	def display_current_channel(self):
		"""Displays the current radio station's name"""
		print("Display info of current radio channel")
		print(f"Name: {self.radio_player.get_station_name()} Url: {self.radio_player.get_station_url()}")

	def change_volume(self):
		newVolume = self.gui.get_volume_slider_value()
		self.radio_player.set_volume(newVolume)
		self.update_gui()
		print("Change volume to " + str(newVolume))

	def set_station(self, station: RadioStation):
		self.radio_player.set_media(station)
		self.update_gui()

	def update_gui(self):
		"""Updates the GUI"""
		if self.gui is None:
			print("GUI is none in Radio(), cannot update GUI")
		else:
			# Update channel name
			self.gui.set_channel_name(self.radio_player.get_station_name())

			# Update the play button
			if self.radio_player.get_is_playing():
				print("Setting play button icon to pause")
				self.gui.set_play_button_icon_to_pause()
			else:
				print("Setting play button icon to play")
				self.gui.set_play_button_icon_to_play()
		
	def get_radio_player(self):
		return self.radio_player


