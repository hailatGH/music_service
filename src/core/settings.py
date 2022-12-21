import os
import django
from django.utils.encoding import force_str
from urllib.parse import urlparse
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from .basesettings import *

django.utils.encoding.force_text = force_str
load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = (str, os.getenv("SECRET_KEY"))
URL = os.getenv('URL')

if URL:
    ALLOWED_HOSTS = [urlparse(URL).netloc]
    CSRF_TRUSTED_ORIGINS = [URL]
else:
    ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = [
#     "music-service.calmgrass-743c6f7f.francecentral.azurecontainerapps.io"]
# CSRF_TRUSTED_ORIGINS = [
#     'https://music-service.calmgrass-743c6f7f.francecentral.azurecontainerapps.io/']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {'sslmode': 'disable'}
    }
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '/static/'),
]
AZURE_ACCOUNT_NAME = 'zemastroragev100'
AZURE_ACCOUNT_KEY = 'AFsY2hZVbyYBKisEkRL+toNNJ7yBOzoJ/cruOxurFHnU84vE+Cmloq9S2ZkCxYaxrM5QemPsUiX5+ASt4WEg8w=='
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_LOCATION = 'zemacontainer'
AZURE_CONTAINER = 'zemacontainer'

STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
DEFAULT_FILE_STORAGE = 'core.custom_storage.AzureMediaStorage'
