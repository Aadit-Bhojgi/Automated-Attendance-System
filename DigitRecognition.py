import os
import re
import DigitRecognizer
import shutil


class DigitRecognition:
    def __init__(self, path, students_strength):
        self.path = path
        self.students_strength = students_strength
        self.digits = []
        self.year = []
        self.date = []
        self.students = []
        self.directory = ''
        self.PredictedDigits = []

    @staticmethod
    def atoi(text):
        return int(text) if text.isdigit() else text

    @staticmethod
    def natural_keys(text):
        return [DigitRecognition.atoi(c) for c in re.split('(\d+)', text)]

    def get_digits_path_and_predict(self):
        for directory, dir_name, filename in sorted(os.walk(self.path + '/AttendanceSheet')):
            filename.sort(key=self.natural_keys)
            if filename and directory:
                self.digits = filename
                self.directory = directory
        for filename in self.digits:
            if filename[0:6] == '.Dates':
                self.date.append(filename)
            elif filename[0:5] == '.Year':
                self.year.append(filename)
            else:
                self.students.append(filename.strip('-1.png'))
        students_strength_perday = int(len(self.date) / 4)
        if len(self.year) == 4 and int(len(self.date) % 4) == 0 \
                and (students_strength_perday * self.students_strength) == len(self.students):
            recognizer = DigitRecognizer.Recognizer()
            recognizer.TrainRecognizer()
            self.PredictedDigits = recognizer.TestRecognizer(self.directory, self.digits)
        shutil.rmtree(self.directory + '/', ignore_errors=True)
        return (list(self.PredictedDigits), list(self.students[::students_strength_perday]), [int(len(self.date))],
                [students_strength_perday])


if __name__ == '__main__':
    pass
