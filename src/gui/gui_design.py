import sys
from typing import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from radio_channel_list_gui import RadioChannelListGuiWindow

class CreateMenuBar(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self, None)
		self.menu_bar = self.menuBar()

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

class CreateChannelWave(QWidget):
	def __init__(self):
		QWidget.__init__(self, None)
		self.channel_wave_layout = QVBoxLayout()
		self.channel_wave_layout.setStretchFactor(self.channel_wave_layout,1)

		# Wave Image Container
		self.wave_container = QLabel()
		self.wave_container.setText("current size (720 x 480)")
		# self.wave_container.setStyleSheet("background-color: red;")
		self.wave_container.setMinimumHeight(480)

		# Control
		self.create_control = CreateControlBar()

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
		self.channel_fav.setFixedSize(256,30)

		# ----Test----
		self.channel_fav.addItem("channel1")
		self.channel_fav.addItem("channel2")
		self.channel_fav.addItem("channel3")
		# ------------

		self.channel_fav_name_layout.addWidget(self.channel_name)
		self.channel_fav_name_layout.addWidget(self.create_control.favorite_button)
		self.channel_fav_name_layout.addWidget(self.channel_fav)
		self.channel_fav_name_layout.addWidget(self.create_control.full_screen_button)

		self.channel_wave_layout.addWidget(self.wave_container)
		self.channel_wave_layout.addLayout(self.channel_fav_name_layout)
		self.channel_wave_layout.addLayout(self.create_control.control_layout)

	
	# Function for adding favorite channel List
	def add_channel_fav_list(self, in_func):
		self.channel_fav.addItem(QListWidgetItem(in_func))

	# Set channel name
	def set_channel_name(self, in_name: str):
		"""
		Sets the channel name label in the GUI

		Parameters
		----------
		in_name : str
			The new channel name
		"""
		self.channel_name.setText(in_name)

class CreateControlBar(QWidget):
	def __init__(self):
		QWidget.__init__(self, None)
		self.control_layout = QVBoxLayout()
		self.control_layout.setAlignment(Qt.AlignCenter)
		self.control_layout.setSpacing(8)

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
		self.favorite_button = QPushButton("Fav")
		self.favorite_button.setFixedSize(30,30)

	# Full Screen Button
		self.full_screen_button = QPushButton("Full")
		self.full_screen_button.setFixedSize(30,30)

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

	def set_favorite_callback(self, in_func):
		self.favorite_button.clicked.connect(in_func)

	# Volume Value Test
	def volume_test_run(self):
		print(self.volume_slider.value())

	def get_volume_slider_value(self):
		return self.volume_slider.value()
		
class MainGuiWindow(QMainWindow):
	def __init__(self, radio_player=None):
		QMainWindow.__init__(self, None)
		mainWindow = QWidget()
		self.setWindowTitle("Ranet")
		self.default_height = 620
		self.default_width = 720
		self.setFixedSize(self.default_width, self.default_height)

		self.create_menu_bar = CreateMenuBar()
		self.setMenuBar(self.create_menu_bar.menu_bar)

		self.radio_player = radio_player

	# QWidget
		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		main_layout = QVBoxLayout(central_widget)
		main_layout.setContentsMargins(0,0,0,0)
		main_layout.setSpacing(0)
		main_layout.setAlignment(Qt.AlignTop)

	# Channel and Control
		self.create_channel_wave = CreateChannelWave()
		main_layout.addLayout(self.create_channel_wave.channel_wave_layout)

	# Show
		self.setLayout(main_layout)
		self.show()

	# Function for the model to use or hookup callback
	def set_play_button_callback(self, in_func):
		self.create_channel_wave.create_control.set_play_button_callback(in_func)

	def set_previous_button_callback(self, in_func):
		self.create_channel_wave.create_control.set_previous_button_callback(in_func)

	def set_next_button_callback(self, in_func):
		self.create_channel_wave.create_control.set_next_button_callback(in_func)

	def set_volume_slider_callback(self, in_func):
		self.create_channel_wave.create_control.set_volume_slider_callback(in_func)
	
	def set_favorite_button_callback(self, in_func):
		self.create_channel_wave.create_control.set_favorite_callback(in_func)

	def set_channel_name(self, in_name):
		self.create_channel_wave.set_channel_name(in_name)

	def set_radio_player(self, radio_player):
		self.radio_player = radio_player

	def get_volume_slider_value(self):return self.create_control.get_volume_slider_value()

	def set_play_button_icon_to_play(self):
		self.create_control.set_play_button_icon_to_play()
	
	def set_play_button_icon_to_pause(self):
		self.create_control.set_play_button_icon_to_pause()

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
