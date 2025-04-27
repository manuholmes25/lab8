import cv2
import os

class WebcamCapture:
    def __init__(self, capture_path):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: No se pudo abrir la cámara")
            exit()
        
        self.capture_path = capture_path
        self.cont = 1
        self.create_capture_directory()

    def create_capture_directory(self):
        if not os.path.exists(self.capture_path):
            os.makedirs(self.capture_path)

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: No se pudo leer el frame")
            return None
        return frame

    def save_grayscale_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        filename = f"{self.capture_path}/imagen{self.cont}.jpg"
        cv2.imwrite(filename, gray)
        print(f"Capturado el frame como: imagen{self.cont}.jpg")
        self.cont += 1
        return filename

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


class ImageProcessor:
    @staticmethod
    def display_image(title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyWindow(title)

    @staticmethod
    def rgb_to_grayscale(image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ImageProcessor.display_image("Escala de grises", gray_image)
        return gray_image

    @staticmethod
    def partition_image(image):
        alto, ancho = image.shape[:2]
        mitad_alto = alto // 2
        mitad_ancho = ancho // 2

        cuadrante1 = image[0:mitad_alto, 0:mitad_ancho]
        cuadrante2 = image[0:mitad_alto, mitad_ancho:ancho]
        cuadrante3 = image[mitad_alto:alto, 0:mitad_ancho]
        cuadrante4 = image[mitad_alto:alto, mitad_ancho:ancho]

        cuadrantes = [cuadrante1, cuadrante2, cuadrante3, cuadrante4]
        for i, cuadrante in enumerate(cuadrantes, 1):
            ImageProcessor.display_image(f'Cuadrante {i}', cuadrante)


class Menu:
    @staticmethod
    def show_image_menu(capture_path, max_images):
        print("Escoger imagen para volver a escala de grises y dividir:")
        for i in range(1, max_images):
            print(f"{i}. imagen{str(i)}.jpg")
        op = int(input("Escribe el numero de imagen:\n"))
        
        selected_image_path = f"{capture_path}/imagen{op}.jpg"
        if not os.path.exists(selected_image_path):
            print("Error: La imagen seleccionada no existe.")
            return None
        image = cv2.imread(selected_image_path)
        return image


def main():
    capture_path = "/home/embebidos2/lab8/Captures"
    webcam = WebcamCapture(capture_path)
    image_processor = ImageProcessor()

    while True:
        frame = webcam.capture_frame()
        if frame is None:
            break
        
        cv2.imshow('Webcam', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('e'):  # e=Exit
            break
        elif key == ord('f'):  # f=Capturar
            webcam.save_grayscale_frame(frame)

    webcam.release()

    img2 = Menu.show_image_menu(capture_path, webcam.cont)
    if img2 is not None:
        img3 = image_processor.rgb_to_grayscale(img2)
        image_processor.partition_image(img3)


if __name__ == "__main__":
    main()
