import sys
from src.radio import *
from src.connection import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class TestUI(QWidget):
	"""For testing purposes only. DELETE ME"""
	def __init__(self, player):
		QWidget.__init__(self, None)

		self.player = player
		self.volume = player.volume
		vbox = QVBoxLayout()

		dec = QPushButton("Decrease Volume", self)
		dec.clicked.connect(self.decrease)
		vbox.addWidget(dec)

		play = QPushButton("Play", self)
		play.clicked.connect(self.play)
		vbox.addWidget(play)

		stop = QPushButton("Stop", self)
		stop.clicked.connect(self.stop)
		vbox.addWidget(stop)

		moe = QPushButton("Switch to LISTEN.moe", self)
		moe.clicked.connect(self.moe_moe_kyun)
		vbox.addWidget(moe)

		self.setLayout(vbox)
		self.show()

	def __del__(self):
		self.player.stop()

	def decrease(self):
		self.volume -= 10
		self.player.set_volume(self.volume)

	def play(self):
		self.player.play()

	def stop(self):
		self.player.stop()

	def moe_moe_kyun(self):
		listen_moe = RadioStation(
			"LISTEN.moe",
			"https://listen.moe/stream",
			"Vorbis"
		)
		self.player.change_station(listen_moe)

def main():
	station = RadioStation(
		"Saitama Chappy",
		"https://musicbird.leanstream.co/JCB019-MP3",
		"mp3"
	)

	player = RadioPlayer(station)
	app = QApplication(sys.argv)
	w = TestUI(player)
	sys.exit(app.exec_())

	# If this line is not used, the music will keep playing
	# even after we close the GUI window.
	del player

if __name__ == "__main__":
	main()
