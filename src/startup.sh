#!/bin/bash

source ../venv/bin/activate
python manage.py makemigrations player
python manage.py migrate --run-syncdb