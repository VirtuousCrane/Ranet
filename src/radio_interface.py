from radio import *
import time
from radio import RadioTracker
from connection import *

class RadioInterface(object):
	def __init__(self):
		self.radio_tracker = RadioTracker()
		self.radio_player = RadioPlayer(self.radio_tracker.get_current_station())

	def switch_on(self):
		print("Playing radio")
		if not connection_check_status() == ConnectionStatus.OK:
			print("Bad connection, bitch")
			sys.exit(1)
		self.radio_player.play()

	def switch_off(self):
		print("Turning off the radio")
		self.radio_player.stop()

	def next_channel(self):
		print("Switching to next possible radio channel")
		self.radio_tracker.increment_index()
		self.radio_player.change_station(self.radio_tracker.get_current_station())

	def previous_channel(self):
		print("Switching to previous possible radio channel")
		self.radio_tracker.decrement_index()
		self.radio_player.change_station(self.radio_tracker.get_current_station())

	def display_current_channel(self):
		print("Display info of current radio channel")
		print("Current radio info: ", self.radio_player.get_station_name(), self.radio_player.get_station_url(), self.radio_player.get_station_media_type())


class RadioCMDApp(object):
	def __init__(self):
		self.radio = RadioInterface()

	def start(self):
		userInput = -1
		while(userInput != 0):
			print("Radio interface")
			print("1. Switch on")
			print("2. Switch off")
			print("3. Next channel")
			print("4. Previous channel")
			print("5. Display current channel")
			print("6. Clicked exit button")
			print("0. Exit")

			try:
				userInput = input("Select option: ")
				userInput = int(userInput)
			except:
				print("Invalid input, exitting program")
				userInput = 0

			if(userInput == 0):
				print("Exitting program")
				self.radio.switch_off()
			elif(userInput == 1):
				self.radio.switch_on()
			elif(userInput == 2):
				self.radio.switch_off()
			elif(userInput == 3):
				self.radio.next_channel()
			elif(userInput == 4):
				self.radio.previous_channel()
			elif(userInput == 5):
				self.radio.display_current_channel()
			else:
				print("Option not available/not implemented")


if __name__ == "__main__":
	app = RadioCMDApp()
	app.start()

	print("End of program")
