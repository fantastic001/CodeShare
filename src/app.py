import sys

from PyQt5.QtWidgets import QApplication

from GUI import AppWindow

app = QApplication(sys.argv)

appWindow = AppWindow(sys.argv)
appWindow.show()

sys.exit(app.exec_())

