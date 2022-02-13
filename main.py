import sys
from src.radio import *
from src.connection import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from src.gui.gui_design import MainGuiWindow
from src.radio_track import RadioTracker


class RadioApp(object):
	def __init__(self):
		self.gui = MainGuiWindow()
		self.radio_track = RadioTracker()
		
	def start(self):
		pass
	

def main():
	radio_app = RadioApp()
	radio_app.start()

if __name__ == "__main__":
	print("Starting program")
	
	main()
