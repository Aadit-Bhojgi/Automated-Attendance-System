import copy

import cv2

BLACK_THRESHOLD = 200
THIN_THRESHOLD = 10
ANNOTATION_COLOUR = (0, 0, 255)

img = cv2.imread('new.jpg')
orig = copy.copy(img)
gray = cv2.cvtColor(img, 6)
thresh = cv2.threshold(gray, thresh=BLACK_THRESHOLD, maxval=255, type=cv2.THRESH_BINARY_INV)[1]

contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

for cont in contours:
    for c in contours:
        x1, y1, w1, h1 = cv2.boundingRect(c)
        if h1 == h_max:
            cont = c
            break
    x, y, w, h = cv2.boundingRect(cont)
    cv2.rectangle(img, (x, y), (x + w, y + h), ANNOTATION_COLOUR, 3)

cv2.imwrite("result.png", img)
