import os
import django
from django.conf import settings
from django.db import connections
from dotenv import load_dotenv

load_dotenv()

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME', 'botgauge_db'),
                'USER': os.getenv('DB_USER', 'botgauge_user'),
                'PASSWORD': os.getenv('DB_PASSWORD', 'botgauge_pass'),
                'HOST': os.getenv('DB_HOST', 'localhost'),
                'PORT': os.getenv('DB_PORT', '5432'),
            }
        },
        INSTALLED_APPS=[
            'api',
        ],
        USE_TZ=False,
    )
    django.setup()

def get_db_connection():
    return connections['default']
