
from PyQt5.QtWidgets import *

class HlAction(QAction):
	def __init__(self, mode, appWindow):
		super(QAction, self).__init__(mode, appWindow)
		self.mode = mode
		self.appWindow = appWindow
		
	def callback(self, item):
		self.appWindow.actionHlMode(self.mode)