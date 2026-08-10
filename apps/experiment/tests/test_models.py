from datetime import date, time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from experiment.models import Experiment, Registration, Session


class ExperimentModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='manager', password='password', email='manager@example.com'
        )
        self.experiment = Experiment.objects.create(
            manager=self.user,
            name='attention-study',
            title='Attention study',
            email='researcher@example.com',
            phone='12345678',
        )

    def test_session_capacity_and_completion(self):
        session = Session.objects.create(
            experiment=self.experiment,
            date=date(2030, 1, 1),
            time=time(12, 0),
            place='Lab',
            max_subjects=2,
        )
        Registration.objects.create(
            session=session,
            first_name='Ada',
            last_name='Lovelace',
            phone='12345678',
            email='ada@example.com',
            is_active=True,
        )
        self.assertEqual(session.active_registrations, 1)
        self.assertEqual(session.complete, 50.0)
        self.assertFalse(session.is_full)

    def test_duplicate_registration_is_rejected_case_insensitively(self):
        session = Session.objects.create(
            experiment=self.experiment,
            date=date(2030, 1, 1),
            time=time(12, 0),
            place='Lab',
            max_subjects=2,
        )
        Registration.objects.create(
            session=session,
            first_name='Ada',
            last_name='Lovelace',
            phone='12345678',
            email='ada@example.com',
        )
        duplicate = Registration(
            session=session,
            first_name='Grace',
            last_name='Hopper',
            phone='12345678',
            email='ADA@EXAMPLE.COM',
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
