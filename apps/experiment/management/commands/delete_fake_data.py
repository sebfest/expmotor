import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from experiment.models import Experiment


class Command(BaseCommand):
    help = "Delete test data."

    def handle(self, *args, **options):
        self.stdout.write("Deleting data...")
        Experiment.objects.all().delete()
        get_user_model().objects.filter(is_superuser=False).delete()
        self.stdout.write("...finished")

        message_folder = os.path.join(os.getcwd(), 'messages')
        if os.path.isdir(message_folder):
            for f in os.listdir(message_folder):
                os.remove(os.path.join(message_folder, f))
