from os import environ

# TensorFlow LOG's a nivel de ERROR.
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from sys import argv
from numpy import int16
from camera import Camera
from tkinter import messagebox
from object_detection.utils.ops import reframe_box_masks_to_image_masks
from tensorflow import cast, uint8, saved_model, expand_dims, convert_to_tensor
from cv2 import imshow, waitKey, destroyWindow, getWindowProperty, WND_PROP_VISIBLE
from object_detection.utils import label_map_util as lmu, visualization_utils as vu

# Función que realiza la detección de objetos.
def objectDetection(pathToModelFoder, pathToLabelMapFile, detectionThreshold, maskThreshold):

    # Variable para controlar si se producen errores.
    error = False

    try:
        
        # Carga un modelo de CNN con sus pesos.
        model = saved_model.load(pathToModelFoder)
        
        try:
        
            # Índice de correspondencias: {'id': <IdClass> , 'name': <ClassName>}
            categoryIndex = lmu.create_category_index_from_labelmap(pathToLabelMapFile)

            try:
                
                # Comprueba que el umbral de confianza de las detecciones sea un número real.
                detectionThreshold = float(detectionThreshold)

                try:
                
                    # Comprueba de que el umbral de confianza de las máscaras de bits sea un número real.
                    maskThreshold = float(maskThreshold)

                    # Se comprueba que el umbral de confianza de las detecciones esté en el rango correcto.
                    if not(detectionThreshold >= 0.0 and detectionThreshold <= 1.0):
                        error = True
                        messagebox.showerror(message="Introduce a valid number for classification threshold in the range [0.0-1.0].", title='Error')

                    # Se comprueba que el umbral de confianza de las máscaras de bits esté en el rango correcto.
                    elif not(maskThreshold >= 0.0 and maskThreshold <= 1.0):
                        error = True
                        messagebox.showerror(message="Introduce a valid number for mask threshold in the range [0.0-1.0].", title='Error')
                
                except Exception:
                    error = True
                    messagebox.showerror(message="Introduce a valid number for mask threshold in the range [0.0-1.0].", title='Error')
                    
            except Exception:
                error = True
                messagebox.showerror(message="Introduce a valid number for classification threshold in the range [0.0-1.0].", title='Error')

        except Exception:
            error = True
            messagebox.showerror(message="Select a 'label_map' file.", title='Error')
            
    except Exception:
        error = True
        messagebox.showerror(message="Select a 'saved_model' folder.", title='Error')

    # Si no hay errores, se lanza la detección de objetos.
    if not error:

        # Inicialización de la cámara.
        camera = Camera()

        # Claves que albergan los datos necesarios para mostrar las detecciones.
        neededKeys = ['detection_boxes', 'detection_classes', 'detection_scores']

        # Se comprueba que la camára funcione.
        if camera.isWorking():

            # Se toma una imagen, un booleano nos dice si la camara está funcionanado.
            ok, image = camera.takePicture()

            # Mientras la cámara funcione con normalidad.
            while ok:
                
                """
                Convierte el la imagen como numpy array a un objeto de tipo tensor.
                El modelo espera un lote (batch) de imágenes, por lo que se añade una 
                nueva dimensión (axis) para que la entrada sea de (1, height, width, 3).
                """        
                tensor = convert_to_tensor(expand_dims(image, axis=0))

                # Pasa el batch de 1 imagen al modelo para obtener un diccionario de tensores.                
                dictOfTensors = model(tensor)

                # Número de detecciones en la imagen actual.
                detections = int(dictOfTensors['num_detections'])
                
                # Si el modelo hace uso de máscaras.
                if 'detection_masks' in dictOfTensors:
                    
                    # Se extraerá su información.
                    neededKeys.append('detection_masks')

                """
                Se le asigna a cada clave un tensor con los valores asociados al primer elemento de la 
                primera dimensión, es decir, los valores asociados a la única imagen que existe en la entrada.
                """
                dictOfTensors = {key: dictOfTensors[key][0, 0 : detections, ...].numpy() for key in neededKeys}
                
                # Si el modelo hace uso de máscaras.
                if 'detection_masks' in dictOfTensors:
                    
                    # Adapta las máscaras al tamaño de la imagen.
                    masks = reframe_box_masks_to_image_masks(
                        dictOfTensors['detection_masks'], # Máscaras de las detecciones.
                        dictOfTensors['detection_boxes'], # Bounding Boxes de las detecciones.
                        image.shape[0], image.shape[1] # Alto y ancho de la imagen capturada.
                    )
                    
                    """
                    Transforma los valores almacenados por los tensores en 1's, si superan el umbral de confianza
                    de la máscara, 0's en caso contrario, luego convierte los tensores en arrays de la librería numpy. 
                    """
                    dictOfTensors['detection_masks'] = cast(masks >= maskThreshold, uint8).numpy()

                # Dibuja en la imagen las detecciones.
                vu.visualize_boxes_and_labels_on_image_array(
                    image=image, # Imagen capturada.
                    boxes=dictOfTensors['detection_boxes'], # Bounding Boxes de las detecciones.
                    classes=dictOfTensors['detection_classes'].astype(int16), # Id's de las detecciones.
                    scores=dictOfTensors['detection_scores'], # Grado de confianza de cada detección.
                    instance_masks=dictOfTensors.get('detection_masks', None), # Máscaras de bits.
                    category_index=categoryIndex, # Índice de correspondencias.
                    use_normalized_coordinates=True, # Coordenadas de las detecciones normalizadas.
                    min_score_thresh=detectionThreshold # Umbral de confianza de las detecciones.
                )

                # Muestra la imagen en la ventana.
                imshow('Detecting', image)

                """
                Se espera 10 ms para comprobar si se pulsó la tecla ESC, 
                en cuyo caso el programa acaba, pero si no es detectada, 
                el programa pasa de largo y continúa la ejecución.
                """
                if waitKey(10) == 27: break

                # Si se pulsa el botón de cierre de la ventana, el programa acaba.
                if not getWindowProperty('Detecting', WND_PROP_VISIBLE): break

                # Se toma una imagen, un booleano nos dice si la camara está funcionanado.
                ok, image = camera.takePicture()

            # Desactiva la cámara de vídeo.
            camera.deactivate()

            # Destruye la ventana de la aplicación.
            destroyWindow('Detecting')

# Punto de entrada al programa.
def main():

    # Se comprueba que el número de argumentos sea el correcto.
    if len(argv) == 5:
        
        # Función que realiza la detección de objetos.
        objectDetection(argv[1], argv[2], argv[3], argv[4])
        
    else:
        
        # Se muestra un mensaje de aviso indicando los parámetros necesarios y su orden.
        messagebox.showwarning(message='Expected 4 argument: path to saved model folder, path to label map file, detection threshold, mask threshold.', title='Warning')

# Programa ejecutado como un script.
if __name__ == '__main__':
    main()