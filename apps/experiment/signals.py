from typing import Type

from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from experiment.models import Experiment, Participant
from experiment.tokens import account_activation_token


@receiver(post_save, sender=Experiment)
def send_new_experiment_notification_email(sender: Type[Experiment], instance: Experiment,
                                           created: bool, **kwargs) -> None:
    """Send confirmation email after successful creation."""
    if created:
        context_variables = {
            'exp_name': instance.name,
            'invitation_manager': instance.manager.get_username(),
            'login_url': instance.get_absolute_url()
        }
        email = EmailMessage(
            subject=f'[Expmotor] Experiment created ({instance.name})',
            body=render_to_string('experiment/experiment_created_confirmation.txt', context_variables),
            from_email="noreply@thomas.nhh.no",
            to=[instance.email],
            bcc=[],
        )
        email.send()


@receiver(post_save, sender=Participant)
def send_registration_notification_email(sender: Type[Participant], instance: Participant,
                                         created: bool, update_fields, **kwargs) -> None:
    """Send confirmation email after successful creation."""

    if created:
        template = Template(instance.session.experiment.confirmation_request)
        context_variables = {
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': account_activation_token.make_token(instance),
        }
        context = Context(context_variables)
        title = '[Expmotor] Please confirm your email'

    elif not created and 'confirmed_email' in update_fields:
        template = Template(instance.session.experiment.final_instructions)
        context_variables = {
            'session': instance.session,
            'manager': instance.session.experiment.manager,
        }
        context = Context(context_variables)
        title = '[Expmotor] Confirmation of experiment participation',

    else:
        return

    email = EmailMessage(
        subject=title,
        body=template.render(context),
        from_email="noreply@thomas.nhh.no",
        to=[instance.email],
        bcc=[],
    )
    email.send()
