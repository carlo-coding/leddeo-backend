#!/bin/bash

# Remove all images
if [ -z "$(docker images -q)" ]; then
  echo "No hay imágenes que eliminar"
else
  sudo docker rmi $(docker images -q)
  echo "Todas las imágenes han sido eliminadas"
fi

# Build a new image
docker build -t production-image:latest .

# Stop and remove all running containers
if [ -z "$(docker ps -a -q)" ]; then
  echo "No hay contenedores que detener"
else
  sudo docker stop $(docker ps -a -q)
  sudo docker rm $(docker ps -a -q)
  echo "Todos los contenedores han sido detenidos y eliminados"
fi