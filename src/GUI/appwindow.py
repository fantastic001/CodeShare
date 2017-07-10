import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .editor import CodeEditor
from .hlaction import HlAction
from client import Client

class AppWindow(QWidget):
	
	hlModes = ["none", "cpp", "pas"]

	def __init__(self, argv):
		super(AppWindow, self).__init__()
		self.setWindowTitle("Code Share")
		
		self.editGranted = False
		self.editRequested = False
		self.textEdited = False
		self.client = Client(argv[1], int(argv[2]), argv[3s])
		self.client.join("gr1")
		self.requestTimer = QTimer(self)
		self.requestTimer.setInterval(500)
		self.requestTimer.timeout.connect(self.requestTimerHandler)
		
		# GUI elements
		self.bDropMenu = QPushButton("Hl Mode")
		self.bRqEdit = QPushButton("Rq Edit")
		self.bRlEdit = QPushButton("Rl Edit")
		self.lEditState = QLabel("Not granted")
		self.codeEditor = CodeEditor(self)
		
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
		
		self.requestTimer.start(500)
		
	def actionHlMode(self, mode):
		try:
			with open("hlData/" + mode + ".json") as f:
				fData = f.read()
				hlData = json.loads(fData)
				self.codeEditor.setHl(hlData)
		except:
			self.codeEditor.setHl({})
		
	def bRqEditClicked(self, item):
		if not self.editGranted:
			self.editRequested = True
			self.lEditState.setText("Requested")
	
	def RqEditAcceptedCallback(self):
		self.editGranted = True
		self.editRequested = False
		self.lEditState.setText("Granted")
		
	def bRlEditClicked(self, item):
		self.editGranted = False
		self.editRequested = False
		self.client.release()
		self.lEditState.setText("Not granted")

	def requestTimerHandler(self):
		if self.editRequested:
			if self.client.request():
				self.RqEditAcceptedCallback()
				
		if self.textEdited:
			if self.editGranted:
				self.client.sendCode(self.codeEditor.toPlainText())
			self.textEdited = False
			
		if not self.editGranted:
			self.codeEditor.setText(self.client.getCode())
		
