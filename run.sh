#!/bin/bash

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
