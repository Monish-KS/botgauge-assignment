import os
import sys
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.database')

if __name__ == '__main__':
    django.setup()
    execute_from_command_line(sys.argv)
