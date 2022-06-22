# Instalación de paquetes del sistema.
apt-get -y install git
apt-get -y install python3
apt-get -y install python3-tk
apt-get -y install python3-pip
apt-get -y install protobuf-compiler

# Descarga de la TensorFlow Object Dection API.
git clone https://github.com/tensorflow/models.git

# Posicionamiento en el directorio "research".
cd models/research

# Compilación de los Protocol Buffers.
protoc object_detection/protos/*.proto --python_out=.

# Copia el instalador de la API en el directorio actual.
cp object_detection/packages/tf2/setup.py .

# Ejecuta el instalador.
python3 -m pip install .

# Vuelta al directorio original.
cd ../..

# Se eliminación de la carpeta descargada.
rm -rf models

# Instalación de paquetes Python.
yes | python3 -m pip uninstall opencv-python-headless
yes | python3 -m pip uninstall opencv-python
python3 -m pip install opencv-python
python3 -m pip install tensorflow