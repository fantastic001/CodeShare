import json
from PyQt5.QtWidgets import *

from .editor import CodeEditor
from .hlaction import HlAction
from client import Client
from control import RequestThread

class AppWindow(QWidget):
	
	hlModes = ["none", "cpp", "pas"]

	def __init__(self, argv):
		super(AppWindow, self).__init__()
		
		self.editGranted = False
		self.editRequested = False
		self.client = Client("0.0.0.0", 5000, "us1")
		self.client.join("gr1")
		self.requestThread = RequestThread(self)
		self.requestThread.start()
		
		# GUI elements
		self.bDropMenu = QPushButton("Hl Mode")
		self.bRqEdit = QPushButton("Rq Edit")
		self.bRlEdit = QPushButton("Rl Edit")
		self.lEditState = QLabel("Not granted")
		self.codeEditor = CodeEditor()
		
		self.menu = QMenu()
		for mode in self.hlModes:
			action = HlAction(mode, self)
			action.triggered.connect(action.callback)
			self.menu.addAction(action)
		self.bDropMenu.setMenu(self.menu)
		self.bRqEdit.clicked.connect(self.bRqEditClicked)
		self.bRlEdit.clicked.connect(self.bRlEditClicked)
		
		# GUI layout
		l1 = QVBoxLayout()
		l2 = QHBoxLayout()
		l2.addWidget(self.bDropMenu)
		l2.addWidget(self.bRqEdit)
		l2.addWidget(self.bRlEdit)
		l2.addWidget(self.lEditState)
		l1.addLayout(l2)
		l1.addWidget(self.codeEditor)
		self.setLayout(l1)
		
	def actionHlMode(self, mode):
		try:
			with open("hlData/" + mode + ".json") as f:
				fData = f.read()
				hlData = json.loads(fData)
				self.codeEditor.setHl(hlData)
		except:
			self.codeEditor.setHl({})
		
	def bRqEditClicked(self, item):
		self.editRequested = True
		self.lEditState.setText("Requested")
	
	def RqEditAcceptedCallback(self):
		self.editGranted = True
		self.editRequested = False
		self.lEditState.setText("Granted")
		
	def bRlEditClicked(self, item):
		self.editGranted = False
		self.lEditState.setText("Not granted")
		self.client.release()
		
	def closeEvent(self, event):
		self.requestThread.terminate()
		event.accept()
		