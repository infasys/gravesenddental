from myimg import myimg
from mylayout2 import Ui_MainWindow
from PyQt5 import QtWidgets,QtGui,QtCore
import base64
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(888, 200)
        pm = QtGui.QPixmap()
        pm.loadFromData(base64.b64decode(myimg.b64_data))
        self.ui.label.setPixmap(pm)
        self.ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows);
        # self.tableWidget.setStyleSheet("QTableWidget::item { padding: 50px }");
        font = QtGui.QFont('PT Mono', 14, QtGui.QFont.Monospace)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias);
        self.ui.tableWidget.horizontalHeader().setFont( font );
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch);
        self.ui.tableWidget.horizontalHeader().setMinimumSectionSize(60)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents);
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents);
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed);
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents);
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents);
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents);
        self.ui.tableWidget.horizontalHeader().resizeSection(4, 85);
        self.ui.tableWidget.horizontalHeader().resizeSection(0, 140);
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers);
        self.ui.btnQuit.clicked.connect(self.quitApp)
        self.ui.lcdpanel.display("12:33")
        self.ui.lcdpanel.setMinimumWidth(self.ui.lcdpanel.width()+1);
        self.ui.rbtn2.setChecked(True)
        self.ui.lblNumber.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse);
        self.ui.tableWidget.setShowGrid(False)

        # self.ui.treeWidget.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents);
        
        # font = QtGui.QFont("Courier")
        
        # font.setStyleHint(QtGui.QFont.Monospace)
        # font.setBold(True)
        self.ui.tableWidget.setFont(font);
        self.ui.tableWidget.setStyleSheet('''
       

        QTableView::item
{
  border: 0px;
  padding: 4px 5px;
}
          ''')



#         self.ui.treeWidget.header().setStyleSheet('''
#     QHeaderView {
#         /* set the bottom border of the header, in order to set a single 
#            border you must declare a generic border first or set all other 
#            borders */
#         border: none;
#         border-bottom: 2px solid black;
#     }

#     QHeaderView::section:horizontal {
#         /* set the right border (as before, the overall border must be 
#            declared), and a minimum height, otherwise it will default to 
#            the minimum required height based on the contents (font and 
#            decoration sizes) */
#         border: none;
#         border-right: 1px solid black;
#         padding:5px 20px;
#     }
# ''')

    def quitApp(self):
        self.close()
        pass