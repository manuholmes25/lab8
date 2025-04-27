import cv2
import numpy as np
import serial
from time import sleep

# Inicializar la cámara
cap = cv2.VideoCapture(0)

#Inicializar UART
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
sleep(2)
print("UART conectado en /dev/ttyACM0")

# Crear el objeto para substracción de fondo
fgbg = cv2.createBackgroundSubtractorMOG2()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionar para consistencia
        frame = cv2.resize(frame, (640, 480))

        fgmask = fgbg.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        # Buscar contornos en la máscara (lo que no es fondo)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_image = np.copy(frame)

        num_contornos = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:  
                num_contornos += 1
                cv2.drawContours(contours_image, [cnt], -1, (0, 255, 0), 2)

        if num_contornos == 1:
            print("Se detectó 1 objeto.")
            ser.write("1\n".encode('utf-8')) 
        elif num_contornos > 1:
            print("Muchos objetos.")
            ser.write("2\n".encode('utf-8'))

        # Mostrar los resultados
        cv2.imshow('Contornos detectados', contours_image) 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    cap.release()
    cv2.destroyAllWindows()
