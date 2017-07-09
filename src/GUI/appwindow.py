
from PyQt5.QtWidgets import *

from .editor import CodeEditor

class AppWindow(QWidget):

	def __init__(self):
		super(AppWindow, self).__init__()
		
		self.editGranted = False
		self.editRequested = False
		
		# GUI
		
		self.bRqEdit = QPushButton("Rq Edit")
		self.bRlEdit = QPushButton("Rl Edit")
		self.lEditState = QLabel("asd")
		self.codeEditor = CodeEditor()
		
		l1 = QVBoxLayout()
		l2 = QHBoxLayout()
		l2.addWidget(self.bRqEdit)
		l2.addWidget(self.bRlEdit)
		l2.addWidget(self.lEditState)
		l1.addLayout(l2)
		l1.addWidget(self.codeEditor)
		self.setLayout(l1)
		
		self.bRqEdit.clicked.connect(self.bRqEditClicked)
		self.bRlEdit.clicked.connect(self.bRlEditClicked)
		
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
		
		