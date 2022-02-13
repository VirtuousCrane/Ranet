import sys
from src.radio import *
from src.connection import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from src.radio_interface


class RadioApp(object):
	def __init__(self):
		self.radio = src.radio_interface.Radio()
		
	def start(self):
		pass
	

def main():
	radio_app = RadioApp()
	radio_app.start()

if __name__ == "__main__":
	print("Starting program")
	print(sys.path)
	main()
