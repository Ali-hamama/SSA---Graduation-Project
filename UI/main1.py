from PyQt5 import QtCore, QtGui, QtWidgets
import main_functions as mf
import sys
import os
from wait_window import Ui_wait_window
from report import Ui_Report_screen
import time
os.chdir('E:\Graduation Project\Full Project')
import Logic as logic



"""
Main screen
"""
class Ui_MainWindow(object):

    def analysis(self,path,interval,name):
        """
        This function connected with 'Analyse' button, it's starting the analysis process 
        """
        data_length, ok = mf.path_validate(path,interval,name)
        if ok :
           self.window_progress = QtWidgets.QMainWindow()
           self.ui_progress = Ui_wait_window()
           self.ui_progress.setupUi(self.window_progress, data_length)
           self.window_progress.show()
           time.sleep(2)
           duration = mf.split_video(path,interval)
           attentiveness_level,image_path = logic.analyse(self.ui_progress,data_length, interval, name)
           self.ui_progress.progressBar.setValue(100)
           self.window_progress.close()
           self.get_report(attentiveness_level,name,image_path,interval,duration)
           

    def get_report(self,attentiveness_level,name,image_path,interval,duration):
        self.window_report = QtWidgets.QMainWindow()
        self.ui_report = Ui_Report_screen()
        self.ui_report.setupUi(self.window_report,image_path,name,duration,attentiveness_level,interval)
        self.window_report.show()
        mf.save_report(image_path,name,attentiveness_level,interval,round(duration/60,2))



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(606, 500)
        MainWindow.setStyleSheet("background-color: rgb(91, 145, 140);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.analyse_btn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda:self.analysis(self.path_txt.text(),int(self.interval_txt.text()),self.name_txt.text()))
        self.analyse_btn.setGeometry(QtCore.QRect(10, 400, 580, 81))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.analyse_btn.setFont(font)
        self.analyse_btn.setStyleSheet("#analyse_btn{\n"
"    background-color: rgb(55, 87, 90);\n"
"    border: 0px;\n"
"    border-radius: 10px;\n"
"    color: white;\n"
"    font-size: 23px;\n"
"}\n"
"\n"
"#analyse_btn:hover{\n"
"    \n"
"    background-color: rgb(99, 130, 144);\n"
"    border: 1px solid rgb(132, 211, 203);\n"
"    border-radius: 15px;\n"
"    border-color: ;\n"
"    color: white;\n"
"    font-size: 25px;\n"
"}\n"
"\n"
"#analyse_btn:pressed{\n"
"    background-color: rgb(55, 87, 90);\n"
"    border: 1px solid rgb(132, 211, 203);\n"
"    border-radius: 15px;\n"
"    color: white;\n"
"    font-size: 25px;\n"
"}")
        self.analyse_btn.setObjectName("analyse_btn")
        self.main_lbl = QtWidgets.QLabel(self.centralwidget)
        self.main_lbl.setGeometry(QtCore.QRect(0, 0, 611, 101))
        font = QtGui.QFont()
        font.setFamily("Perpetua Titling MT")
        font.setPointSize(36)
        self.main_lbl.setFont(font)
        self.main_lbl.setStyleSheet("color: rgb(255, 254, 237);\n"
"background-color: rgb(110, 175, 169);\n"
"border-bottom: 1px solid rgb(132, 211, 203);")
        self.main_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.main_lbl.setObjectName("main_lbl")
        self.desc_lbl = QtWidgets.QLabel(self.centralwidget)
        self.desc_lbl.setGeometry(QtCore.QRect(20, 250, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.desc_lbl.setFont(font)
        self.desc_lbl.setStyleSheet("color: rgb(211, 211, 211);")
        self.desc_lbl.setObjectName("desc_lbl")
        self.path_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.path_txt.setGeometry(QtCore.QRect(140, 240, 391, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.path_txt.setFont(font)
        self.path_txt.setStatusTip("")
        self.path_txt.setAccessibleDescription("")
        self.path_txt.setStyleSheet("#path_txt{\n"
"    background-color: rgb(55, 87, 90);\n"
"    border: 1px solid rgb(55, 87, 90);\n"
"    border-radius: 8;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"#path_txt:focus{\n"
"    background-color:  rgb(99, 130, 144);\n"
"    border: 1px solid rgb(132, 211, 203);\n"
"    border-radius: 8;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"    font-size: 13px;\n"
"}")
        self.path_txt.setInputMask("")
        self.path_txt.setText("")
        self.path_txt.setClearButtonEnabled(True)
        self.path_txt.setObjectName("path_txt")
        self.interval_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.interval_txt.setGeometry(QtCore.QRect(140, 310, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.interval_txt.setFont(font)
        self.interval_txt.setStatusTip("")
        self.interval_txt.setAccessibleDescription("")
        self.interval_txt.setStyleSheet("#interval_txt{\n"
"    background-color: rgb(55, 87, 90);\n"
"    border: 1px solid rgb(55, 87, 90);\n"
"    border-radius: 8;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"#interval_txt:focus{\n"
"    background-color: rgb(99, 130, 144);\n"
"    border: 1px solid rgb(132, 211, 203);\n"
"    border-radius: 8;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"    font-size: 13px;\n"
"}")
        self.interval_txt.setInputMask("")
        self.interval_txt.setText("")
        self.interval_txt.setClearButtonEnabled(True)
        self.interval_txt.setObjectName("interval_txt")
        self.desc_lbl_2 = QtWidgets.QLabel(self.centralwidget)
        self.desc_lbl_2.setGeometry(QtCore.QRect(20, 320, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.desc_lbl_2.setFont(font)
        self.desc_lbl_2.setStyleSheet("color: rgb(211, 211, 211);")
        self.desc_lbl_2.setObjectName("desc_lbl_2")
        self.desc_lbl_3 = QtWidgets.QLabel(self.centralwidget)
        self.desc_lbl_3.setGeometry(QtCore.QRect(360, 320, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.desc_lbl_3.setFont(font)
        self.desc_lbl_3.setStyleSheet("color: rgb(211, 211, 211);")
        self.desc_lbl_3.setObjectName("desc_lbl_3")
        self.desc_lbl_4 = QtWidgets.QLabel(self.centralwidget)
        self.desc_lbl_4.setGeometry(QtCore.QRect(20, 180, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.desc_lbl_4.setFont(font)
        self.desc_lbl_4.setStyleSheet("color: rgb(211, 211, 211);")
        self.desc_lbl_4.setObjectName("desc_lbl_4")
        self.name_txt = QtWidgets.QLineEdit(self.centralwidget)
        self.name_txt.setGeometry(QtCore.QRect(140, 170, 391, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.name_txt.setFont(font)
        self.name_txt.setStatusTip("")
        self.name_txt.setAccessibleDescription("")
        self.name_txt.setStyleSheet("#name_txt{\n"
"    background-color: rgb(55, 87, 90);\n"
"    border: 1px solid rgb(55, 87, 90);\n"
"    border-radius: 8;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"#name_txt:focus{\n"
"    background-color:  rgb(99, 130, 144);\n"
"    border: 1px solid rgb(132, 211, 203);\n"
"    border-radius: 8;\n"
"    color: white;\n"
"    padding-left: 10px;\n"
"    font-size: 13px;\n"
"}")
        self.name_txt.setInputMask("")
        self.name_txt.setText("")
        self.name_txt.setClearButtonEnabled(True)
        self.name_txt.setObjectName("name_txt")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.analyse_btn.setText(_translate("MainWindow", "Analyse"))
        self.main_lbl.setText(_translate("MainWindow", "Monitoring Tool"))
        self.desc_lbl.setText(_translate("MainWindow", "Video path:"))
        self.path_txt.setPlaceholderText(_translate("MainWindow", "Put the PATH Here.."))
        self.interval_txt.setPlaceholderText(_translate("MainWindow", "Put the interval in sec"))
        self.desc_lbl_2.setText(_translate("MainWindow", "Time intervals:"))
        self.desc_lbl_3.setText(_translate("MainWindow", "Sec."))
        self.desc_lbl_4.setText(_translate("MainWindow", "Student Name:"))
        self.name_txt.setPlaceholderText(_translate("MainWindow", "Put Student\'s name Here.."))


if __name__ == "__main__":
    
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
