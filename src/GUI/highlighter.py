
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

class CodeHighlighter(QSyntaxHighlighter):
    
    def __init__(self, parent):
        super(CodeHighlighter, self).__init__(parent)
        self.parent = parent
        kw_format = QTextCharFormat()
        kw_format.setForeground(QBrush(QColor(255, 0, 120)))
        
        self.rules = []
        keywords = ["char", "class", "const", "int", "double", "float", "long", "private", "public", "void", "unsigned", "short"]
        for kw in keywords:
            self.rules.append((QRegExp(kw), kw_format))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QBrush(QColor(120, 255, 120)))
        self.rules.append((QRegExp("\".*\""), quotationFormat))
        
        comm_format = QTextCharFormat()
        comm_format.setForeground(QBrush(QColor(0, 0, 255)))
        self.rules.append((QRegExp("//.*"), comm_format))
        

    def highlightBlock(self, text):
        self.parent = QTextDocument(self.parent.toPlainText())
        for r in self.rules:
            exp = QRegExp(r[0])
            index = exp.indexIn(text)
            while index >= 0:
                length = exp.matchedLength();
                self.setFormat(index, length, r[1])
                index = exp.indexIn(text, index + length)

        comm_format = QTextCharFormat()
        comm_format.setForeground(QBrush(QColor(0, 0, 255)))
        commstartexpr = QRegExp(r"/\*")
        commendexpr = QRegExp(r"\*/")
        
        startindex = 0;
        if self.previousBlockState() != 1:
            startindex = commstartexpr.indexIn(text);
        while startindex >= 0:
            endindex = commendexpr.indexIn(text, startindex)
            commentLength = 0
            if endindex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startindex
            else:
                commentLength = endindex - startindex + commendexpr.matchedLength()
            self.setFormat(startindex, commentLength, comm_format)
            startindex = commstartexpr.indexIn(text, startindex + commentLength)
