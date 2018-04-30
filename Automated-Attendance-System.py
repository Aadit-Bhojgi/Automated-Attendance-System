from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread
import GUI
import OCR
import sys
import json
import RowMarking
import RowSegregation
import DigitRecognition
import os
import inspect
import CSV


class Attendance(QtWidgets.QMainWindow, GUI.Ui_Attendance):
    def __init__(self):
        super(Attendance, self).__init__()
        self.setupUi(self)
        self.csv.hide()
        self.message.hide()
        self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
        self.CSV = CSV.CSV()
        self.image = self.RowsMarked = ''
        self.MainThread = MainThread()
        self.upload.clicked.connect(self.get_image)
        self.csv.clicked.connect(self.csv_file)
        self.list = []

    def get_image(self):
        if not self.MainThread.isRunning():
            filter_list = "Images (*.HEIC *.JPG *.PNG *.GIF *.JPEG *.jpeg *jpg *png *gif)"
            open_dir = QtWidgets.QFileDialog()
            options = QtWidgets.QFileDialog.Options()
            selected = open_dir.getOpenFileNames(open_dir, "Select Photos", '.', filter_list, options=options)
            if selected[0]:
                self.image = str(selected[0][0])
                self.upload.hide()
                self.message.show()
                self.MainThread = MainThread(self.image, self.path)
                self.MainThread.status.connect(self.status)
                self.MainThread.start()

    def message_alert(self, data):
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logo/Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg.setWindowIcon(icon)
        msg.setWindowTitle('Automated Attendance System - Message')
        msg.setText(data)
        msg.addButton(QtWidgets.QMessageBox.Ok)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        if msg.exec_() or msg.close():
            self.message.hide()
            self.upload.show()

    def status(self, result):
        if result == 'Error':
            self.message_alert('Image you uploaded is not captured properly\nPlease Re-Take the Image.')
        else:
            self.message.hide()
            self.csv.show()
            self.list = result[0], result[1], result[2], result[3]

    def csv_file(self):
        self.CSV.organise_data(self.list[0], self.list[1], self.list[2], self.list[3])
        open_dir = QtWidgets.QFileDialog()
        options = QtWidgets.QFileDialog.Options()
        filters = "CSV Files (*.csv *csv)"
        file = open_dir.getSaveFileName(open_dir, "Save File", '.', filter=filters, options=options)
        if file[0]:
            self.CSV.write(file[0])
            self.csv.hide()
            self.upload.show()


class MainThread(QThread):
    status = QtCore.pyqtSignal(object)

    def __init__(self, image='', path=''):
        QThread.__init__(self)
        self.path = path
        self.image = image
        self.result = []
        self.RowsMarked = ''

    @staticmethod
    def sanity_check(names):
        while names[-1][:1] != '(' and names[-1][-1:] != ')':
            del names[-1]
        return names

    def mark_rows(self):
        return RowMarking.RowMarking(self.image, self.path).rows()

    def segregate_rows(self, names, students_strength):
        RowSegregation.RowSegregate(self.RowsMarked, names, students_strength, self.path).crop()
        os.remove(self.RowsMarked)

    def digit_recognition(self, students_strength):
        self.result = DigitRecognition.DigitRecognition(self.path, students_strength).get_digits_path_and_predict()
        if self.result[0]:
            self.status.emit(self.result)
        else:
            self.status.emit('Error')

    def play(self):
        file_data = OCR.OCR.ocr_space_file(filename=self.image, language='eng')
        response = json.loads(file_data)
        names = response["ParsedResults"][0]["ParsedText"].split(' \r\n')
        names = self.sanity_check(names)
        students_strength = int((len(names) - 1) / 2)
        self.RowsMarked = self.mark_rows()
        self.segregate_rows(names, students_strength)
        self.digit_recognition(students_strength)

    def run(self):
        self.play()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Attendance()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
