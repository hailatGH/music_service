#!/bin/bash

source ../venv/bin/activate
python manage.py makemigrations player
python manage.py migrate --run-syncdb
python manage.py runserver 127.0.0.1:8000