import json
from PyQt5.QtWidgets import *

from .editor import CodeEditor
from .hlaction import HlAction

class AppWindow(QWidget):
	
	hlModes = ["none", "cpp", "pas"]

	def __init__(self):
		super(AppWindow, self).__init__()
		
		self.editGranted = False
		self.editRequested = False
		
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
		while not self.editGranted and self.editRequested:
			# wait on timer before sending edit request
			response = '0' # send edit request to the server
			if response == '1':
				self.editGranted = True
				self.editRequested = False
				self.lEditState.setText("Granted")
		
	def bRlEditClicked(self, item):
		self.editGranted = False
		self.lEditState.setText("Not granted")
		
		