import cv2

cap = cv2.VideoCapture(0)  

fgbg = cv2.createBackgroundSubtractorMOG2()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        fgmask = fgbg.apply(frame)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                motion_detected = True
                break

        if motion_detected:
            print("Movimiento detectado!")
        else:
            print("Sin movimiento.")
        cv2.imshow('Video en vivo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    cap.release()
    cv2.destroyAllWindows()
