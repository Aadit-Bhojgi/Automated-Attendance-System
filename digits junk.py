import cv2


class GetDigits:
    def __init__(self):
        self.BLACK_THRESHOLD = 200
        self.MIN_SIZE = 40
        self.MAX_SIZE = 300
        self.THIN_THRESHOLD = max(10, self.MIN_SIZE)
        self.PADDING = 2
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
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions
        # Grab only the innermost child components
        inner_contours = [c[0] for c in zip(contours, hierarchy) if c[1][3] > 0]
        sorted_contours = self.sort_contours(inner_contours)
        # For each contour, find the bounding rectangle and extract it
        for contour in sorted_contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = img[(y + self.PADDING):(y + h - self.PADDING), (x + self.PADDING):(x + w - self.PADDING)]
            # Skip thin contours (vertical and horizontal lines)
            # if (h < self.THIN_THRESHOLD) or (w < self.THIN_THRESHOLD):
            #     continue
            # if (h > self.MAX_SIZE) and (w > self.MAX_SIZE):
            #     continue
            if h < self.THIN_THRESHOLD or w < self.THIN_THRESHOLD:
                continue
            if h > 300 and w > 300:
                continue
            # discard areas that are too small
            if h < 40 or w < 40:
                continue
            if h < 105 and w < 105:
                cv2.imwrite('{}-{}.png'.format(directory, self.idx), roi)
                self.idx += 1
        self.idx = 1


if __name__ == '__main__':
    GetDigits = GetDigits()
    GetDigits.get_digits('check.png', r'C:\Users\Aadit bhojgi\Desktop\Python\tf')
