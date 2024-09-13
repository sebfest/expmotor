import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent

paths = [
    BASE_DIR,
    BASE_DIR / 'apps',
]

for index, path in enumerate(paths):
    if str(path) not in sys.path:
        sys.path.insert(index, str(path))

application = get_wsgi_application()