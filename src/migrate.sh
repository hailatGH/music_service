source ../venv/bin/activate
python manage.py makemigrations
python manage.py makemigrations music

python manage.py migrate
python manage.py migrate music

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@kinideas.com', 'playground')" | python manage.py shell