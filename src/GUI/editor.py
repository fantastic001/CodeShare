
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 

from .highlighter import CodeHighlighter 

class CodeEditor(QTextEdit):

	def __init__(self, appWindow):
		super(CodeEditor, self).__init__()
		self.textChanged.connect(self.changeText)
		self.appWindow = appWindow
		self.highlighter = None

	def setHl(self, hlData):
		keywords = []
		colors = []
		for key in hlData:
			keywords.append(key)
			colors.append(QColor(hlData[key][0], hlData[key][1], hlData[key][2]))
		self.highlighter = CodeHighlighter(self.document(), keywords, colors)
		
	def changeText(self):
		self.appWindow.textEdited = True