from typing import Type, FrozenSet, Optional

from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Template, Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from settings.production import EMAIL_HOST_USER
from .models import Experiment, Participant
from .tokens import account_activation_token


def send_my_mail(sender: Optional[str] = EMAIL_HOST_USER, *, recipient: str, subject: str, body: str) -> None:
    """Send email from host to single recipient."""
    email = EmailMessage(
        from_email=sender,
        to=[recipient],
        subject=subject,
        body=body,
    )
    email.send(fail_silently=True)


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
        recipient = instance.manager.email
        message = render_to_string('experiment/experiment_created_confirmation.txt', context_dict)
        subject = f'[Expmotor] Experiment created ({instance.name})'

        send_my_mail(recipient=recipient, subject=subject, body=message)


@receiver(post_save, sender=Participant)
def send_email_confirmation_request(sender: Type[Participant], instance: Participant,
                                    created: bool, update_fields: Optional[FrozenSet], **kwargs) -> None:
    """Send request to conform email after successful creation."""
    if created:
        domain = Site.objects.get_current().domain
        path = reverse(
            'experiment:registration_activate',
            kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': account_activation_token.make_token(instance),
            }
        )
        url = f'https://{domain}{path}'


        recipient = instance.email
        name = instance.first_name
        title = instance.session.experiment.name
        subject = f'{title}: Please confirm your email'
        html_message = render_to_string(
            'experiment/participant_pre_conformation_email.html',
            {
                'registration_link': url,
                'name': name,
                'title': title,
            }
        )
        message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=True,
        )


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
            'email': instance.session.experiment.email,
            'phone': instance.session.experiment.phone,
        }
        context = Context(context_dict)

        title = instance.session.experiment.name
        subject = f'{title}: Confirmation of experiment participation'
        message = template.render(context)
        recipient = instance.email

        send_my_mail(subject=subject, body=message, recipient=recipient)
