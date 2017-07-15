import json

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .editor import CodeEditor
from .hlaction import HlAction
from client import Client

from control import RequestThread

class AppWindow(QWidget):
        
        hlModes = ["none", "cpp", "pas"]

        # args : asddress, port, username
        def __init__(self, argv):
                super(AppWindow, self).__init__()
                self.setWindowTitle("Code Share")
                if len(argv) > 3: 
                    self.client = Client(argv[1], int(argv[2]), argv[3], argv[4])
                else:
                    self.client = Client(argv[1], int(argv[2]))
                self.client.join(1)
                self.thread = RequestThread(self.client)
                self.thread.requestAccepted.connect(self.RqEditAcceptedCallback)
                self.thread.codeChanged.connect(self.codeChangedCallback)
                
                # GUI elements
                self.bDropMenu = QPushButton("Hl Mode")
                self.bRqEdit = QPushButton("Rq Edit")
                self.bRlEdit = QPushButton("Rl Edit")
                self.lEditState = QLabel("Not granted")
                self.codeEditor = CodeEditor(self)
                self.codeEditor.textChanged.connect(self.codeEditedCallback)
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
                
        
        def codeEditedCallback(self):
                self.thread.codeEdited.emit(self.codeEditor.toPlainText())

        def bRqEditClicked(self, item):
                if not self.thread.getGranted():
                        self.thread.setRequested(True)
                        self.lEditState.setText("Requested")
        
        def RqEditAcceptedCallback(self):
                self.lEditState.setText("Granted")
                
        def bRlEditClicked(self, item):
                self.thread.setRequested(False)
                self.lEditState.setText("Not granted")

        def codeChangedCallback(self, code):
                self.codeEditor.setText(code)


