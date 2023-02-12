#!/bin/bash
LOCAL_FONT_DIR="/usr/share/fonts"
# Define la lista de fuentes deseadas
DESIRED_FONTS=(
  "Open Sans"
  "Roboto"
  "Lato"
  "Oswald"
  "Slabo 27px"
  "Montserrat"
  "Raleway"
  "Poppins"
  "Nunito"
  "Bakbak One"
  "Comfortaa"
  "Caveat"
  "Comic Neue"
  "Courier Prime"
  "Lexend"
  "Lobster"
  "Lora"
  "Merriweather"
  "Spectral"
  "Pacifico"
  "Zeyada"
  "Babylonica"
  "Mukta"
)
# Recorre la lista de fuentes deseadas
for font in "${DESIRED_FONTS[@]}"; do
  # Construye la URL de descarga de la fuente
  font_url="https://fonts.google.com/download?family=$(echo $font | tr ' ' '+')"
  # Descarga la fuente
  wget -P $LOCAL_FONT_DIR $font_url
  # Descomprime el archivo zip
  unzip -o -d $LOCAL_FONT_DIR "$LOCAL_FONT_DIR/$(basename $font_url)"
  # Elimina el archivo zip
  rm "$LOCAL_FONT_DIR/$(basename $font_url)"
done

echo "Las fuentes deseadas se descargaron correctamente"

# Stop and remove all running containers
if [ -z "$(docker ps -a -q)" ]; then
  echo "No hay contenedores que detener"
else
  sudo docker stop $(docker ps -a -q)
  sudo docker rm $(docker ps -a -q)
  echo "Todos los contenedores han sido detenidos y eliminados"
fi

# Remove all images
if [ -z "$(docker images -q)" ]; then
  echo "No hay imágenes que eliminar"
else
  sudo docker rmi $(docker images -q)
  echo "Todas las imágenes han sido eliminadas"
fi

# Build a new image
docker build -t production-image:latest .