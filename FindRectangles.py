import copy
import cv2

BLACK_THRESHOLD = 200
THIN_THRESHOLD = 10
ANNOTATION_COLOUR = (0, 0, 255)
MIN_SIZE = 40
MAX_SIZE = 300

img = cv2.imread('Test7.jpg')
orig = copy.copy(img)
gray = cv2.cvtColor(img, 6)
thresh = cv2.threshold(gray, thresh=BLACK_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY_INV)[1]


# Sort Contours on the basis of their x-axis coordinates in ascending order
def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours
    return cnts


# Find contours on the thresholded image
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 3)[1]
# hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions
# Grab only the innermost child components
# inner_contours = [c[0] for c in zip(contours, hierarchy) if c[1][3] > 0]
sorted_contours = sort_contours(contours, method="top-to-bottom")
i=1
for cont in sorted_contours:
    x, y, w, h = cv2.boundingRect(cont)
    roi = img[(y + 6):(y + h - 6), (x + 6):(x + w - 6)]
    # Skip thin contours (vertical and horizontal lines)
    perimeter = cv2.arcLength(cont, True)
    approx = cv2.approxPolyDP(cont, 0.04 * perimeter, True)
    if len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        if ar >= 0.7 and ar <= 0.99999999999998999:
            if h < THIN_THRESHOLD or w < THIN_THRESHOLD:
                continue
            if h > 300 and w > 300:
                continue
            # discard areas that are too small
            if h < 45 or w < 40:
                continue
            print(i, ar, h, w)
            cv2.rectangle(img, (x, y), (x + w, y + h), ANNOTATION_COLOUR, 1)
            cv2.imwrite('{}.png'.format(i), roi)
            i += 1

cv2.imwrite("result.jpg", img)
print(i)