from Terminal import Terminal
from PyQt5 import QtWidgets, QtGui
import sys


app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon("terminal_icon.png"))
terminal = Terminal()
terminal.show()
app.exec()
app.exit(0)
