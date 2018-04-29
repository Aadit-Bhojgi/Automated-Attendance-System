import os
import cv2
import GetDigits


class RowSegregate:
    def __init__(self, image, names, strength, path):
        self.path = path
        self.image = image
        self.i = 1
        self.StudentsList = names
        self.RowCount = strength + 2
        self.row = ''
        self.directory = ''
        self.index = -1
        self.get_digits = GetDigits.GetDigits()

    def crop(self):
        img = cv2.imread(self.image, 0)
        ret, thresh = cv2.threshold(img, 127, 255, 0)
        _, contours, hierarchy = cv2.findContours(thresh, 2, 3)
        if not os.path.exists(self.path + '\\AttendanceSheet'):
            os.makedirs(self.path + '\\AttendanceSheet')
        for c in contours:
            if self.i == self.RowCount + 1:
                break
            else:
                x, y, w, h = cv2.boundingRect(c)
                if x + w == img.shape[1] and x == 0:
                    if self.i == self.RowCount:
                        self.directory = self.path + '\\AttendanceSheet\\.Year'
                        self.row = '{}.png'.format(self.directory)
                    elif self.i == self.RowCount - 1:
                        self.directory = self.path + '\\AttendanceSheet\\.Dates'
                        self.row = '{}.png'.format(self.directory)
                    else:
                        namespace = self.StudentsList[self.index - 1] + self.StudentsList[self.index]
                        self.directory = self.path + '\\AttendanceSheet\\{}'.format(namespace)
                        self.row = '{}.png'.format(self.directory)
                        self.index -= 2
                    cv2.imwrite(self.row, img[y:y + h, x:x + w])
                    self.get_digits.get_digits(self.row, self.directory)
                    os.remove(self.row)
                    self.i += 1


if __name__ == "__main__":
    pass
