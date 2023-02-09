from django.core.management.base import BaseCommand, CommandError
from experiment.factories import ExperimentFactory


class Command(BaseCommand):
    help = "Populate the database with fake data."

    def handle(self, *args, **options):
        self.stdout.write("Generating fake data...")
        ExperimentFactory.create_batch(size=5)
        self.stdout.write("...finished")

