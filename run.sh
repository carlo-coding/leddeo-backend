#!/bin/bash
LOCAL_FONT_DIR="/usr/share/fonts"
# Define la lista de fuentes deseadas
DESIRED_FONTS=(
  "Anton"
  "Open Sans"
  "Roboto"
  "Lato"
  "Oswald"
  "Slabo 27px"
  "Montserrat"
  "Raleway"
  "Poppins"
  "Oxygen"
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
  "Phudu"
  "Noto Sans"
  "Rubik"
  "Quicksand"
  "Barlow"
  "Dosis"
  "Bitter"
  "Cabin"
  "Prompt"
  "Abel"
  "Exo 2"
  "Varela Round"
  "Asap"
  "Assistant"
  "Abril Fatface"
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

### Save the downloaded fonts in image magic file
file_path="/etc/ImageMagick-6/type-ghostscript.xml"
echo '<?xml version="1.0" encoding="UTF-8"?>' > $file_path
echo '<!DOCTYPE typemap [' >> $file_path
echo '  <!ELEMENT typemap (type)+>' >> $file_path
echo '  <!ATTLIST typemap xmlns CDATA #FIXED "">' >> $file_path
echo '  <!ELEMENT type EMPTY>' >> $file_path
echo '  <!ATTLIST type xmlns CDATA #FIXED "" encoding NMTOKEN #IMPLIED' >> $file_path
echo '    family CDATA #REQUIRED format NMTOKEN #REQUIRED foundry NMTOKEN #REQUIRED' >> $file_path
echo '    fullname CDATA #REQUIRED glyphs CDATA #REQUIRED metrics CDATA #REQUIRED' >> $file_path
echo '    name NMTOKEN #REQUIRED stretch NMTOKEN #REQUIRED style NMTOKEN #REQUIRED' >> $file_path
echo '    version CDATA #IMPLIED weight CDATA #REQUIRED>' >> $file_path
echo ']>' >> $file_path
echo '<typemap>' >> $file_path
for font in $(ls /usr/share/fonts | grep .ttf | awk '{print substr($1, 1, length($1)-4)}')
do
  name=$font
  glyphs="/usr/share/fonts/$font.ttf"
  echo "<type format='ttf' name='$name' glyphs='$glyphs'/>"
  echo "<type format='ttf' name='$name' glyphs='$glyphs'/>" >> $file_path
done
echo '</typemap>' >> $file_path


### Run django commands to start server
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
