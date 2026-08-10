from datetime import date, time

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from experiment.models import Experiment, Registration, Session


class EmailTest(TestCase):
    name = 'experiment_name'

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(
            username='email-manager', password='password', email='manager@example.com'
        )
        cls.experiment = Experiment.objects.create(
            manager=user,
            name=cls.name,
            title='Experiment',
            email='researcher@example.com',
            phone='12345678',
        )
        cls.session = Session.objects.create(
            experiment=cls.experiment,
            date=date(2030, 1, 1),
            time=time(12, 0),
            place='Lab',
            max_subjects=2,
        )

    def test_send_email(self):
        mail.outbox.clear()
        registration = Registration.objects.create(
            session=self.session,
            first_name='Ada',
            last_name='Lovelace',
            phone='12345678',
            email='ada@example.com',
        )
        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject, f'{self.name}: Please confirm your email')
        self.assertEqual(mail.outbox[0].to[0], registration.email)
