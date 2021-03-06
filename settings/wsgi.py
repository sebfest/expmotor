import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, '.env'))

paths = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'apps'),
]

for index, path in enumerate(paths):
    if path not in sys.path:
        sys.path.insert(index, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'

application = get_wsgi_application()
