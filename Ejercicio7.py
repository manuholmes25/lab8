import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

MOTOR_PIN = 18  # Puede ser cualquier pin PWM, como 18 (hardware PWM)

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

pwm_motor = GPIO.PWM(MOTOR_PIN, 1000)
pwm_motor.start(0)  # Empezamos con el motor apagado

def set_motor_speed(duty_cycle):
    pwm_motor.ChangeDutyCycle(duty_cycle)

cap = cv2.VideoCapture(0)  # 0 es la cámara por defecto (puede ser 1 si tienes varias)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo capturar la imagen.")
            break

    
        frame = cv2.resize(frame, (320, 240))

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Verde
        lower_green = np.array([40, 50, 50])
        upper_green = np.array([80, 255, 255])

        # Amarillo
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([35, 255, 255])

        # Rojo (dos rangos por el círculo HSV)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        # Crear máscaras para cada color
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)

        # Calcular la cantidad de píxeles detectados para cada color
        green_area = np.sum(mask_green) / 255
        yellow_area = np.sum(mask_yellow) / 255
        red_area = np.sum(mask_red) / 255

        max_area = max(green_area, yellow_area, red_area)

        if max_area == green_area and green_area > 50:
            print("Verde detectado → Motor al 100%")
            set_motor_speed(100)

        elif max_area == yellow_area and yellow_area > 50:
            print("Amarillo detectado → Motor al 25%")
            set_motor_speed(25)

        elif max_area == red_area and red_area > 50:
            print("Rojo detectado → Motor apagado")
            set_motor_speed(0)

        else:
            print("No se detecta ningún LED encendido.")
            set_motor_speed(0)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Interrumpido por el usuario.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    pwm_motor.stop()
    GPIO.cleanup()
