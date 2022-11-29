from PyQt5 import QtCore, QtGui, QtWidgets
import main_functions as mf



"""
Waiting and progress window 
"""
class Ui_wait_window(object):
    
    def setupUi(self, wait_window,num_videos):
        wait_window.setObjectName("wait_window")
        wait_window.resize(364, 91)
        self.centralwidget = QtWidgets.QWidget(wait_window)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 50, 331, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        wait_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(wait_window)
        QtCore.QMetaObject.connectSlotsByName(wait_window)

        

    def retranslateUi(self, wait_window):
        _translate = QtCore.QCoreApplication.translate
        wait_window.setWindowTitle(_translate("Progress", "Progress"))
        self.label.setText(_translate("wait_window", "Analysis in progress, please wait.."))
