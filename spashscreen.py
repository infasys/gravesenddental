from myimg import myimg
from PyQt5 import QtWidgets,QtGui
from PyQt5 import QtCore, QtWidgets,QtGui
import time,sys,base64;
class SpashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        
        pm = QtGui.QPixmap() 
        pm.loadFromData(base64.b64decode(myimg.b64_data2))
        super(SpashScreen, self).__init__(pm,QtCore.Qt.WindowStaysOnTopHint)
        self.pixmap = pm
        # QtCore.QTimer.singleShot(5000, self, self.close()); 
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setEnabled(False)
        # adding progress bar
        progressBar = QtWidgets.QProgressBar(self)
        progressBar.setMaximum(100)
        progressBar.setGeometry(0, pm.height() - 50, pm.width(), 20)
        self.show()
        # self.showMessage("", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        p = 0.03
        for i in range(1, 100):
            m = i;
            progressBar.setValue(m)
            t = time.time()
            
            if i>10:
                p = 0.01
            if i>40:
                p = 0.003
            if i>50:
                p = 0.0009
            while time.time() < t + p:
                QtWidgets.QApplication.processEvents()
                pass
        self.hide()