import copy
import cv2

BLACK_THRESHOLD = 200
THIN_THRESHOLD = 10
ANNOTATION_COLOUR = (0, 0, 255)

img = cv2.imread('0.png')
orig = copy.copy(img)
gray = cv2.cvtColor(img, 6)
thresh = cv2.threshold(gray, thresh=BLACK_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY_INV)[1]

# Find the contours
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


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
    # return the list of sorted contours and bounding boxes
    return cnts


sorted_contours = sort_contours(contours, hierarchy)

hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions
idx = 0
day = 1
# For each contour, find the bounding rectangle and extract it
for component in sorted_contours:
    currentContour = component
    x, y, w, h = cv2.boundingRect(currentContour)
    roi = img[y + 2:y + h - 2, x + 2:x + w - 2]
    # Skip thin contours (vertical and horizontal lines)
    if h < THIN_THRESHOLD or w < THIN_THRESHOLD:
        continue
    if h > 300 and w > 300:
        continue
    if h < 40 or w < 40:
        continue
    idx += 1
    if idx % 2 == 0:
        cv2.imwrite('Day{}.png'.format(day), roi)
        day += 1
