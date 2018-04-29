import cv2 as cv
import numpy as np
import os
import inspect


class RowMarking:
    def __init__(self, image, template):
        self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
        self.image = image
        self.template = template

    def rows(self):
        img_rgb = cv.imread(self.image)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(self.template, 0)
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv.line(img_rgb, (0, pt[1]), (img_rgb.shape[0], pt[1]), (0, 0, 255), 2)
        image = self.path + '\RowsMarked.jpg'
        cv.imwrite(image, img_rgb)
        return image


if __name__ == "__main__":
    RowMarking = RowMarking('ok.jpg', 'Template.jpg')
    RowMarking.rows()
