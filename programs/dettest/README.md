# DETTEST

Programa para probar el desempeño de modelos de CNN creados para la detección de objetos en imágenes.

Para ejecutar el programa:

    1. Instalar el script 'install.sh' lanzándolo en una shell de bash como: $ sudo bash install.sh
    
    2. Desde el mismo shell de bash, lanzar la GUI de la aplicación mediante: $ python3 view.py
        
        * Si se desea utilizar el programa directamente desde la shell de bash sin GUI, lanzar:
        $ python3 <pathToModelFolder> <pathToLabelMapFile> <detectionThreshold> <maskThreshold>
