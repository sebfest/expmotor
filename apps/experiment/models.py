from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models import Sum, Count, Q
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site


from .basemodels import AbstractBaseModel
from .constants import defaults
from settings.local import AUTH_USER_MODEL


class Experiment(AbstractBaseModel):
    manager = models.ForeignKey(
        AUTH_USER_MODEL,
        verbose_name=_('manager'),
        related_name='experiments',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=30,
        help_text='Name of experiment; max 30 letters.',
        unique=True,
    )
    email = models.EmailField(
        verbose_name=_('inviter email'),
        help_text='This address will appear in autogenerated e-mails. Usually this will be the '
                  'address to the person who registers the experiment in Expmotor.'
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        max_length=8,
        help_text="Phone number participants can contact.",
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Phone number must be entered in the format: '12345678'."
            )
        ]
    )
    registration_help = models.TextField(
        verbose_name=_('registration instructions'),
        default=defaults['registration_help'],
        help_text="This text will meet participants when registering for participation."
    )
    # TODO: remove
    confirmation_request = models.TextField(
        verbose_name=_('confirmation mail'),
        default=defaults['confirmation_request_email'],
        help_text="Message in email asking subjects to confirm their email address."
    )
    final_instructions = models.TextField(
        verbose_name=_('instructions mail'),
        default=defaults['final_instructions_email'],
        help_text="Message in email sent after confirmation of email address."
    )

    class Meta:
        verbose_name = _('experiment')
        verbose_name_plural = _('experiments')
        ordering = ['-created_date']
        get_latest_by = 'activation_date'

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self) -> str:
        """URL to object."""
        return reverse('experiment:experiment_detail', kwargs={'pk': self.pk})

    def get_full_absolute_url(self) -> str:
        """URL to object with domain"""
        domain = Site.objects.get_current().domain
        url = self.get_absolute_url()
        return f'https://{domain}{url}'

    @property
    def owner(self) -> AUTH_USER_MODEL:
        """Owner of object"""
        return self.manager

    @property
    def slots(self) -> int:
        """Number of available slots."""
        agg_sum = Experiment.objects.all() \
            .filter(pk=self.pk) \
            .aggregate(slots=Sum('sessions__max_subjects'))
        return agg_sum.get('slots') or 0

    @property
    def registrations(self) -> int:
        """Number of registrations."""
        agg_count = Experiment.objects.all() \
            .filter(pk=self.pk) \
            .aggregate(registrations=Count('sessions__participants', filter=Q(sessions__participants__is_active=True)))
        return agg_count.get('registrations') or 0

    @property
    def complete(self):
        """Registration rate."""
        return (self.registrations / self.slots) * 100.0 if self.slots else 0.0


class Session(AbstractBaseModel):
    experiment = models.ForeignKey(
        Experiment,
        editable=False,
        verbose_name=_('experiment'),
        related_name='sessions',
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        verbose_name=_('session date.'),
        help_text='The date of the session.',
    )
    time = models.TimeField(
        verbose_name=_('session starting time.'),
        help_text='The start time of the session.',
    )
    place = models.CharField(
        verbose_name=_('session location.'),
        max_length=50,
        help_text='The place where session is organized.',
    )
    max_subjects = models.PositiveIntegerField(
        verbose_name=_('number of subjects.'),
        help_text='The maximal number of participants that can register.',
        validators=[
            MinValueValidator(
                limit_value=1,
                message="You must provide space for at least one subject."
            )
        ],
    )

    def __str__(self) -> str:
        if self.date and self.time:
            return f"{self.date.strftime('%Y-%m-%d')}, {self.time.strftime('%H:%M:%S')}"

    def get_absolute_url(self) -> str:
        """URL to object."""
        return reverse('experiment:session_detail', kwargs={'pk_eks': self.experiment.pk, 'pk': self.pk})

    @property
    def owner(self) -> AUTH_USER_MODEL:
        """Owner of object"""
        return self.experiment.manager

    @property
    def registrations(self) -> int:
        """Number of participants registered."""
        return self.participants.filter(is_active=True).count()

    @property
    def complete(self) -> float:
        """Share of participants registered."""
        return (self.registrations / self.max_subjects) * 100.0

    @property
    def is_full(self) -> bool:
        """Checks whether session is full."""
        return self.registrations >= self.max_subjects


class Participant(AbstractBaseModel):
    session = models.ForeignKey(
        Session,
        verbose_name=_('session'),
        related_name='participants',
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=30,
        help_text='Your first name.',
    )
    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=30,
        help_text='Your last name.',
    )
    email = models.EmailField(
        verbose_name=_('email'),
        help_text='An email will be sent to this address for validation purposes, you must click on a link in this '
                  'email before registration is complete.'
    )
    confirmed_email = models.BooleanField(
        default=False,
        help_text='Set to "True" when e-mail is confirmed.'
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        max_length=15,
        help_text="Your phone number.",
    )

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self) -> str:
        return reverse(
            'experiment:session_detail',
            kwargs={'pk_eks': self.session.experiment.pk, 'pk': self.session.pk}
        )

    @property
    def owner(self):
        """Owner of object"""
        return self.session.experiment.manager
