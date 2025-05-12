'''Detect the contours of an image using the functions “findContours()”
and “drawContours()”.'''

import cv2

def edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 17, 19)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = img.copy()
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 1)
    cv2.imshow('Contornos', img_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
img = cv2.imread('/home/embebidos2/lab8/img1.jpeg')
edge(img)
