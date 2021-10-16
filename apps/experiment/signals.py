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
from settings.production import EMAIL_HOST_USER


def send_mail(subject: str, body: str, recipient: str) -> None:
    """Send email from host to single recipient."""
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=EMAIL_HOST_USER,
        to=[recipient],
    )
    email.send()


@receiver(post_save, sender=Experiment)
def send_new_experiment_notification_email(sender: Type[Experiment], instance: Experiment,
                                           created: bool, **kwargs) -> None:
    """Send confirmation email after successful experiment creation."""
    if created:
        context_dict = {
            'experiment_name': instance.name,
            'experiment_url': instance.get_full_absolute_url(),
            'invitation_manager': instance.manager.get_username(),
        }
        recipient = instance.email
        message = render_to_string('experiment/experiment_created_confirmation.txt', context_dict)
        subject = f'[Expmotor] Experiment created ({instance.name})'

        send_mail(subject=subject, body=message, recipient=recipient)


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

        subject = '[Expmotor] Please confirm your email'
        message = template.render(context)
        recipient = instance.email

        send_mail(subject=subject, body=message, recipient=recipient)


@receiver(post_save, sender=Participant)
def send_registration_info(sender: Type[Participant], instance: Participant,
                           created: bool, update_fields: Optional[FrozenSet], **kwargs) -> None:
    """Send email with registration_old info after email confirmation."""
    if not created and update_fields and 'confirmed_email' in update_fields:
        template = Template(instance.session.experiment.final_instructions)
        context_dict = {
            'place': instance.session.place,
            'date': instance.session.date,
            'time': instance.session.time,
            'manager': instance.session.experiment.manager,
        }
        context = Context(context_dict)

        subject='[Expmotor] Confirmation of experiment participation'
        message = template.render(context)
        recipient = instance.email

        send_mail(subject=subject, body=message, recipient=recipient)
