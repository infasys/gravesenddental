import sys,time
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtWidgets,QtGui
from mywindow import MyMainWindow
from PersonClass import Person
import platform,requests
from spashscreen import SpashScreen
from mysocket import ListenWebsocket
import logging,threading,json
class PyShine_THREADS_APP(MyMainWindow):
    appendSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(PyShine_THREADS_APP, self).__init__()
        self.showAll = 2;
        self.calls = []
        self.platformName = platform.node()
        timer = QtCore.QTimer(self)
        try:
            self.aList = json.loads(open("phones.json", "r").read())
        except:
            self.aList = [];
            pass
        print(self.aList)
        for p in self.aList:
            pname = p['name'];
            self.ui.pushButton_tahid = QtWidgets.QPushButton(self.ui.frame_3)
            self.ui.pushButton_tahid.setText(pname)
            self.ui.pushButton_tahid.setObjectName("pushButton_"+pname)
            self.ui.verticalLayout.addWidget(self.ui.pushButton_tahid)
            self.ui.pushButton_tahid.setStyleSheet("background-color: orange;color:black;font-weight:bold;padding:8px;font-size:24px;")
            self.ui.pushButton_tahid.clicked.connect(self.dialNumber1)
            print(p['name'])
        # timerPing = QtCore.QTimer(self)
        # timerPing.timeout.connect(self.showPing)
        # timerPing.start(12000)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.thread = ListenWebsocket()
        app.aboutToQuit.connect(self.thread.stop)
        self.thread.start()
        self.thread.any_signal.connect(self.my_function)
        self.ui.rbtn1.toggled.connect(self.onClicked1)
        self.ui.rbtn2.toggled.connect(self.onClicked2)
        self.ui.rbtn3.toggled.connect(self.onClicked3)
        self.ui.tableWidget.selectionModel().selectionChanged.connect(self.selChanged)
    def thread_function(self,myname,username,password,uri,ext):
        print("DIALING NUMBER")
        logging.warning("Thread %s: starting", username)
        number = self.ui.lblNumber.text()
        number = number.replace(" ", "")
        if len(number)>8:
            myurl = 'http://'+username+':'+password+'@'+uri+'/servlet?key=number='+number+'&outgoing_uri='+ext+''
            logging.warning("URL %s: dialing", myurl)
            r = requests.get(myurl, verify=False)
        logging.warning("Thread %s: finishing", username)
        print("DONE")
    def dialNumber1(self,test):
        sending_button = self.sender()
        btnname = sending_button.text()
        for p in self.aList:
            pname = p['name'];
            if(btnname==pname):
                print("START"+pname)
                self.callthread = threading.Thread(target=self.thread_function, args=(pname,p['username'],p['password'],p['uri'],p['ext']))
                self.callthread.start()
        # sending_button
        print("START")
        pass
    def onClicked1(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.showAll = 1;
        self.updateTable()
    def onClicked2(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.showAll = 2;
        self.updateTable()
    def onClicked3(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.showAll = 3;
        self.updateTable()
    def selChanged(self, selected, deselected):
        try: 
            a1 = selected.indexes()[1].data()
            print(a1)
            self.ui.lblNumber.setText(a1)
        except:
            self.ui.lblNumber.setText("")
            pass
    def updateTableTiming(self):
        pass
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
                self.ui.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(str(timestr)))
                item = self.ui.tableWidget.item(row,2)
                if(item  is not None):
                    print(item)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
                    pass
            row=row+1;
    def updateTable(self):
        fb = QtGui.QFont()
        fb.setBold(True)
        fb.setPixelSize(18)
        row = 0

        self.selectedindex = self.ui.tableWidget.selectionModel().selectedIndexes();
        self.ui.tableWidget.setRowCount(row)
        self.t = time.process_time()
        logging.warning("============================\nUPDATE START: %s",0)


        if(self.showAll==2):
            self.ui.tableWidget.setColumnHidden(4,True)
        elif(self.showAll==3):
            self.ui.tableWidget.setColumnHidden(4,True)
        else:
            self.ui.tableWidget.setColumnHidden(4,False)
        self.ui.tableWidget.setRowCount(len(self.calls))
        
        self.calls.sort(key=lambda x: x.timestamp, reverse=True)
        for person in self.calls:
            isdisplay = False
             
            if(self.showAll==2):
                if(person.status=="MISSED"):
                    isdisplay = True
            elif(self.showAll==3):
                if(person.status=="UNRETURNED"):
                    isdisplay = True
            else:
                isdisplay = True
                if(person.status=="UNRETURNED"):
                    isdisplay = False
                
            if(isdisplay):
                self.ui.tableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(str(person.date)))
                itemdate = self.ui.tableWidget.item(row,0)
                itemdate.setForeground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                self.ui.tableWidget.setItem(row,2,QtWidgets.QTableWidgetItem( ""+str(person.count)+""))
                itemdate = self.ui.tableWidget.item(row,2)
                itemdate.setForeground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                self.ui.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(str(person.number)))
                itemnum = self.ui.tableWidget.item(row,1)
                itemnum.setForeground(QtGui.QBrush(QtGui.QColor(45, 45, 45)))
                itemnum.setFont(fb)
                timestr2 = ""
                timestr = ""
                self.ui.tableWidget.setItem(row,4,QtWidgets.QTableWidgetItem(""))
                self.ui.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(""))
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
                    self.ui.tableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(str(timestr)))
                    item = self.ui.tableWidget.item(row,3)
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
                    self.ui.tableWidget.setItem(row,4,QtWidgets.QTableWidgetItem(str(timestr2)))
                    item = self.ui.tableWidget.item(row,4)
                    item.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
                    item.setForeground(QtGui.QBrush(QtGui.QColor(100, 100, 100)))
                self.ui.tableWidget.setItem(row,5,QtWidgets.QTableWidgetItem(str(person.status)))
                item = self.ui.tableWidget.item(row,5)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                row=row+1;
        logging.warning("============================\nUPDATE Finish: %s",time.process_time() - self.t)
        self.ui.tableWidget.setRowCount(row)
        logging.warning("============================\nUPDATE Finish: %s",time.process_time() - self.t)
        if(len(self.selectedindex)>0):
            self.ui.tableWidget.selectionModel().select(self.selectedindex[0], QtCore.QItemSelectionModel.Select | QtCore.QItemSelectionModel.Rows );
            logging.warning("============================\nSELECT: %s",time.process_time() - self.t)
    def loaddata(self):
        self.updateTable();
    def my_function(self,msg,code,additional):
        if code == 23:
            if additional:
                if "total" in additional:self.ui.label_tot.setText(str(additional["total"]))
                if "active" in additional:self.ui.label_act.setText(str(additional["active"]))
                if "missed" in additional:self.ui.label_mis.setText(str(additional["missed"]))
                if "average" in additional:
                    if(additional["average"]):
                        if(int(additional["average"])>0):
                            m, s = divmod(int(additional["average"]), 60)
                            if(s):
                                timestr = f"{s} Secs"
                            if(m):
                                timestr = f"{m} Mins\n{s} Secs"
                            self.ui.label_out.setText(timestr)
                if "calllist" in additional:
                    self.calls = []
                    calllist = additional["calllist"]
                    
                    for x in calllist:
                        # print(str(x))
                        self.calls.append(Person(x["timestamp"],x["callid"],x["date"],x["wait"],x["total"],x["number"],x["status"],x["count"])) 
                    self.updateTable()
    def showTime(self):
        current_time = QtCore.QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        self.ui.lcdpanel.display(label_time)
        self.updateTableTiming()
    # def showPing(self):
    #     current_time = QtCore.QTime.currentTime()
    #     label_time = current_time.toString('hh:mm')
    #     # self.thread.sendmsg({"time":label_time,"type":1,"msg":"ping"})
    #     print(label_time);
    #     print("TAHID")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    SpashScreen()
    mainWindow = PyShine_THREADS_APP()
    # mainWindow.showFullScreen()
    mainWindow.show()
    sys.exit(app.exec_())
