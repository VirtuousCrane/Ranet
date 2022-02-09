from enum import Enum
import os
import requests
import platform
import subprocess

class ConnectionStatus(Enum):
	"""
	An Enum representing each state of connection status\n

	ConnectionStatus.OK  = The Connection connected successfully\n
	ConnectionStatus.ERR = There was an error with the connection\n
	"""
	ERR = 0
	OK = 1

def connection_check_status(url: str = "https://www.google.com", timeout: int = 5) -> ConnectionStatus:
	"""
	A function to check the internet connectivity status

	Parameters
	----------
	url : str
		The url we want to check the connection against.
		DEFAULT: https://www.google.com
	timeout : int
		How long to wait until we report an error
		DEFAULT: 5

	Returns
	-------
	ConnectionStatus
		The status of the connection. OK if fine, ERR if error.

	"""
	try:
		res = requests.get(url, timeout=timeout)
		return ConnectionStatus.OK
	except (requests.ConnectionError, requests.Timeout) as e:
		return ConnectionStatus.ERR

def connection_ping(url: str) -> ConnectionStatus:
	"""
	Pings a given URL

	Parameters
	----------
	url : str
		The URL to ping

	Returns
	-------
	ConnectionStatus
		OK if a response is received, otherwise ERR.

	"""

	# Determines the command line argument based on the user's OS
	param = ""
	if platform.system().lower() == "windows":
		param = "-n"
	else:
		param = "-c"

	# Pings the given URL
	command = ["ping", param, "1", url]

	devnull = open(os.devnull, 'w')
	result = subprocess.call(command,
		stdout=devnull,
		stderr=subprocess.STDOUT)

	if result == 0:
		return ConnectionStatus.OK
	return ConnectionStatus.ERR
