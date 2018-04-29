# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Attendance(object):
    def setupUi(self, Attendance):
        Attendance.setObjectName("Attendance")
        Attendance.resize(776, 346)
        Attendance.setMinimumSize(QtCore.QSize(776, 346))
        Attendance.setMaximumSize(QtCore.QSize(776, 346))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Attendance.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Attendance)
        self.centralwidget.setMinimumSize(QtCore.QSize(776, 346))
        self.centralwidget.setMaximumSize(QtCore.QSize(776, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-20, -50, 951, 441))
        self.label.setObjectName("label")
        self.upload = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.upload.setEnabled(True)
        self.upload.setGeometry(QtCore.QRect(450, 170, 161, 71))
        self.upload.setMinimumSize(QtCore.QSize(161, 71))
        self.upload.setMaximumSize(QtCore.QSize(161, 71))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.upload.setFont(font)
        self.upload.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.upload.setStyleSheet("font: 16pt \"Yu Gothic UI Semibold\";\n"
"\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Logo/new-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.upload.setIcon(icon1)
        self.upload.setIconSize(QtCore.QSize(50, 50))
        self.upload.setDefault(False)
        self.upload.setObjectName("upload")
        self.message = QtWidgets.QLabel(self.centralwidget)
        self.message.setEnabled(False)
        self.message.setGeometry(QtCore.QRect(410, 190, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setObjectName("message")
        self.csv = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.csv.setEnabled(True)
        self.csv.setGeometry(QtCore.QRect(470, 170, 111, 71))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.csv.setFont(font)
        self.csv.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.csv.setStyleSheet("font: 16pt \"Yu Gothic UI Semibold\";\n"
"\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Logo/csv-file-format-extension.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.csv.setIcon(icon2)
        self.csv.setIconSize(QtCore.QSize(50, 50))
        self.csv.setDefault(False)
        self.csv.setObjectName("csv")
        Attendance.setCentralWidget(self.centralwidget)

        self.retranslateUi(Attendance)
        QtCore.QMetaObject.connectSlotsByName(Attendance)

    def retranslateUi(self, Attendance):
        _translate = QtCore.QCoreApplication.translate
        Attendance.setWindowTitle(_translate("Attendance", "Automated Attendance System"))
        self.label.setText(_translate("Attendance", "<html><head/><body><p><img src=\":/Logo/bg.png\"/></p></body></html>"))
        self.upload.setText(_translate("Attendance", "Upload"))
        self.message.setText(_translate("Attendance", "<html><head/><body><p><span style=\" font-size:10pt; color:#333333;\">Getting Your CSV FIle Ready....</span></p></body></html>"))
        self.csv.setText(_translate("Attendance", "File"))

import Resource

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Attendance = QtWidgets.QMainWindow()
    ui = Ui_Attendance()
    ui.setupUi(Attendance)
    Attendance.show()
    sys.exit(app.exec_())

