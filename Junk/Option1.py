import copy
import cv2

BLACK_THRESHOLD = 200
THIN_THRESHOLD = 10
ANNOTATION_COLOUR = (0, 0, 255)

img = cv2.imread('Dates.png')
orig = copy.copy(img)
gray = cv2.cvtColor(img, 6)
thresh = cv2.threshold(gray, thresh=BLACK_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY_INV)[1]

# Find the contours
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

# SortedContours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0], reverse=True)
hierarchy = hierarchy[0]  # get the actual inner list of hierarchy descriptions
idx = 0
# For each contour, find the bounding rectangle and draw it
for component in zip(contours, hierarchy):
    currentContour = component[0]
    currentHierarchy = component[1]
    x, y, w, h = cv2.boundingRect(currentContour)
    roi = img[y+2:y + h-2, x+2:x + w-2]
    # Skip thin contours (vertical and horizontal lines)
    if h < THIN_THRESHOLD or w < THIN_THRESHOLD:
        continue
    if h > 300 and w > 300:
        continue
    if h < 40 or w < 40:
        continue
    if currentHierarchy[3] > 0:
        # these are the innermost child components
        idx += 1
        cv2.imwrite(str(idx) + '.png', roi)
