import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from src.connection import *
from src.gui.gui_design import MainGuiWindow, CSS

class RanetApp(object):
	def __init__(self):
		# Intiailizing the QtWidgets
		self.app = QApplication(sys.argv)
		self.app.setStyleSheet(CSS)
		self.gui = MainGuiWindow()

	def start(self):
		if not connection_check_status() == ConnectionStatus.OK:
			print("Bad connection")
			sys.exit(1)
		self.gui.show()
		self.app.exec()

def main():
	radio_app = RanetApp()
	radio_app.start()

if __name__ == "__main__":
	print("Starting program in main.py")
	main()
