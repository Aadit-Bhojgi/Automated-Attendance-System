import cv2 as cv


class RowMarking:
    def __init__(self, image, path):
        self.path = path
        self.image = image

    def rows(self):
        img = cv.imread(self.image)
        gray = cv.cvtColor(img, 6)
        thresh = cv.threshold(gray, thresh=200, maxval=255, type=cv.THRESH_BINARY_INV)[1]
        # Find contours on the threshold image
        contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[1]
        for c in contours:
            perimeter = cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, 0.04 * perimeter, True)
            if len(approx) == 4:
                (x, y, w, h) = cv.boundingRect(approx)
                ar = w / float(h)
                # To get only rectangles of desired AREA
                if ar >= 2:
                    if w < 130 and h < 70 and x < 60:
                        cv.line(img, (0, y), (img.shape[0], y), (0, 0, 255), 2)
        image = self.path + '\RowsMarked.jpg'
        cv.imwrite(image, img)
        return image


if __name__ == "__main__":
    RowMarking = RowMarking('result.jpg', '.')
    RowMarking.rows()
