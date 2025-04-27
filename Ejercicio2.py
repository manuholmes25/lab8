import cv2
import numpy as np

class Filter:
    def apply(self, frame):
        return frame

class GrayscaleFilter(Filter):
    def apply(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

class EdgeFilter(Filter):
    def apply(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 50, 150)

class SepiaFilter(Filter):
    def apply(self, frame):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)

class CameraApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.filter = Filter()

    def run(self):
        print("Presiona 1 = Gris, 2 = Bordes, 3 = Sepia, q = Salir")

        while True:
            _, frame = self.cap.read()
            filtered = self.filter.apply(frame)

            if len(filtered.shape) == 2:  
                cv2.imshow("Camara con filtro", filtered)
            else:
                cv2.imshow("Camara con filtro", filtered)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('1'):
                self.filter = GrayscaleFilter()
            elif key == ord('2'):
                self.filter = EdgeFilter()
            elif key == ord('3'):
                self.filter = SepiaFilter()
            elif key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = CameraApp()
    app.run()
