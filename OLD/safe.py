
from threading import Thread
from time import sleep
from PyQt5.QtGui import QTextCursor
import websockets
import websocket
import sys
from PyQt5.QtWidgets import QDialog,QApplication, QProgressBar,QLabel,QMainWindow,QTextEdit,QPushButton,QVBoxLayout
from PyQt5 import QtCore
import shlex
import faulthandler
faulthandler.enable()

class Window(QDialog):
    appendSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.v_layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.btnOne = QPushButton("SEND...");
        self.v_layout.addWidget(QLabel("E-Mail Me"))
        self.v_layout.addWidget(self.textEdit)
        self.v_layout.addWidget(self.btnOne)
        self.setLayout(self.v_layout)
        self.thread = ListenWebsocket()
        self.thread.start()
        self.thread.any_signal.connect(self.my_function)
        self.btnOne.pressed.connect(self.onMyBtnClick)
    def my_function(self,msg):
        self.textEdit.insertPlainText(msg);
        self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum());
    def onMyBtnClick(self):
        print("Pressed")
        self.updateText("(Make sure 'QTextCursor' is registered using qRegisterMetaType().)(Make sure 'QTextCursor' is registered using qRegisterMetaType().)(Make sure 'QTextCursor' is registered using qRegisterMetaType().)(Make sure 'QTextCursor' is registered using qRegisterMetaType().)(Make sure 'QTextCursor' is registered using qRegisterMetaType().)(Make sure 'QTextCursor' is registered using qRegisterMetaType().)(Make sure 'QTextCursor' is registered using qRegisterMetaType().)\n")
    def updateText(self,msg):
        try:
            self.textEdit.insertPlainText(msg);
        except ValueError:
            pass
        
class ListenWebsocket(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)

        websocket.enableTrace(True)

        self.WS = websocket.WebSocketApp("ws://localhost:8765",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close) 

    def run(self):
        #ws.on_open = on_open
        self.WS.run_forever()


    def on_message(self, ws, message):
        for i in range(100):
            self.any_signal.emit(message)
            sleep(0.01)
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    @QtCore.pyqtSlot()
    def stop(self):
        print("STOP")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setQuitOnLastWindowClosed(True)

    window = Window()
    window.show()

    sys.exit(app.exec_())