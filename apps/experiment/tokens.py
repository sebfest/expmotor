import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import Participant


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: Participant, timestamp):
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.confirmed_email)
        )


account_activation_token = AccountActivationTokenGenerator()
