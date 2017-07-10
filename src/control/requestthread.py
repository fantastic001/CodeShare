import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RequestThread(QThread):
	def __init__(self, parent):
		super(RequestThread, self).__init__(parent)
		self.appWindow = parent
		self.running = True
		self.start()
	
	def run(self):
		while self.running:
			if self.appWindow.editRequested:
				if self.appWindow.client.request():
					self.appWindow.RqEditAcceptedCallback()
			else:
				time.sleep(1)
	
	def terminate(self):
		self.running = False