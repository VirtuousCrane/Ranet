import sys
from src.connection import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from src.radio import Radio
from src.gui.gui_design import MainGuiWindow, CSS

class RadioApp(object):
	def __init__(self):
		# Intiailizing the QtWidgets
		self.app = QApplication(sys.argv)
		self.app.setStyleSheet(CSS)
		self.gui = MainGuiWindow()

		# Intiialize the radio
		self.radio = Radio(self.gui)
		
		# Linking the radio model with the GUI callbacks
		self.gui.set_play_button_callback(self.radio.toggle)
		self.gui.set_previous_button_callback(self.radio.previous_channel)
		self.gui.set_next_button_callback(self.radio.next_channel)
		
		
	def start(self):
		self.gui.show()
		self.app.exec()
	

def main():
	radio_app = RadioApp()
	radio_app.start()

if __name__ == "__main__":
	print("Starting program in main.py")
	main()
