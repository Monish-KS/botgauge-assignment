import os
from django.db import connections
from dotenv import load_dotenv

load_dotenv(override=True)

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'botgauge_db'),
        'USER': os.getenv('DB_USER', 'botgauge_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'botgauge_pass'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
INSTALLED_APPS = ['api']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = False

def get_db_connection():
    return connections['default']
