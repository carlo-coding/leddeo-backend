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

# Run django commands to start server
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(is_superuser=True).exists())" | grep -q "True"
if [ "$?" -ne 1 ]; then
  echo "A super user already exists"
else
  echo "Creating a super user"
  python manage.py createsuperuser --noinput
fi
python manage.py runserver 0.0.0.0:8000
