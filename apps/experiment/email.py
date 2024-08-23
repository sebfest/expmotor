from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode

from settings.production import EMAIL_HOST_USER
from .models import Registration
from .tokens import account_activation_token


def send_confirmation_request(instance: Registration) -> None:
    """Send request to conform email after successful creation."""
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
    html_message = render_to_string('experiment/registration_pre_confirmation_email.html', context_dict)
    message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[recipient],
    )
    email.attach_alternative(html_message, 'text/html')
    email.send(fail_silently=True)


def send_registration_info(instance: Registration) -> None:
    """Send email with registration info after email confirmation."""
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

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[recipient],
    )
    email.send(fail_silently=True)


def send_registration_info_update(instance: Registration) -> None:
    """Send email with updated registration info after email registration change."""
    title = instance.session.experiment.name
    subject = f'{title}: Your registration has changed.'
    context_dict = {
        'name': instance.first_name,
        'title': title,
        'place': instance.session.place,
        'date': instance.session.date,
        'time': instance.session.time,
        'manager': instance.session.experiment.manager,
        'email': instance.session.experiment.email,
        'phone': instance.session.experiment.phone,
    }
    recipient = instance.email
    html_message = render_to_string('experiment/registration_update_confirmation_email.html', context_dict)
    message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[recipient],
    )
    email.attach_alternative(html_message, 'text/html')
    email.send(fail_silently=True)
