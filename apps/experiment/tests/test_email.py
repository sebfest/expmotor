from django.core import mail
from django.test import TestCase

from experiment.factories import ExperimentFactory, SessionFactory, RegistrationFactory
from experiment.models import Session

class EmailTest(TestCase):
    name = 'experiment_name'

    @classmethod
    def setUpTestData(cls):
        experiment = ExperimentFactory(name=cls.name, session=None)
        SessionFactory(experiment=experiment, registrations=None)
        print("setUpTestData: Run once to set up non-modified data for all class methods.")

    def test_send_email(self):
        session = Session.objects.get(experiment__name=self.name)
        self.assertEqual(len(mail.outbox), 0)
        registration = RegistrationFactory(session=session)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        print(email)
        self.assertEqual(mail.outbox[0].subject, f'{self.name}: Please confirm your email')
        self.assertEqual(mail.outbox[0].to[0], registration.email)