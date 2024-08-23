from typing import Type, FrozenSet, Optional

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from settings.production import EMAIL_HOST_USER
from .email import send_confirmation_request, send_registration_info, send_registration_info_update
from .models import Experiment, Registration


@receiver(post_save, sender=Experiment)
def send_new_experiment_notification_email(
        sender: Type[Experiment],
        instance: Experiment,
        created: bool,
        **kwargs) -> None:
    """Send confirmation email after successful experiment creation."""
    if created:
        context_dict = {
            'experiment_name': instance.name,
            'experiment_url': instance.get_full_absolute_url(),
            'invitation_manager': instance.manager.get_username(),
        }
        subject = f'[Expmotor] Experiment created ({instance.name})'
        recipient = instance.manager.email
        html_message = render_to_string('experiment/experiment_created_confirmation_email.html', context_dict)
        message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=True,
        )


@receiver(post_save, sender=Registration)
def handle_emails_for_registration(
        sender: Type[Registration],
        instance: Registration,
        created: bool,
        update_fields: Optional[FrozenSet],
        **kwargs) -> None:
    if created:
        send_confirmation_request(instance=instance)
    elif not created and update_fields and 'confirmed_email' in update_fields:
        send_registration_info(instance=instance)
    elif not created and update_fields and 'session' in update_fields:
        send_registration_info_update(instance=instance)
    else:
        return
