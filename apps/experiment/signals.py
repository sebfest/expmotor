from io import BytesIO
from typing import Type, FrozenSet, Optional

import qrcode

from django.contrib.sites.models import Site
from django.core.files.uploadedfile import InMemoryUploadedFile
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
from .models import Experiment, Registration
from .tokens import account_activation_token


@receiver(post_save, sender=Experiment)
def send_new_experiment_notification_email(sender: Type[Experiment], instance: Experiment, created: bool, **kwargs) -> None:
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


@receiver(post_save, sender=Experiment)
def generate_qr_code_for_experiment(sender: Type[Experiment], instance: Experiment, created: bool, **kwargs) -> None:
    """Generate qr code image after successful experiment creation."""
    if created:
        file_ext = 'PNG'
        file_name = f'{instance.name}_qr_code.{file_ext.lower()}'
        file_content_type = 'image/png'

        qr_content = instance.get_full_absolute_url()
        qr = qrcode.QRCode()
        qr.add_data(qr_content)
        qr.make()

        buffer = BytesIO()
        image = qr.make_image(fill='black', back_color='white')
        image.save(buffer, file_ext)

        uploaded_file = InMemoryUploadedFile(
            file=buffer,
            field_name=None,
            name=file_name,
            content_type=file_content_type,
            size=buffer.tell(),
            charset=None
        )
        instance.qr_code_image.save(file_name, uploaded_file, save=True)

        for temporary in [image, buffer, uploaded_file]:
            temporary.close()


@receiver(post_save, sender=Registration)
def send_email_confirmation_request(sender: Type[Registration], instance: Registration,
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

        title = instance.session.experiment.name
        subject = f'{title}: Please confirm your email'
        context_dict = {
            'registration_link': url,
            'name': instance.first_name,
            'title': title,
        }
        recipient = instance.email
        html_message = render_to_string('experiment/registration_pre_conformation_email.html', context_dict)
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
def send_registration_info(sender: Type[Registration], instance: Registration,
                           created: bool, update_fields: Optional[FrozenSet], **kwargs) -> None:
    """Send email with registration info after email confirmation."""
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

        email = EmailMessage(
            from_email=sender,
            to=[recipient],
            subject=subject,
            body=message,
        )
        email.send(fail_silently=True)
