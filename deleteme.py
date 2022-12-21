# import os
# from azure.keyvault.secrets import SecretClient
# from azure.identity import DefaultAzureCredential

# keyVaultName = os.environ["KEY_VAULT_NAME"]
# KVUri = f"https://{keyVaultName}.vault.azure.net"

# credential = DefaultAzureCredential()
# client = SecretClient(vault_url=KVUri, credential=credential)

# secretName = input("Input a name for your secret > ")
# secretValue = input("Input a value for your secret > ")

# print(
#     f"Creating a secret in {keyVaultName} called '{secretName}' with the value '{secretValue}' ...")

# client.set_secret(secretName, secretValue)

# print(" done.")

# print(f"Retrieving your secret from {keyVaultName}.")

# retrieved_secret = client.get_secret(secretName)

# print(f"Your secret is '{retrieved_secret.value}'.")
# print(f"Deleting your secret from {keyVaultName} ...")

# poller = client.begin_delete_secret(secretName)
# deleted_secret = poller.result()

# print(" done.")
from .basesettings import *
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from urllib.parse import urlparse
from django.utils.encoding import force_str
import django
import os
from dotenv import load_dotenv

load_dotenv()

KEY_VAULT_NAME = os.getenv('KEY_VAULT_NAMES')
print(KEY_VAULT_NAME)


django.utils.encoding.force_text = force_str
load_dotenv()

DEBUG = os.getenv('DEBUG')
SECRET_KEY = (str, os.getenv("SECRET_KEY"))

if os.getenv('URL'):
    ALLOWED_HOSTS = [urlparse(os.getenv('URL')).netloc]
    CSRF_TRUSTED_ORIGINS = [os.getenv('URL')]
else:
    ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {'sslmode': os.getenv('DB_SSL_MODE')}
    }
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '/static/'),
]
AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_LOCATION = os.getenv('AZURE_LOCATION')
AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')

STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

STATICFILES_STORAGE = os.getenv('STATICFILES_STORAGE')
DEFAULT_FILE_STORAGE = os.getenv('DEFAULT_FILE_STORAGE')
