import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.local')

import django

django.setup()


from experiment.models import Experiment
from experiment.factories import ExperimentFactory, SessionFactory
from django.contrib.auth.models import User


def create() -> None:
    """Create dummy participants"""
    print("Starting blog population script...")

    ExperimentFactory.create_batch(size=5)

    for instance in Experiment.objects.all():
        print(instance)
    print("...population finished")


def delete() -> None:
    """Delete all dummy posts and associated authors."""
    print("Deleting")
    Experiment.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
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
