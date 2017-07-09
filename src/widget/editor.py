
from PyQt5.QtWidgets import * 

from .highlighter import CodeHighlighter 

class CodeEditor(QTextEdit):
    
    def __init__(self):
        super(CodeEditor, self).__init__()
        self.highlighter = CodeHighlighter(self.document())

