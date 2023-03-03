import os
import sys

from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

paths = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'apps'),
]

for index, path in enumerate(paths):
    if path not in sys.path:
        sys.path.insert(index, path)

application = get_wsgi_application()
