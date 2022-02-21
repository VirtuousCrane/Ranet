class Error(Exception):
	"""Base class for other exceptions"""
	pass

class ConnectionError(Error):
	"""Raised when there is an error with the connection status"""
	pass
