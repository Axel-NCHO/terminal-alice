import sys

from PyQt5 import QtCore, QtWidgets, QtGui
from terminalUi import UiTerminal
from Components.Tab.Tab import Tab
from Components.TitleBar.TitleBar import TitleBar
from Components.TextArea.TextArea import TextArea


class Terminal(QtWidgets.QWidget, UiTerminal):

    def __init__(self):
        super(Terminal, self).__init__()
        self.setup_ui(self)
        self.setWindowIcon(QtGui.QIcon("terminal_icon.png"))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.tab_dict = dict()
        self.tab_id = 0
        self.active_tab = 0
        self.tab_count = 0

        self.title_bar = TitleBar(self)
        self.verticalLayout.addWidget(self.title_bar)
        self.add_tab()
        self.title_bar.titleBarPushButton_4.clicked.connect(self.add_tab)

    def add_tab(self):
        try:
            self.tab_dict[self.active_tab][0].set_active(0)
            self.tab_dict[self.active_tab][1].hide()
        except Exception as e:
            print(e)

        tab = Tab()
        tab.set_id(self.tab_id)
        self.title_bar.insert_tab(tab)
        text_area = TextArea(parent=self)
        self.verticalLayout.addWidget(text_area)

        self.active_tab = self.tab_id
        self.tab_dict[self.tab_id] = [tab, text_area]
        tab.clicked.connect(self.select_tab)
        tab.tabPushButton.clicked.connect(self.delete_tab)
        self.tab_id += 1
        self.tab_count += 1
        self.insert_default_text()

    def select_tab(self, tab_id):
        try:
            self.tab_dict[self.active_tab][0].set_active(0)
            self.tab_dict[self.active_tab][1].hide()
        except Exception as e:
            print(e)
        self.tab_dict[tab_id][0].set_active(1)
        self.tab_dict[tab_id][1].show()
        self.active_tab = tab_id

    def delete_tab(self):
        delete_id = int(self.sender().objectName())
        temp = list(self.tab_dict)
        temp_id = temp.index(delete_id)
        last_id = len(temp) - 1
        if self.tab_count > 1:
            if delete_id == self.active_tab:
                if last_id > temp_id:
                    s_id = temp[temp_id + 1]
                else:
                    s_id = temp[temp_id - 1]
                self.select_tab(s_id)
            self.tab_dict[delete_id][0].deleteLater()
            self.tab_dict[delete_id][1].deleteLater()
            self.tab_dict.pop(delete_id)
            self.tab_count -= 1
        else:
            sys.exit(0)

    def insert_text(self, text: str):
        self.tab_dict[self.active_tab][1].set_text(text)

    def insert_default_text(self):
        self.tab_dict[self.active_tab][1].set_default_text()
