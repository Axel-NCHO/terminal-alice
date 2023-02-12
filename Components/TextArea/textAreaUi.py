# -*- coding: utf-8 -*-
import re
import socket

# Form implementation generated from reading ui file '.\textArea.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import threading


user = "axel"
terminal_prompt = ">  "
terminal_prompt_color = (252, 158, 88)
terminal_io_color = (170, 170, 170)
terminal_error_color = (168, 74, 50)
terminal_warning_color = (168, 158, 50)
terminal_error_indicator = "\\error"
terminal_warning_indicator = "\\warn"
terminal_separator = " "
terminal_system_key_word = "sys"
terminal_media_keyword = "media"
terminal_net__keyword = "net"
terminal_memory_keyword = "mem"


class UiTextAreaWidget(object):
    def setup_ui(self, textAreaUi):
        textAreaUi.setObjectName("textAreaUi")
        textAreaUi.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(textAreaUi)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(textAreaUi)
        self.widget.setMinimumSize(QtCore.QSize(600, 400))
        # self.widget.setMaximumSize(QtCore.QSize(600, 400))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_area = CustomQTextEdit(self.widget)  # QWidget.QTextEdit
        self.text_area.setMinimumSize(QtCore.QSize(600, 400))
        # self.text_area.setMaximumSize(QtCore.QSize(600, 400))
        self.text_area.setStyleSheet("QTextEdit{\n"
                                     "    background-color:rgb(35, 34, 39);\n"
                                     "    color:rgb(170, 170, 170);\n"
                                     "    border-bottom-left-radius:5px;\n"
                                     "    border-bottom-right-radius:5px;\n"
                                     "    padding:2px;\n"
                                     "}")
        self.text_area.setObjectName("text_area")
        self.text_area.setFont(QtGui.QFont("Calibri", 13))
        self.verticalLayout_2.addWidget(self.text_area)
        self.verticalLayout.addWidget(self.widget)
        self.text_area.setFocus()

        self.retranslate_ui(textAreaUi)
        QtCore.QMetaObject.connectSlotsByName(textAreaUi)

    def retranslate_ui(self, textAreaUi):
        _translate = QtCore.QCoreApplication.translate
        textAreaUi.setWindowTitle(_translate("textAreaUi", "Form"))


class CustomQTextEdit(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super(CustomQTextEdit, self).__init__(parent=parent)
        self.__HOST = "127.0.0.1"
        self.__PORT = 65432
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__HOST, self.__PORT))
        self.__successive_entries = []
        self.__displayed_entry_index = -1
        self.__i_regex = re.compile(r"in:.+:in")
        self.__o_regex = re.compile(r"out:.+:out")

    def send_request_to_alice(self, request):
        self.__socket.sendall(request)
        data = self.__socket.recv(1024)
        print("Received from alice : ", data)

    def close_connection_with_alice(self):
        self.__socket.close()

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key_Backspace:
            if not self.toPlainText().endswith(terminal_prompt):
                super().keyPressEvent(e)
            else:
                self.setTextColor(QtGui.QColor(terminal_io_color[0],
                                               terminal_io_color[1],
                                               terminal_io_color[2]))

        elif e.key() == QtCore.Qt.Key_Return:
            content = self.toPlainText()
            command = content[content.rfind(terminal_prompt) + len(terminal_prompt):]
            self.__successive_entries.append(command)
            self.__displayed_entry_index = len(self.__successive_entries) - 1
            execute_thread = threading.Thread(name="execute_thread", target=self.__execute_command, args=[command])
            execute_thread.setDaemon(True)
            execute_thread.start()
            # super().keyPressEvent(e)

        elif e.key() == QtCore.Qt.Key_Alt:
            self.clear()
            self.set_default_text()

        elif e.key() == QtCore.Qt.Key_Up:
            pass

        elif e.key() == QtCore.Qt.Key_Down:
            pass

        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.__move_cursor_to_end()

    def setText(self, text: str) -> None:
        self.__move_cursor_to_end()
        super().append(text)
        self.__move_cursor_to_end()

    def set_default_text(self):
        self.__set_prompt_color()
        self.setText(f"terminal@alice/{user} {terminal_prompt}")
        self.__set_default_io_color()

    def set_error_text(self, text):
        self.__set_error_color()
        self.setText(f"{text}\n")
        self.__set_default_io_color()

    def set_warning_text(self, text):
        self.__set_warning_color()
        self.setText(f"{text}\n")
        self.__set_default_io_color()

    def __set_default_io_color(self):
        self.setTextColor(QtGui.QColor(terminal_io_color[0],
                                       terminal_io_color[1],
                                       terminal_io_color[2]))

    def __set_prompt_color(self):
        self.setTextColor(QtGui.QColor(terminal_prompt_color[0],
                                       terminal_prompt_color[1],
                                       terminal_prompt_color[2]))

    def __set_error_color(self):
        self.setTextColor(QtGui.QColor(terminal_error_color[0],
                                       terminal_error_color[1],
                                       terminal_error_color[2]))

    def __set_warning_color(self):
        self.setTextColor(QtGui.QColor(terminal_warning_color[0],
                                       terminal_warning_color[1],
                                       terminal_warning_color[2]))

    def __move_cursor_to_end(self):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.setTextCursor(cursor)
        self.__set_default_io_color()

    def __execute_command(self, command: str):
        entry = self.__parse_command_line(command)
        if len(entry[0][0]) != 0:
            state = False
            to_print = ""
            try:
                if entry[0][0] == terminal_system_key_word:
                    request = f"{entry[0][1]}:{entry[1].__str__()}:{entry[2].__str__()}"
                    self.send_request_to_alice(bytes(request, "utf-8"))
                elif entry[0][0] == terminal_media_keyword:
                    request = f"{entry[0][1]}:{entry[1].__str__()}:{entry[2].__str__()}"
                    self.send_request_to_alice(bytes(request, "utf-8"))
                elif entry[0][0] == terminal_net__keyword:
                    request = f"{entry[0][1]}:{entry[1].__str__()}:{entry[2].__str__()}"
                    self.send_request_to_alice(bytes(request, "utf-8"))
                elif entry[0][0] == terminal_memory_keyword:
                    request = f"{entry[0][1]}:{entry[1].__str__()}:{entry[2].__str__()}"
                    self.send_request_to_alice(bytes(request, "utf-8"))
                else:
                    self.set_error_text(f"{entry[0][0]} is not valid command family")
                if state:
                    if to_print != "":
                        if to_print.startswith(terminal_warning_indicator):
                            self.set_warning_text(to_print)
                        else:
                            self.setText(to_print)
                    self.setText("status: [OK]")
                else:
                    if to_print != "":
                        if to_print.startswith(terminal_error_indicator):
                            self.set_error_text(to_print)
                        else:
                            self.setText(to_print)
                    self.setText("status: [FAILED]")
            except OSError as e:
                print(e)
        self.set_default_text()

    def __parse_command_line(self, command):
        inp = self.__i_regex.findall(command)
        print("inp1: ", inp)
        out = self.__o_regex.findall(command)
        if len(inp) != 0:
            inp = inp[0][3:len(inp[0])-3].split(" ")
            print("inp2: ", inp)
        if len(out) != 0:
            out = out[0][4:len(out[0])-4].split(" ")
        args = command.split(" ")[:2]
        print("args: ", args)
        print("inp: ", inp)
        print("out: ", out)
        return args, inp, out
