from PyQt5 import QtWidgets, QtCore


class MovableLabel(QtWidgets.QLabel):

    main_window = None

    def __init__(self, parent=None):
        super(MovableLabel, self).__init__(parent=parent)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.main_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.main_window.move(event.globalPos() - self.dragPosition)
            event.accept()
