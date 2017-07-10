
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RequestThread(QThread):
    
    # These signals are emitted by GUI
    editRequested = pyqtSignal()
    codeEdited = pyqtSignal(str)
    editReleased = pyqtSignal()

    # These signals are emitted by thread and GUI has to catch them 
    requestAccepted = pyqtSignal()
    codeChanged = pyqtSignal(str)

    def __init__(self, client):
        super(RequestThread, self).__init__()
        self.running = True
        self.start()
        self.client = client
        self.granted = False 

        self.editRequested.connect(self.editRequestedCallback)
        self.codeEdited.connect(self.codeEditedCallback)
        self.editReleased.connect(self.editReleasedCallback)

    def editReleasedCallback(self):
        self.granted = False 
        self.client.release()

    def editRequestedCallback(self):
        self.granted = self.client.request()
        if self.granted:
            self.requestAccepted.emit()

    def codeEditedCallback(self, s):
        if self.granted:
            self.code = s
    
    def run(self):
        while self.running:
            if self.granted:
                self.client.sendCode(self.code)
            else:
                self.code = self.client.getCode()
                self.codeChanged.emit(self.code)
        
            time.sleep(1)
    
    def terminate(self):
        self.running = False
