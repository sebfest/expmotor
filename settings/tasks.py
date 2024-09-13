from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives

from settings.production import EMAIL_HOST_USER
from .celery import app

logger = get_task_logger(__name__)


@app.task(name='send_email')
def send_email(subject: str, message: str, recipient: str, html_message: str | None) -> None:
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[recipient],
    )
    if html_message:
        email.attach_alternative(html_message, 'text/html')

    email.send(fail_silently=True)
    logger.info("Successfully sent email message to %s.", recipient)
