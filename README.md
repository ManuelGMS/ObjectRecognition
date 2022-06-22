# ObjectRecognition
Trabajo de Fin de Máster en Ingeniería Informática.

El presente repositorio contiene el proyecto creado para la parte técnica del Trabajo de Fin de Máster en Ingeniería Informática: *Application of deep learning techniques for object recognition in images*. Una plataforma para simplificar y facilitar el conjunto de actividades a realizar para la puesta a punto, configuración y evaluación de modelos de detección de objetos. Esta se ha desarrollado con el lenguaje de proramación *Python3*, y el *framework* proporcionado por la *TensorFlow Object Detection API*, sobre los servicios *Google Colaboratory*, *Google Cloud Storage*, y *Google Drive*.

## Programas:

1. *CDSGnenerator*: permite evaluar y construir automáticamente *datasets* de imágenes con los que entrenar y validar detectores de objetos. 

2. *Dettool*: sirve para realizar el entrenamiento y la validación de un detector de objetos.

3. *Dettest*: es un programa portable para analizar el verdadero desempeño de un detector de objetos en lo que respecta a su capacidad de clasificación, localización, y generación de máscaras.

## Consideraciones:

* No es necesario realizar una instalación para poder utilizar la plataforma aquí desarrollada, solo posicionar la carpeta del proyecto en la raíz de su *Google Drive* y ejecutar los *Notebooks* con *Google Chrome*. Sin embargo, sí hay que realizar ciertas configuraciones para utilizar el programa *Dettool*, ya que este recurre a un bucket personal de *Google Cloud Storage*, por lo que es preciso cambiar dicho *bucket* por el suyo. Para ello se deben seguir estos pasos:

  1. Crear un *bucket* propio en *Google Cloud Storage* agregando al servidor de TPU vinculado al Notebook los permisos: lector de buckets heredados de almacenamiento, propietario de objetos heredados de almacenamiento, administrador de almacenamiento, propietario de buckets heredados de almacenamiento, y lector de objetos heredados del almacenamiento.

  2. Obtener para el bucket recién creado en *Google Cloud Storage* el fichero JSON para el acceso autentificado a este *bucket*. Para esto, debe acceder a *Cuentas de Servicio* en *IAM y Administración*, una vez allí, seleccione el nombre de su bucket y seleccione la pestaña *Claves*, y dentro de ella, en el desplegable *Agregar Clave* seleccionar *Crear Clave Nueva*, esto abrirá un cuadro de diálogo de donde se puede descargar el fichero JSON con el permiso de acceso. El fichero obtenido debe reemplazar a auth.json en la ruta *ObjectRecognition\exfiles* dentro del proyecto de *ObjectRecognition*.
        
  3. Configurar el *Notebook Dettool* de la siguiente manera: en la celda con el nombre *Autorización para el acceso a un bucket de Google Cloud Storage*, cambiar el valor de la variable *bucketName* al nombre de su *bucket*.

* La plataforma se ha desarrollado con la versión de *Google Colab Plus* debido a las limitaciones del hardware de la versión gratuita de *Colab*, y aunque puede utilizarse con esta, es posible que disminuya muy notablemente la capacidad para realizar el entrenamiento y la validación de los detectores.
