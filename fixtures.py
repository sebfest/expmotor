import os
import sys
from dotenv import load_dotenv

paths = [
    os.getcwd(),
    os.path.join(os.getcwd(), 'apps'),
]

for index, path in enumerate(paths):
    if path not in sys.path:
        sys.path.insert(index, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')


load_dotenv()


import django

django.setup()

from experiment.models import Experiment
from experiment.factories import ExperimentFactory
from django.contrib.auth.models import User


def create() -> None:
    """Create dummy registrations"""
    print("Starting production...")

    ExperimentFactory.create_batch(size=5)

    for instance in Experiment.objects.all():
        print(instance)
    print("...production finished")


def delete() -> None:
    """Delete all dummy registrations and associated managers."""
    print("Deleting")
    Experiment.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    
    folder = '../../messages/'
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))

    print("Success.")


def main() -> None:
    """Populate or delete database."""

    choices = {
        1: create,
        2: delete,
        3: quit,
    }
    menu = """
    
    1 = Create.
    2 = Delete.
    3 = Quit.
    
    """
    print(menu)
    while True:
        choice = int(input('Select an action: '))
        func = choices.get(choice)
        if func:
            func()
            print(menu)
        else:
            print(f'{choice} is not a valid option.')


if __name__ == '__main__':
    main()
