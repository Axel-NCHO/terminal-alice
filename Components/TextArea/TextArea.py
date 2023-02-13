from PyQt5 import QtWidgets

from Components.TextArea.textAreaUi import UiTextAreaWidget


class TextArea(QtWidgets.QWidget, UiTextAreaWidget):

    def __init__(self, parent=None):
        super(TextArea, self).__init__(parent=parent)
        self.setup_ui(textAreaUi=self)

    def set_text(self, text: str):
        self.text_area.setText(text)

    def set_default_text(self):
        self.text_area.set_default_text()

    def show(self):
        super().show()
        self.text_area.setFocus()
