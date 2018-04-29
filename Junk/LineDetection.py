import cv2
import numpy as np

img = cv2.imread('test.jpg')
img = img[:, 10:img.shape[1] - 10]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
minLineLength = img.shape[1] - 300
lines = cv2.HoughLinesP(image=edges, rho=0.001, theta=np.pi / 180, threshold=100, lines=np.array([]),
                        minLineLength=10, maxLineGap=5)
a, b, c = lines.shape
for i in range(a):
    cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
cv2.imwrite('result.png', img)
