import csv


class CSV:
    def __init__(self):
        self.prediction = []
        self.CSV_Fields = []
        self.students = []
        self.attendance = []

    def organise_data(self, predicted_info, name_roll_no, date_length, no_of_days):
        self.attendance = []
        self.CSV_Fields = []
        self.students = name_roll_no
        self.prediction = predicted_info
        self.CSV_Fields.append('NAME')
        self.CSV_Fields.append('ROLL NUMBER')
        date = predicted_info[0:date_length[0]]
        year = predicted_info[date_length[0]:date_length[0] + 4]
        days = no_of_days[0]
        attendance = predicted_info[date_length[0] + 4::]
        for i in range(0, date_length[0], 4):
            self.CSV_Fields.append('{}{}/{}{}/{}{}{}{}'.format(date[i], date[i + 1], date[i + 2], date[i + 3], year[0],
                                                               year[1], year[2], year[3]))
        students_count = 0
        for i in range(0, len(attendance), days):
            dict_ = dict()
            dict_[self.CSV_Fields[0]] = self.students[students_count].split('(')[0]
            dict_[self.CSV_Fields[1]] = self.students[students_count].split('(')[1].strip(')')
            for j in range(0, days):
                if attendance[i + j] == 0:
                    dict_[self.CSV_Fields[2 + j]] = 'ABSENT'
                elif attendance[i + j] == 1:
                    dict_[self.CSV_Fields[2 + j]] = 'PRESENT'
            self.attendance.append(dict_)
            students_count += 1

    def write(self, filename):
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_Fields)
            writer.writeheader()
            writer.writerows(self.attendance)


if __name__ == '__main__':
    pass
