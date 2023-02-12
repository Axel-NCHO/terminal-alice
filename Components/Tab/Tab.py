from PyQt5 import QtCore, QtGui, QtWidgets
from Components.Tab.tabUi import UiTabWidget


class Tab(QtWidgets.QTabWidget, UiTabWidget):

    clicked = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(Tab, self).__init__(parent=parent)
        self.setup_ui(self)

    def set_active(self, act):
        if act == 0:
            self.tabWidget_2.setStyleSheet("QWidget{\n"
                                           "    background-color:rgb(12, 11, 16);\n"
                                           "    color:rgb(144, 144, 144);\n"
                                           "    padding:2px;\n"
                                           "}\n"
                                           "QWidget:hover{\n"
                                           "    background-color:rgb(25, 25, 25);\n"
                                           "}")
        else:
            self.tabWidget_2.setStyleSheet("QWidget{\n"
                                           "    background-color:rgb(35, 34, 39);\n"
                                           "    color:rgb(170, 170, 170);\n"
                                           "    padding:2px;\n"
                                           "}")

    def set_id(self, identifier):
        self.tabPushButton.setObjectName(str(identifier))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(int(self.tabPushButton.objectName()))
