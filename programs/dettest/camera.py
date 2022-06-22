# Librerías del modulo.
from cv2 import VideoCapture

# Clase para controlar una camara del sistema con la ayuda de la biblioteca de OpenCV.
class Camera:

    # Constantes que simbolizan el ancho y alto de la camara.
    __CAM_WIDTH = 3
    __CAM_HEIGHT = 4

    # Constructor que recive la cámara y la resolución de la imagen.
    def __init__(self, idCamera = 0, rWidth = 1280, rHeight = 720):

        # Manejador de la camára de video.
        self.__camera = VideoCapture(idCamera)

        # Resolución de la imagen.
        self.__resWidth = rWidth #   1280 ; 800 ; 640 
        self.__resHeight = rHeight #  720 ; 600 ; 480 

        # Se establece la resolución de la imagen.
        self.__camera.set(self.__CAM_WIDTH, self.__resWidth)
        self.__camera.set(self.__CAM_HEIGHT, self.__resHeight)

    # Realiza una captura.
    def takePicture(self):
        return self.__camera.read()

    # Comprueba si la camara esta activa.
    def isWorking(self):
        return self.__camera.isOpened()

    # Desactiva la cámara.
    def deactivate(self):
        self.__camera.release()

    # Establece el ancho de la imagen.
    def setWidth(self, rWidth):
        self.__resWidth = rWidth
        self.__camera.set(self.__CAM_WIDTH, self.__resWidth)

    # Establece el alto de la imagen.
    def setHeight(self, rHeight):
        self.__resHeight = rHeight
        self.__camera.set(self.__CAM_HEIGHT, self.__resHeight)

    # Obtiene el ancho de la imagen.
    def getWidth(self):
        return self.__resWidth

    # Obtiene el alto de la imagen.
    def getHeight(self):
        return self.__resHeight