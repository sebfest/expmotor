import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from experiment.models import Experiment


class Command(BaseCommand):
    help = "Delete test data."

    def handle(self, *args, **options):
        self.stdout.write("Deleting data...")
        Experiment.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write("...finished")

        message_folder = os.path.join(os.getcwd(), 'messages')
        for f in os.listdir(message_folder):
            os.remove(os.path.join(message_folder, f))

