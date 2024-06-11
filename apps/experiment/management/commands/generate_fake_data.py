from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from experiment.factories import ExperimentFactory


class Command(BaseCommand):
    help = "Populate the database with fake data."

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, nargs='?', const=5, default=5,
                            help='Indicates the number of experiments to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']

        self.stdout.write(self.style.WARNING("Generating {} fake experiments...".format(total)))
        admin = User.objects.get(is_superuser=True)
        ExperimentFactory.create_batch(size=total, manager=admin)
        self.stdout.write(self.style.SUCCESS("...finished"))
