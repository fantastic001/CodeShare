
from src import CodeEditor
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

c = CodeEditor()
c.show()

sys.exit(app.exec_())

