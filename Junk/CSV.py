import os
import inspect
import GetDigits


class CSV:
    def __init__(self, students_data):
        self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
        self.files = []
        self.directory = []
        self.StudentsData = students_data
        self.get_digits = GetDigits.GetDigits()

    def get_students_data(self):
        for directory, _, filename in os.walk(self.path + '\AttendanceSheet'):
            self.directory.append(directory)
            if filename is not None:
                for f in filename:
                    self.files.append(r'{}\{}'.format(directory, f))
        if not os.path.exists(self.directory[0] + '\Digits'):
            os.makedirs(os.path.join(self.directory[0], 'Digits'))
        self.directory[0] = self.directory[0] + r'\Digits\\'
        print(len(self.files))
        for i in range(0, len(self.files)):
            self.get_digits.get_digits(self.files[i], self.directory[0])
