from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from experiment.factories import ExperimentFactory


class Command(BaseCommand):
    help = "Populate the database with fake data."

    def handle(self, *args, **options):
        self.stdout.write("Generating fake data...")
        admin = User.objects.get(is_superuser=True)
        ExperimentFactory.create_batch(size=5, manager=admin)
        ExperimentFactory.create_batch(size=5)
        self.stdout.write("...finished")

