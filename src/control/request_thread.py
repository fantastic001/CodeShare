
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RequestThread(QThread):
	
	# These signals are emitted by GUI
	codeEdited = pyqtSignal(str)
	
	# These signals are emitted by thread and GUI has to catch them 
	requestAccepted = pyqtSignal()
	codeChanged = pyqtSignal(str)
	
	def __init__(self, client):
		super(RequestThread, self).__init__()
		self.running = True
		self.start()
		self.client = client
		self.granted = False 
		self.requested = False
	
		self.codeEdited.connect(self.codeEditedCallback)
	
	def setRequested(self, requested):
		self.requested = requested
		
	def getGranted(self):
		return self.granted
	
	def codeEditedCallback(self, s):
		if self.granted:
			self.code = s
	
	def run(self):
		while self.running:
			if self.granted:
				self.client.sendCode(self.code)
				if not self.requested:
					self.client.release()
					self.granted = False
			else:
				self.code = self.client.getCode()
				self.codeChanged.emit(self.code)
				if self.requested:
					self.granted = self.client.request()
					if self.granted:
						self.requestAccepted.emit()
		
			time.sleep(0.4)
	
	def terminate(self):
		self.running = False
	