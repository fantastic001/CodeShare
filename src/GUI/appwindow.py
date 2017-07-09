
from PyQt5.QtWidgets import *

from editor import CodeEditor

class AppWindow(QWidget):

	def __init__(self):
		super(AppWindow, self).__init__()
		self.bRqEdit = QPushButton("Rq Edit")
		self.bRlEdit = QPushButton("Rl Edit")
		self.codeEditor = CodeEditor()
		l1 = QVBoxLayout()
		l2 = QHBoxLayout()
		l2.addWidget(self.bRqEdit)
		l2.addWidget(self.bRlEdit)
		l1.addLayout(l2)
		l1.addWidget(self.codeEditor)
		self.setLayout(l1)