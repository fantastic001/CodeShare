
from GUI import AppWindow
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

appWindow = AppWindow()
appWindow.show()

sys.exit(app.exec_())

