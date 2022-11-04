
# Tahid here in this place
import json
from turtle import update
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time, threading
import socketio
import base64
from myimg import myimg
i = 0

class Person(object):

    def __init__(self,timestamp,callid,date, wait,totaltime, number,status):

        self.timestamp = timestamp
        self.callid = callid
        self.date = date
        self.wait = wait
        self.totaltime = totaltime
        self.number = number
        self.status = status

class PyShine_THREADS_APP(QtWidgets.QMainWindow):
    appendSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(PyShine_THREADS_APP, self).__init__()
        # QtWidgets.QMainWindow.__init__(self)
        self.i=1
        self.showAll = True;
        self.ui = uic.loadUi('tahidtest.ui',self)
        
        self.resize(888, 200)
		# self.listView = QtWidgets.QListView
        self.calls = []
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(myimg.b64_data))
        self.label.setPixmap(pm)
        self.textEdit.hide();
        self.label_tot.setText("TOT")
        self.label_act.setText("ACT")
        self.label_mis.setText("MIS")
        self.label_out.setText("OUT")
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows);
        # self.tableWidget.setStyleSheet("QTableWidget::item { padding: 50px }");
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch);
        self.tableWidget.horizontalHeader().setMinimumSectionSize(60)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Fixed);
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed);
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents);
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents);
        self.tableWidget.horizontalHeader().resizeSection(4, 90);
        self.tableWidget.horizontalHeader().resizeSection(0, 120);
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers);
        
        self.btnQuit.clicked.connect(self.quitApp)
        # self.btnRemove.clicked.connect(self.start_worker_2)
        self.lcdpanel.display("12:33")
        self.lcdpanel.setMinimumWidth(self.lcdpanel.width()+1);
        timer = QtCore.QTimer(self)
        timerPing = QtCore.QTimer(self)
        timerPing.timeout.connect(self.showPing)
        timerPing.start(12000)
        # adding action to timer
        timer.timeout.connect(self.showTime)
        # update the timer every second
        timer.start(1000)
        self.thread = ListenWebsocket()
        app.aboutToQuit.connect(self.thread.stop)
        self.thread.start()
        self.thread.any_signal.connect(self.my_function)
        self.loaddata()
        self.rbtn1.setChecked(True)
        self.rbtn1.toggled.connect(self.onClicked1)
    def onClicked1(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.showAll = True;
        else:
            self.showAll = False;
        self.updateTable()
        print("Pressed B"+str(self.showAll))
    def updateTableTiming(self):
        row = 0
        for person in self.calls:
            if (str(person.status)=="QUEUE"):
                person.wait = int(person.wait)
                person.wait = person.wait+1;
                timestr = "";
                if(int(person.wait)<72):
                    timestr = f"{person.wait} secs";
                else:
                    m, s = divmod(person.wait, 60)
                    if(s):
                        timestr = f"{s} secs"
                    if(m):
                        timestr = f"{m} mins, {s} s"
                self.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(str(timestr)))
                item = self.tableWidget.item(row,2)
                item.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
                
                pass
            row=row+1;
    def updateTable(self):
        row = 0
        if(not self.showAll):
            self.tableWidget.setColumnHidden(3,True)
        else:
            self.tableWidget.setColumnHidden(3,False)
        self.tableWidget.setRowCount(len(self.calls))
        self.calls.sort(key=lambda x: x.timestamp, reverse=True)
        for person in self.calls:
            isdisplay = False
             
            if(not self.showAll):
                if(person.status=="MISSED"):
                    isdisplay = True
                if(person.status=="QUEUE"):
                    isdisplay = True
                if(person.status=="ACTIVE"):
                    isdisplay = True
            else:
                isdisplay = True
            if(isdisplay):
                self.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(str(person.date)))
                itemdate = self.tableWidget.item(row,0)
                itemdate.setForeground(QtGui.QBrush(QtGui.QColor(170, 170, 170)))
                self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(str(person.number)))
                timestr2 = ""
                timestr = ""
                self.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(""))
                self.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(""))
                if(person.wait):
                    timestr = "";
                    if(int(person.wait)<72):
                        timestr = f"{person.wait} secs";
                    else:
                        m, s = divmod(int(person.wait), 60)
                        if(s):
                            timestr = f"{s} secs"
                        if(m):
                            timestr = f"{m} mins, {s} s"
                    self.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(str(timestr)))
                    item = self.tableWidget.item(row,2)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
                    item.setForeground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                if(person.totaltime):
                    timestr2 = "";
                    if(int(person.totaltime)<72):
                        timestr2 = f"{person.totaltime} secs";
                    else:
                        m, s = divmod(int(person.totaltime), 60)
                        if(s):
                            timestr2 = f"{s} secs"
                        if(m):
                            timestr2 = f"{m} mins, {s} s"
                    self.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(str(timestr2)))
                    item = self.tableWidget.item(row,3)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
                    item.setForeground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                self.tableWidget.setItem(row,4,QtWidgets.QTableWidgetItem(str(person.status)))
                # self.tableWidget.setItem(row,5,QtWidgets.QTableWidgetItem(str(person.callid)))
                item = self.tableWidget.item(row,4)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                row=row+1;
        self.tableWidget.setRowCount(row)
    def loaddata(self):
        self.updateTable();
    def my_function(self,msg,code,additional):
        label_time = QtCore.QTime.currentTime().toString('hh:mm:ss')
        if code==1 :
            self.textEdit.insertPlainText(label_time+" "+msg+"\n");
            self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum());
        elif code == 23:
            if additional:
                if "total" in additional:self.label_tot.setText(str(additional["total"]))
                if "active" in additional:self.label_act.setText(str(additional["active"]))
                if "missed" in additional:self.label_mis.setText(str(additional["missed"]))
                if "average" in additional:
                    
                    m, s = divmod(int(additional["average"]), 60)
                    if(s):
                        timestr = f"{s} Secs"
                    if(m):
                        timestr = f"{m} Mins\n{s} Secs"
                    self.label_out.setText(timestr)
                if "calllist" in additional:
                    self.calls = []
                    calllist = additional["calllist"]
                    for x in calllist:
                        # print(str(x))
                        self.calls.append(Person(x["timestamp"],x["callid"],x["date"],x["wait"],x["total"],x["number"],x["status"])) 
                    self.updateTable()
            self.textEdit.insertPlainText(label_time+" "+msg+"\n");
            self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum());
            pass
        elif code == 5:
            time.sleep(5)
            self.thread.stop()
            self.thread = ListenWebsocket()
            self.thread.start()
            self.thread.any_signal.connect(self.my_function)
    def showTime(self):
        current_time = QtCore.QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        self.lcdpanel.display(label_time)
        self.updateTableTiming()
    def showPing(self):
        current_time = QtCore.QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        self.thread.sendmsg({"time":label_time,"type":1,"msg":"ping"})
    def quitApp(self):
        self.close()
        

class ListenWebsocket(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(str,int,dict)
    def __init__(self, parent=None):
        super(ListenWebsocket, self).__init__(parent)
        self._lock = threading.Lock()
        # self.sio = socketio.Client()
        self.sio = socketio.Client(logger=True, engineio_logger=True)
        try:
            self.sio.connect('https://sock.infasys.co.uk')
        except socketio.exceptions.ConnectionError as err:
            print("ConnectionError: %s", err)
        @self.sio.event
        def connect():
            print("I'm connected!")
        @self.sio.event
        def connect_error(data):
            print("The connection failed!")
        @self.sio.event
        def disconnect():
            print("I'm disconnected!")

        @self.sio.on('chat message')
        def message(data):
            if isinstance(data, dict):
                # print(json.dumps(data))
                # print(json.dumps(data['msg']))
                self.any_signal.emit(data['msg'],data['type'],data)
            if isinstance(data, str):
                self.any_signal.emit(data,1,data)
        @self.sio.on('*')
        def catch_all(event, data):
            # print(data)
            pass
        print('my sid is', self.sio.sid)
    def sendmsg(self,msg):
        # try:
            self.sio.emit('chat message',msg)
        # except socketio.exceptions.BadNamespaceError as err:
        #     print("BadNamespaceError")
    def _do_before_done(self):
        print('waiting 3 seconds before thread done..')
        for i in range(3, 0, -1):
            print('{0} seconds left...'.format(i))
            self.sleep(1)
        self.sio.disconnect()
        print('ok, thread done.')
    def stop(self):
        print('received stop signal from window.')
        with self._lock:
            self._do_before_done()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    splash_pix = QtGui.QPixmap('bells.png')

    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)
    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0, splash_pix.height() - 50, splash_pix.width(), 20)

    # splash.setMask(splash_pix.mask())

    splash.show()
    splash.showMessage("", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)
    for i in range(1, 11):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
           app.processEvents()
    mainWindow = PyShine_THREADS_APP()
    mainWindow.showFullScreen()
    mainWindow.show()
    splash.hide()
    sys.exit(app.exec_())
