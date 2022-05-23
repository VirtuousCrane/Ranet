import sys
from turtle import width
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from src.gui.radio_channel_list_gui import RadioChannelListGuiWindow
from src.video_player import FavoriteMediaChannelShelf, HLSStation, MediaChannelShelf, VideoPlayer
from src.radio import RadioStation, RadioPlayer

# from radio_channel_list_gui import RadioChannelListGuiWindow
# from video_player import FavoriteMediaChannelShelf, MediaChannelShelf, VideoPlayer
# from radio import RadioPlayer

class CreateMenuBar(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self, None)
		self.menu_bar = self.menuBar()

		self.create_channel_wave = CreateChannelWave()
		self.control_clicked_handler = ControlClickHandler()

	# FileMenu Section
		file_menu = QMenu("&File", self)

		## FileMenu Action List
		self.play_action = QAction("&Play", self)
		self.play_action.triggered.connect(self.control_clicked_handler.play_action_button_click)
		self.pause_action = QAction("&Pause", self)
		self.pause_action.triggered.connect(self.control_clicked_handler.pause_action_button_click)
		self.next_action = QAction("&Next", self)
		self.next_action.triggered.connect(self.control_clicked_handler.next_button_click)
		self.previous_action = QAction("&Previous", self)
		self.previous_action.triggered.connect(self.control_clicked_handler.previous_button_click)
		self.channel_list_action = QAction("&Channel List", self)
		self.channel_list_action.triggered.connect(self.open_channel_list_gui)

		file_menu.addAction(self.play_action)
		file_menu.addAction(self.pause_action)
		file_menu.addAction(self.next_action)
		file_menu.addAction(self.previous_action)
		file_menu.addAction(self.channel_list_action)

		self.menu_bar.addMenu(file_menu)

	# EditMenu Section
		edit_menu = QMenu("&Edit", self)

		## EditMenu Action List
		self.theme_action = QAction("&Theme", self)
		edit_menu.addAction(self.theme_action)
		self.menu_bar.addMenu(edit_menu)

	# RecordMenu Section
		record_menu = QMenu("&Record", self)

		## RecordMenu Action List
		self.start_recording_action = QAction("&Start Recording", self)
		self.stop_recording_action = QAction("&Stop Recording", self)
		self.go_to_folder_action = QAction("&Go To Folder", self)

		record_menu.addAction(self.start_recording_action)
		record_menu.addAction(self.stop_recording_action)
		record_menu.addAction(self.go_to_folder_action)

		self.menu_bar.addMenu(record_menu)

	# All Channel List Action
		self.all_channel_list_action = QAction("&All Channel List", self)
		self.all_channel_list_action.triggered.connect(self.all_channel_list_resize_animation)

		self.menu_bar.addAction(self.all_channel_list_action)

	# All Channel List Animation
	def all_channel_list_resize_animation(self):
		mainWindow = QWidget()
		self.current_height = self.create_channel_wave.channel_wave_frame.height()
		self.current_width = self.create_channel_wave.channel_wave_frame.width()
		# self.create_channel_wave.wave_container_frame.resize(self.width, self.height)
		self.animation_all_channel_list = QPropertyAnimation(self.create_channel_wave.all_channel_list_frame, b"geometry")
		self.animation_all_channel_list.setDuration(500) # 0.5 second
		self.animation_video_player = QPropertyAnimation(self.create_channel_wave.wave_container_frame, b"geometry")
		self.animation_video_player.setDuration(500)
		

		if self.create_channel_wave.all_channel_list_frame.width() == 0: # Expand
			self.animation_all_channel_list.setStartValue(QRect(self.create_channel_wave.all_channel_list_frame.x(), self.create_channel_wave.all_channel_list_frame.y(), 0, self.current_height-150))
			self.animation_all_channel_list.setEndValue(QRect(self.create_channel_wave.all_channel_list_frame.x(), self.create_channel_wave.all_channel_list_frame.y(), 144, self.current_height-150))
			self.animation_all_channel_list.start()
			self.animation_video_player.setStartValue(QRect(self.create_channel_wave.wave_container_frame.x(), self.create_channel_wave.wave_container_frame.y(), self.current_width, self.current_height-150))
			self.animation_video_player.setEndValue(QRect(self.create_channel_wave.wave_container_frame.x() + 144, self.create_channel_wave.wave_container_frame.y(), self.current_width-144, self.current_height-150))
			self.animation_video_player.start()
		else: # Close
			self.animation_all_channel_list.setStartValue(QRect(self.create_channel_wave.all_channel_list_frame.x(), self.create_channel_wave.all_channel_list_frame.y(), 144, self.current_height-150))
			self.animation_all_channel_list.setEndValue(QRect(self.create_channel_wave.all_channel_list_frame.x(), self.create_channel_wave.all_channel_list_frame.y(), 0, self.current_height-150))
			self.animation_all_channel_list.start()

			self.animation_video_player.setStartValue(QRect(self.create_channel_wave.wave_container_frame.x(), self.create_channel_wave.wave_container_frame.y(), self.current_width-144, self.current_height-150))
			self.animation_video_player.setEndValue(QRect(self.create_channel_wave.wave_container_frame.x() -144, self.create_channel_wave.wave_container_frame.y(), self.current_width, self.current_height-150))
			self.animation_video_player.start()
		

	# file_menu callback Function
	def set_play_action_callback(self, in_func):
		self.play_action.clicked.connect(in_func)
		
	def set_pause_action_callback(self, in_func):
		self.pause_action.clicked.connect(in_func)
		
	def set_previous_action_callback(self, in_func):
		self.previous_action.clicked.connect(in_func)
		
	def set_next_action_callback(self, in_func):
		self.next_action.clicked.connect(in_func)

	def open_channel_list_gui(self):
		self.channel_list_gui = RadioChannelListGuiWindow()
		self.channel_list_gui.show()
	
	def get_channel_wave(self):
		return self.create_channel_wave

class CreateChannelWave(QWidget):
	def __init__(self):
		QWidget.__init__(self, None)
		self.channel_wave_layout = QVBoxLayout()
		self.channel_wave_layout.setStretch(1, 1)
		self.channel_wave_frame = QFrame()

		# Control
		self.create_control = CreateControlBar()

		# Center Layout
		self.all_channel_list_and_display_screen_layout = QHBoxLayout()

		# All Channel Layout and Frame
		self.all_channel_list_layout = QVBoxLayout()
		self.all_channel_list_frame = QFrame()
		self.all_channel_list_frame.setMaximumWidth(144)

		self.all_channel_list_search_bar = QLineEdit()
		self.all_channel_list = QListWidget()

		# Wave Image Container
		#self.wave_container_frame = QFrame()
		self.wave_container_frame = VideoPlayer()
		self.wave_container_layout = QVBoxLayout()

		# Channel Name Layout
		self.channel_fav_name_layout = QHBoxLayout() 

		# Channel Name Container
		self.channel_name = QLabel()
		self.channel_name.setAlignment(Qt.AlignCenter)
		self.channel_name.setStyleSheet("border: 1px solid grey;")
		self.channel_name.setMinimumHeight(30)
		self.channel_name.setText("Channel Name")

		# Channel Favorite DropDown
		self.channel_fav = QComboBox()
		self.channel_fav.setEditable(True)
		self.channel_fav.setPlaceholderText("Favorite Channel")
		self.channel_fav.setFixedSize(256,30)

		# ----Test----
		#self.channel_fav.addItem("channel1")
		#self.channel_fav.addItem("channel2")
		#self.channel_fav.addItem("channel3")
		# ------------

		# Channel List Test
		self.all_channel_list_layout.addWidget(self.all_channel_list_search_bar)
		self.all_channel_list_layout.addWidget(self.all_channel_list)
		self.all_channel_list_frame.setLayout(self.all_channel_list_layout)

		self.wave_container_frame.setLayout(self.wave_container_layout)

		self.all_channel_list_and_display_screen_layout.addWidget(self.all_channel_list_frame, 5)
		self.all_channel_list_and_display_screen_layout.addWidget(self.wave_container_frame, 19)

		self.channel_fav_name_layout.addWidget(self.channel_name)
		self.channel_fav_name_layout.addWidget(self.create_control.favorite_button)
		self.channel_fav_name_layout.addWidget(self.channel_fav)
		self.channel_fav_name_layout.addWidget(self.create_control.full_screen_button)
		self.channel_fav_name_layout.addWidget(self.create_control.change_mode_button)


		self.channel_wave_layout.addLayout(self.all_channel_list_and_display_screen_layout)
		self.channel_wave_layout.addLayout(self.channel_fav_name_layout)
		self.channel_wave_layout.addLayout(self.create_control.control_layout)

		self.channel_wave_frame.setLayout(self.channel_wave_layout)

	
	# Function for adding favorite channel List
	def add_channel_fav_list(self, in_func):
		self.channel_fav.addItem(QListWidgetItem(in_func))

	# Set channel name
	def set_channel_name(self, station: HLSStation):
		"""
		Sets the channel name label in the GUI

		Parameters
		----------
		station : str
			The new channel
		"""
		self.channel_name.setText(station.name)
		self.create_control.update_current(station)
	
	def all_channel_list_add_item(self, channel_name: str):
		self.all_channel_list.addItem(channel_name)
	
	def get_all_channel_list(self) -> QListWidget:
		return self.all_channel_list
	
	def clear_all_channel_list(self):
		self.all_channel_list.clear()

	def set_search_bar_callback(self, callback):
		self.all_channel_list_search_bar.textEdited.connect(callback)
	
	def get_search_bar(self):
		return self.all_channel_list_search_bar
	
	def set_channel_list_callback(self, callback):
		self.all_channel_list.itemClicked.connect(callback)
	
	def get_channel_list(self):
		return self.all_channel_list
	
	def get_video_player(self) -> VideoPlayer:
		return self.wave_container_frame
	
	def set_change_mode_callback(self, callback):
		self.create_control.set_change_mode_callback(callback)
	
	def load_favorite_list(self, fav_list: FavoriteMediaChannelShelf):
		"""
		Load items into the favorite list

		PARAMETERS
		----------
		fav_list : FavoriteMediaChannelShelf
			The list to load media from
		"""
		#self.channel_fav.addItem("I love lolis")
		self.channel_fav.clear()
		self.create_control.set_favorite_list(fav_list)
		for channel in fav_list.get_media_channels_list():
			self.channel_fav.addItem(channel.name)
	
	def set_channel_fav_callback(self, fn):
		self.channel_fav.activated.connect(fn)
	
	def update_current(self, channel: HLSStation):
		self.create_control.update_current(channel)
	
class CreateControlBar(QWidget):
	def __init__(self):
		QWidget.__init__(self, None)
		self.control_layout = QVBoxLayout()
		self.control_layout.setAlignment(Qt.AlignCenter)
		self.control_layout.setSpacing(8)
		self.current_channel = None
		self.fav_list = None

		self.control_button_layout = QHBoxLayout()
		self.control_button_layout.setAlignment(Qt.AlignCenter)
		self.control_button_layout.setContentsMargins(0,8,0,0)
		self.control_button_layout.setSpacing(8)
		
		self.control_clicked_handler = ControlClickHandler()

	# Buttons Play, Next, Previous
		# Previous Button
		self.previous_button = QPushButton(self)
		self.previous_button.setIcon(QIcon(QPixmap("assets/previous_icon.png")))
		self.previous_button.setIconSize(QSize(24,24))
		self.previous_button.setFixedSize(44,44)
		self.previous_button.setStyleSheet("border-radius: 22; border: 2px solid black")
		self.previous_button.clicked.connect(self.control_clicked_handler.previous_button_click)
		
		self.control_button_layout.addWidget(self.previous_button)

	# Play Button
		self.play_button = QPushButton(self)
		self.play_button.setIcon(QIcon(QPixmap("assets/play_icon.png")))
		self.play_button.setIconSize(QSize(28,28))
		self.play_button.setFixedSize(50,50)
		self.play_button.setStyleSheet("border-radius: 25; border: 2px solid black;")
		self.play_button.clicked.connect(self.control_clicked_handler.play_pause_button_click)
		self.play_button.clicked.connect(self.toggle_play_pause_icon)
		
		self.control_button_layout.addWidget(self.play_button)
	
	# Next Button
		# self.next_button = QPushButton("Next", self)
		self.next_button = QPushButton(self)
		self.next_button.setIcon(QIcon(QPixmap("assets/next_icon.png")))
		self.next_button.setIconSize(QSize(24,24))
		self.next_button.setFixedSize(44,44)
		self.next_button.setStyleSheet("border-radius: 22; border: 2px solid black;")
		self.next_button.clicked.connect(self.control_clicked_handler.next_button_click)
		
		self.control_button_layout.addWidget(self.next_button)

		self.control_layout.addLayout(self.control_button_layout)
		
	# Sound Volume Control
		self.volume_slider = QSlider(Qt.Horizontal)
		self.volume_slider.setFixedSize(154, 20)
		self.volume_slider.setMinimum(0)
		self.volume_slider.setValue(50)
		self.volume_slider.setMaximum(100)

		# Test Slider Volume Change
		self.control_layout.addWidget(self.volume_slider)

	# Favorite Button
		self.favorite_button = QPushButton()
		self.favorite_button.setFixedSize(30,30)
		self.update_favorite_icon()

	# Full Screen Button
		self.full_screen_button = QPushButton("Full")
		self.full_screen_button.setFixedSize(30,30)
		self.full_screen_button.setIcon(QIcon(QPixmap("assets/full_screen_icon.png")))
		self.full_screen_button.setIconSize(QSize(24,24))
	
	# Change Mode Button
		self.change_mode_button = QPushButton("M")
		self.change_mode_button.setFixedSize(30, 30)

		# Toggle Play Pause Icon
	def toggle_play_pause_icon(self):
		if (self.control_clicked_handler.currently_playing == True):
			self.play_button.setIcon(QIcon(QPixmap("assets/pause_icon.png")))
			self.play_button.setIconSize(QSize(24,24))
		else: 
			self.play_button.setIcon(QIcon(QPixmap("assets/play_icon.png")))
			self.play_button.setIconSize(QSize(28,28))

	def set_play_button_icon_to_play(self):
		self.play_button.setIcon(QIcon(QPixmap("assets/play_icon.png")))
		self.play_button.setIconSize(QSize(28,28))

	def set_play_button_icon_to_pause(self):
		self.play_button.setIcon(QIcon(QPixmap("assets/pause_icon.png")))
		self.play_button.setIconSize(QSize(24,24))
		
	def set_play_button_callback(self, in_func):
		self.play_button.clicked.connect(in_func)
		
	def set_previous_button_callback(self, in_func):
		self.previous_button.clicked.connect(in_func)
		
	def set_next_button_callback(self, in_func):
		self.next_button.clicked.connect(in_func)
		
	def set_volume_slider_callback(self, in_func):
		self.volume_slider.valueChanged.connect(in_func)

	def set_volume_slider_value(self, in_func):
		self.volume_slider.setValue(in_func)

	def set_favorite_button_callback(self, in_func):
		self.favorite_button.clicked.connect(in_func)
	
	def set_change_mode_callback(self, callback):
		self.change_mode_button.clicked.connect(callback)

	def is_in_favorite_list(self):
		if self.fav_list is not None:
			return self.fav_list.is_media_channel_in_list(self.current_channel)
	
	def update_favorite_icon(self):
		if(self.is_in_favorite_list()):
			self.favorite_button.setIcon(QIcon(QPixmap("assets/favorite_icon.png")))
			self.favorite_button.setIconSize(QSize(24,24))
		else:
			self.favorite_button.setIcon(QIcon(QPixmap("assets/unfavorite_icon.png")))
			self.favorite_button.setIconSize(QSize(24,24))

	# Volume Value Test
	def volume_test_run(self):
		print(self.volume_slider.value())
	
	def set_favorite_list(self, fav: FavoriteMediaChannelShelf):
		self.fav_list = fav

	def get_volume_slider_value(self):
		return self.volume_slider.value()
	
	def update_current(self, station: HLSStation):
		self.current_channel = station
		
class MainGuiWindow(QMainWindow):
	def __init__(self, radio_player=None):
		QMainWindow.__init__(self, None)
		mainWindow = QWidget()
		self.setWindowTitle("Ranet")
		# self.default_height = 620
		# self.default_width = 720
		self.default_height = 360
		self.default_width = 640
		self.setMinimumSize(self.default_width, self.default_height)

		self.create_menu_bar = CreateMenuBar()
		self.setMenuBar(self.create_menu_bar.menu_bar)

		self.radio_player = RadioPlayer()
		self.video_player = self.create_menu_bar.create_channel_wave.get_video_player()

	# QWidget
		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		main_layout = QVBoxLayout(central_widget)
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.setSpacing(0)
		main_layout.setAlignment(Qt.AlignTop)

	# Channel and Control
		# self.create_channel_wave = CreateChannelWave()
		main_layout.addWidget(self.create_menu_bar.create_channel_wave.channel_wave_frame)
	
	# Current Player mode
		self.mode = "radio"

	# Load channels into channel list
		self.channel_wave = self.create_menu_bar.get_channel_wave()
		self.channel_list = self.create_menu_bar.get_channel_wave().get_all_channel_list()
		#self.radio_media_shelf = MediaChannelShelf("assets/all_radio.csv")
		#self.tv_media_shelf    = MediaChannelShelf("assets/all_tv.csv")
		self.radio_media_shelf = MediaChannelShelf.load_from_pickle("assets/all_radio.pickle")
		self.tv_media_shelf = MediaChannelShelf.load_from_pickle("assets/all_tv.pickle")

		self.update_search_bar()

	# Load channels for favorite list
		#self.favorite_radio = FavoriteMediaChannelShelf("assets/favorite_radio.csv")
		#self.favorite_tv = FavoriteMediaChannelShelf("assets/favorite_tv.csv")
		self.favorite_radio = FavoriteMediaChannelShelf.load_from_pickle("assets/favorite_radio.pickle")
		self.favorite_tv = FavoriteMediaChannelShelf.load_from_pickle("assets/favorite_tv.pickle")

		self.load_favorite_list()
		self.channel_wave.set_channel_fav_callback(self.play_fav)
	
	# Setting the callback of the search bar, channel list, and change mode button
		self.channel_wave.set_search_bar_callback(self.update_search_bar)
		self.channel_wave.set_channel_list_callback(self.select_channel)
		self.channel_wave.set_change_mode_callback(self.change_mode)

	# Setting the callback for the play, next, previous, slider volume, favorite
		self.channel_wave.create_control.set_play_button_callback(self.play_button_callback)
		self.channel_wave.create_control.set_next_button_callback(self.next_button_callback)
		self.channel_wave.create_control.set_previous_button_callback(self.previous_button_callback)
		self.channel_wave.create_control.set_favorite_button_callback(self.favorite_button_callback)
		self.channel_wave.create_control.set_volume_slider_callback(self.volume_slider_callback)
		
	# Setting favorite list callback

	# Show
		self.setLayout(main_layout)
		self.show()

	# Function for the model to use or hookup callback
	def set_play_button_callback(self, in_func):
		self.create_menu_bar.create_channel_wave.create_control.set_play_button_callback(in_func)

	def set_previous_button_callback(self, in_func):
		self.create_menu_bar.create_channel_wave.create_control.set_previous_button_callback(in_func)

	def set_next_button_callback(self, in_func):
		self.create_menu_bar.create_channel_wave.create_control.set_next_button_callback(in_func)

	def set_volume_slider_callback(self, in_func):
		self.create_menu_bar.create_channel_wave.create_control.set_volume_slider_callback(in_func)
	
	def set_favorite_button_callback(self, in_func):
		self.create_menu_bar.create_channel_wave.create_control.set_favorite_button_callback(in_func)

	def set_channel_name(self, in_name):
		self.create_menu_bar.create_channel_wave.set_channel_name(in_name)

	def set_radio_player(self, radio_player):
		self.radio_player = radio_player
	
	def get_volume_slider_value(self):
		return self.create_menu_bar.create_channel_wave.create_control.get_volume_slider_value()

	def set_play_button_icon_to_play(self):
		self.create_menu_bar.create_channel_wave.create_control.set_play_button_icon_to_play()
	
	def set_play_button_icon_to_pause(self):
		self.create_menu_bar.create_channel_wave.create_control.set_play_button_icon_to_pause()
	
	def load_channels_from_array(self, arr: list[str]):
		self.channel_wave.clear_all_channel_list()
		for channel in arr:
			self.channel_wave.all_channel_list_add_item(channel)
	
	def update_search_bar(self):
		"""
		Once text has been typed into the search bar, this function will
		update the channel list with the relevant search result.
		"""
		search_bar = self.channel_wave.get_search_bar()
		search_input = search_bar.text()
		query_result : list[str] = []
		
		if self.mode == "radio":
			query_result = self.radio_media_shelf.get_channels_name_by_search(search_input)
		else:
			query_result = self.tv_media_shelf.get_channels_name_by_search(search_input)
		query_result.sort()
		
		self.load_channels_from_array(query_result)
	
	def update_favorite_btn(self):
		self.channel_wave.create_control.update_favorite_icon()
	
	def select_channel(self):

		selected_channel = self.channel_list.currentItem().text()
		if self.mode == "radio":
			media = self.radio_media_shelf.get_channel_by_name(selected_channel)
			self.radio_media_shelf.set_main_current_index(media)
			self.radio_player.set_media(media)
			self.radio_player.update_gui(self)
		else:
			media = self.tv_media_shelf.get_channel_by_name(selected_channel)
			self.tv_media_shelf.set_main_current_index(media)
			self.video_player.set_media(media)
			self.video_player.update_gui(self)

	def volume_slider_callback(self):
		slider_value = self.get_volume_slider_value()
		if self.mode == "radio":
			self.radio_player.set_volume(slider_value)
		else:
			self.video_player.set_volume(slider_value/100)

	def play_button_callback(self):
		
		if self.mode == "radio":
			self.radio_player.toggle()
			self.radio_player.update_gui(self)
		else:
			self.video_player.toggle()
			self.video_player.update_gui(self)

	def next_button_callback(self):

		if self.mode == "radio":
			media = self.radio_media_shelf.get_next_channel()
			self.radio_player.set_media(media)
			self.radio_player.update_gui(self)
		else:
			media = self.tv_media_shelf.get_next_channel()
			self.video_player.set_media(media)
			self.video_player.update_gui(self)

	def previous_button_callback(self):
		
		if self.mode == "radio":
			media = self.radio_media_shelf.get_previous_channel()
			self.radio_player.set_media(media)
			self.radio_player.update_gui(self)
		else:
			media = self.tv_media_shelf.get_previous_channel()
			self.video_player.set_media(media)
			self.video_player.update_gui(self)

	def favorite_button_callback(self):
		if self.mode == "radio":
			current_station = self.radio_player.get_station()
			if self.favorite_radio.is_media_channel_in_list(current_station):
				self.favorite_radio.delete_media_channel(current_station)
			else:
				self.favorite_radio.add_media_channel(current_station)
		else:
			current_station = self.video_player.get_current_station()
			if self.favorite_tv.is_media_channel_in_list(current_station):
				self.favorite_tv.delete_media_channel(current_station)
			else:
				self.favorite_tv.add_media_channel(current_station)
		self.load_favorite_list()
		
	def change_mode(self):
		if self.mode == "radio":
			self.radio_player.stop()
			self.mode = "tv"
			self.radio_player.update_gui(self)
		else:
			self.video_player.stop()
			self.mode = "radio"
			self.video_player.update_gui(self)
		self.update_search_bar()
		self.load_favorite_list()
	
	def load_favorite_list(self):
		if self.mode == "radio":
			self.channel_wave.load_favorite_list(self.favorite_radio)
		else:
			self.channel_wave.load_favorite_list(self.favorite_tv)
	
	def play_fav(self, i):
		selected_channel = self.channel_wave.channel_fav.itemText(i)
		if self.mode == "radio":
			media = self.radio_media_shelf.get_channel_by_name(selected_channel)
			self.radio_player.set_media(media)
			self.radio_player.update_gui(self)
		else:
			media = self.tv_media_shelf.get_channel_by_name(selected_channel)
			self.video_player.set_media(media)
			self.video_player.update_gui(self)


			
		

		

class ControlClickHandler(object):
	_instance = None
	def __new__(self):
		if not self._instance:
			self._instance = super(ControlClickHandler, self).__new__(self)
			self.currently_playing = False
		return self._instance

	# Toggle Status When Play or Pause Button is Clicked
	def play_pause_button_click(self):
		if self.currently_playing:
			self.currently_playing = False
			print(self.currently_playing)
		else:
			self.currently_playing = True
			print(self.currently_playing)

	def play_action_button_click(self):
		self.currently_playing = True
		# Test
		print(self.currently_playing)

	def pause_action_button_click(self):
		self.currently_playing = False
		# Test
		print(self.currently_playing)

	# CallBack Function when the previous button is clicked
	def previous_button_click(self):
		# Test
		print("Previous button Click")

	# CallBack Function when the next button is clicked
	def next_button_click(self):
		# Test
		print("Next button Click")

class ControlChannelHandler(QWidget):
	def __init__(self):
		QWidget.__init__(self, None)
		self.create_channel_wave = CreateChannelWave()

	# set channel number
	def set_current_channel_num(self, new_channel_num):
		self.channel_num.setText(new_channel_num)
		self.create_channel_wave.channel_num.setText(self.current_channel_num)

	# set channel name
	def set_current_channel_name(self, new_channel_name):
		self.channel_name.setText(new_channel_name)
		self.create_channel_wave.channel_name.setText(self.current_channel_name)

# CSS
CSS = """
	QSlider::handle:horizontal {
		background: black;
		border: 1px solid black;
		width: 24px;
		height: 8 px;
		border-radius: 4px;
	}
	QSlider::groove:horizontal {
		border: 1px solid black;
		height: 10px;
		background: #eee;
		margin: 0px;
		border-radius: 4px;
	}
	QPushButton::hover{
		background: lightgray;
	}
	QPushButton::hover:pressed{
		background: black;
	}
	
"""

# Temporary // Testing
def main():
	app = QApplication(sys.argv)
	app.setStyleSheet(CSS)

	w = MainGuiWindow()
	w.show()

	return app.exec()

if __name__ == "__main__":
	sys.exit(main())
