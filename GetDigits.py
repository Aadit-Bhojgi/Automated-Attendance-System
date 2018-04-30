import cv2


class GetDigits:
    def __init__(self):
        self.BLACK_THRESHOLD = 200
        self.MIN_SIZE = 40
        self.MAX_SIZE = 300
        self.THIN_THRESHOLD = max(10, self.MIN_SIZE)
        self.PADDING = 6
        self.idx = 1

    @staticmethod
    # Sort Contours on the basis of their x-axis coordinates in ascending order
    def sort_contours(contours):
        # construct the list of bounding boxes and sort them from left to right
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        (contours, bounding_boxes) = zip(*sorted(zip(contours, bounding_boxes), key=lambda b: b[1][0], reverse=False))
        # return the list of sorted contours
        return contours

    def get_digits(self, image, directory):
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Don't use magic numbers
        thresh = cv2.threshold(gray, thresh=self.BLACK_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
        # Find the contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 3)[1]
        # Grab only the innermost child components
        sorted_contours = self.sort_contours(contours)
        # For each contour, find the bounding rectangle and extract it
        for contour in sorted_contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = img[(y + self.PADDING):(y + h - self.PADDING), (x + self.PADDING):(x + w - self.PADDING)]
            # Skip thin contours (vertical and horizontal lines)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            if len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)
                if (ar >= 0.7) and (ar <= 0.99999999999999999):
                    if h < self.THIN_THRESHOLD or w < self.THIN_THRESHOLD:
                        continue
                    if h > 300 and w > 300:
                        continue
                    # discard areas that are too small
                    if h < 45 or w < 40:
                        continue
                    cv2.imwrite('{}-{}.png'.format(directory, self.idx), roi)
                    self.idx += 1
        self.idx = 1


if __name__ == '__main__':
    GetDigits = GetDigits()
    GetDigits.get_digits('check.png', r'C:\Users\Aadit bhojgi\Desktop\Python\tf')
