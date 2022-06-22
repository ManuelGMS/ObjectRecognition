from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Spinbox
from tkinter import filedialog
from tkinter import messagebox
from detection import objectDetection

# Ventana de la aplicación.
class Window(Tk):

    # Constructor de la clase.
    def __init__(self, *args, **kwargs):
        
        # Constructor de TKinter.
        Tk.__init__(self, *args, **kwargs)

        # Título de la ventana.
        self.title('Dettester')

        # Ventana no redimensionable.
        self.resizable(width=False, height=False)

        # El cierre de la ventana llama al destructor de la clase.
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        
        # Contenedor principal de los Widgets.
        self.__frame = Frame(self, bg='white')
        
        # Ruta a una carpeta 'saved_model'.
        self.__pathToModelFoder = ()

        # Ruta a un fichero de 'label_map'.
        self.__pathToLabelMapFile = ()

        # Función para seleccionar el directorio 'saved_model'.
        def __selectModel():
            # Cuadro de diálogo para seleccionar el directorio 'saved_model'.
            self.__pathToModelFoder = filedialog.askdirectory(mustexist=True)
        
        # Función para seleccionar el fichero 'label_map'.
        def __selectLabelMap():
            # Cuadro de diálogo para seleccional el fichero 'label_map'.
            self.__pathToLabelMapFile = filedialog.askopenfilename(filetypes=(('Text Protobuf', '*.pbtxt'), ))

        # Función para lanzar el reconocimiento de objetos.
        def __runObjectDetection():
            
            # Función que realiza la detección de objetos.
            objectDetection(self.__pathToModelFoder, self.__pathToLabelMapFile, __sbDetectionThreshold.get(), __sbMaskThreshold.get())
    
            # Tras cada prueba el usuario debe seleccionar: la carpeta 'saved_model' el fichero 'label_map' y el valor de los umbrales.
            self.__pathToModelFoder = ()
            self.__pathToLabelMapFile = ()
            __sbDetectionThreshold.delete(0, len(__sbDetectionThreshold.get()))
            __sbDetectionThreshold.insert(0, 'Detection Threshold')
            __sbMaskThreshold.delete(0, len(__sbMaskThreshold.get()))
            __sbMaskThreshold.insert(0, 'Mask Threshold')

        # Botón para seleccionar la carpeta 'saved_model'; definición, posicionamiento en el grid y reacción ante la tecla 'ENTER'.
        __btnSelectModel = Button(self.__frame, text='Saved Model Folder', font=('Arial Bold', 20), command=lambda : __selectModel())
        __btnSelectModel.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        __btnSelectModel.bind('<Return>', lambda unused : __selectModel())
        
        # Botón para seleccionar el fichero 'label_map'; definición, posicionamiento en el grid y reacción ante la tecla 'ENTER'.
        __btnSelectLabelMap = Button(self.__frame, text='Label Map File', font=('Arial Bold', 20), command=lambda : __selectLabelMap())
        __btnSelectLabelMap.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        __btnSelectLabelMap.bind('<Return>', lambda unused : __selectLabelMap())

        # Spinbox para seleccionar el umbral de confianza de las detecciones; definición, posicionamiento en el grid y texto informativo inicial.
        __sbDetectionThreshold = Spinbox(self.__frame, font=('Arial Bold', 20), from_=0.0, to=1.0, increment=0.01, justify='center')
        __sbDetectionThreshold.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        __sbDetectionThreshold.delete(0, len(__sbDetectionThreshold.get()))
        __sbDetectionThreshold.insert(0, 'Detection Threshold')

        # Spinbox para seleccionar el umbral de confianza de las máscaras de bits; definición, posicionamiento en el grid y texto informativo inicial.
        __sbMaskThreshold = Spinbox(self.__frame, font=('Arial Bold', 20), from_=0.0, to=1.0, increment=0.01, justify='center')
        __sbMaskThreshold.grid(row=3, column=0, padx=10, pady=5, sticky='ew')
        __sbMaskThreshold.delete(0, len(__sbMaskThreshold.get()))
        __sbMaskThreshold.insert(0, 'Mask Threshold')

        # Botón para iniciar el reconocimiento de objetos; definición, posicionamiento en el grid y reacción ante la tecla 'ENTER'.
        __btnGo = Button(self.__frame, text='Go', font=('Arial Bold', 20), command=lambda : __runObjectDetection())
        __btnGo.grid(row=4, column=0, padx=10, pady=5, sticky='ew')
        __btnGo.bind('<Return>', lambda unused : __runObjectDetection())

        # Añade el frame a la ventana y lo expande.
        self.__frame.pack(fill="both", expand = True)

# Punto de entrada al programa.
def main():
    # Ejecuta la ventana.
    Window().mainloop()

# Programa ejecutado como un script.
if __name__ == '__main__':
    main()