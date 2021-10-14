from typing import Type, FrozenSet, Optional

from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Experiment, Participant
from .tokens import account_activation_token


@receiver(post_save, sender=Experiment)
def send_new_experiment_notification_email(sender: Type[Experiment], instance: Experiment,
                                           created: bool, **kwargs) -> None:
    """Send confirmation email after successful experiment creation."""
    if created:
        context_dict = {
            'exp_name': instance.name,
            'invitation_manager': instance.manager.get_username(),
            'login_url': instance.get_absolute_url()
        }
        email = EmailMessage(
            subject=f'[Expmotor] Experiment created ({instance.name})',
            body=render_to_string('experiment/experiment_created_confirmation.txt', context_dict),
            from_email='thechoicelab@nhh.no',
            to=[instance.email],
        )
        email.send()


@receiver(post_save, sender=Participant)
def send_email_confirmation_request(sender: Type[Participant], instance: Participant,
                                    created: bool, update_fields: Optional[FrozenSet], **kwargs) -> None:
    """Send request to conform email after successful creation."""

    if created:
        template = Template(instance.session.experiment.confirmation_request)
        context_dict = {
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': account_activation_token.make_token(instance),
        }
        context = Context(context_dict)

        email = EmailMessage(
            subject='[Expmotor] Please confirm your email',
            body=template.render(context),
            from_email='thechoicelab@nhh.no',
            to=[instance.email],
        )
        email.send()


@receiver(post_save, sender=Participant)
def send_registration_info(sender: Type[Participant], instance: Participant,
                           created: bool, update_fields: Optional[FrozenSet], **kwargs) -> None:
    """Send email with registration_old info after email confirmation."""

    if not created and update_fields and 'confirmed_email' in update_fields:
        template = Template(instance.session.experiment.final_instructions)
        context_dict = {
            'session': instance.session,
            'manager': instance.session.experiment.manager,
        }
        context = Context(context_dict)

        email = EmailMessage(
            subject='[Expmotor] Confirmation of experiment participation',
            body=template.render(context),
            from_email='thechoicelab@nhh.no',
            to=[instance.email],
        )
        email.send()
