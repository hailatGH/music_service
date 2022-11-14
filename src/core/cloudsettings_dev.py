import io, os, environ, google.auth
from google.cloud import secretmanager
from urllib.parse import urlparse

from .basesettings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

env = environ.Env(
    SECRET_KEY=(str, os.getenv("SECRET_KEY")),
    DATABASE_URL=(str, os.getenv("DATABASE_URL")),
    GS_BUCKET_NAME=(str, os.getenv("GS_BUCKET_NAME")),
)

try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.getenv("PYTHON_ENV") == "dev":
    DEBUG = True

elif os.getenv("GOOGLE_CLOUD_PROJECT", None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.getenv("SETTINGS_NAME", "music_service_settings_dev")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )

    env.read_env(io.StringIO(payload))
else:
    raise Exception(
        "No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found."
    )

SECRET_KEY = env("SECRET_KEY")

MUSIC_SERVICE_URL = env("MUSIC_SERVICE_URL", default=None)

if MUSIC_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(MUSIC_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [MUSIC_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

DATABASES = {"default": env.db()}

if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "cloudsql-proxy"
    DATABASES["default"]["PORT"] = 5432

if "core" not in INSTALLED_APPS:
    INSTALLED_APPS += ["core"]

GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = []
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

# ELASTIC_HOST_KEY= f"https://elastic:OOPjLQHlFr2CPkO5FCD5YIzm@kinmusic.es.europe-west1.gcp.cloud.es.io:9243"
ELASTIC_HOST_KEY= f"https://elastic:iBDoYGCEeBHcjhtGPPo0rrI1@kin-music-search-577dcc.es.europe-west1.gcp.cloud.es.io:9243"

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': [ELASTIC_HOST_KEY]
    }
}