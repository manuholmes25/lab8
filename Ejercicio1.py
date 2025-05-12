import numpy as np
import cv2

kernel = np.ones((5, 5), np.uint8)

def Crop(img, start_row, end_row, start_col, end_col):
    return img[start_row:end_row, start_col:end_col]

def redf_img(img, alto, ancho):
    up_points = (ancho, alto)
    resized = cv2.resize(img, up_points)
    return resized

def cortar_h(img):
    h, w = img.shape[:2]
    mid_h = h // 2
    img_top = Crop(img, 0, mid_h, 0, w)
    img_bottom = Crop(img, mid_h, h, 0, w)
    return img_top, img_bottom

def cuadrantes(img):
    h, w = img.shape[:2]
    mid_h, mid_w = h // 2, w // 2
    q1 = Crop(img, 0, mid_h, 0, mid_w)
    q2 = Crop(img, 0, mid_h, mid_w, w)
    q3 = Crop(img, mid_h, h, 0, mid_w)
    q4 = Crop(img, mid_h, h, mid_w, w)
    return q1, q2, q3, q4

def edge(img, fgbg):
    fgmask = fgbg.apply(img)
    thresh = cv2.adaptiveThreshold(fgmask, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 17, 19)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(gray, contours, -1, (0, 255, 0), 1) 
    cv2.imshow('Contornos', gray)

cap = cv2.VideoCapture('/home/embebidos2/lab8/ball.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No hay video")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = redf_img(gray, 400, 600)

    img_top, img_bottom = cortar_h(resized)
    q1, q2, q3, q4 = cuadrantes(resized)
    edge(resized, fgbg)

    # Mostrar imágenes
    cv2.imshow('Redimensionado', resized)
    cv2.imshow("Mitad Superior", img_top)
    cv2.imshow("Mitad Inferior", img_bottom)
    cv2.imshow("Cuadrante 1", q1)
    cv2.imshow("Cuadrante 2", q2)
    cv2.imshow("Cuadrante 3", q3)
    cv2.imshow("Cuadrante 4", q4)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
