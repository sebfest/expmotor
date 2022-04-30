from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from django import forms
from django.core.validators import MinValueValidator
from django.db.models import F, Count, Q
from django.utils import timezone
from django.utils.safestring import mark_safe

from .models import Registration, Session


class SessionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            max_subjects_validator = self.get_max_subjects_validator()
            self.fields['max_subjects'].validators.append(max_subjects_validator)
            self.fields['max_subjects'].widget.attrs['min'] = max_subjects_validator.limit_value

    def get_max_subjects_validator(self):
        """Return validator to not allow fewer slots than registered subjects"""
        min_value = self.instance.participants.filter(is_active=True).count()
        message = f'The maximum number of participants must be larger than {min_value}'
        return MinValueValidator(limit_value=min_value, message=message)

    class Meta:
        model = Session
        fields = [
            'date',
            'time',
            'place',
            'max_subjects',
        ]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'time': TimePickerInput(format='%H:%M'),
        }


class SessionCreateForm(SessionForm):

    def clean_date(self):
        """Ensure new session instances are in the future."""
        session_date = self.cleaned_data['date']
        today = timezone.now().date()

        if session_date <= today:
            self.add_error(None, forms.ValidationError("Session date must be in the future"))
            self.add_error('date', forms.ValidationError("Session date must be in the future"))
        return session_date

    class Meta(SessionForm.Meta):
        fields = SessionForm.Meta.fields


class SessionUpdateForm(SessionForm):
    class Meta(SessionForm.Meta):
        fields = SessionForm.Meta.fields + ['is_active', ]


class RegistrationCreateOrUpdateForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'session',
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session')
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['session'].queryset = self.get_all_available_sessions()
        else:
            self.fields['session'].queryset = self.get_parent_session()
            self.fields['session'].empty_label = None
            self.fields['session'].required = False
            self.fields['session'].disabled = True
            self.fields['session'].widget = forms.HiddenInput()

    def get_all_available_sessions(self):
        """Find available sessions."""
        active_participants = Q(participants__is_active=True)
        available_sessions = Session.objects \
            .filter(experiment_id=self.instance.session.experiment.id) \
            .annotate(free_slots=F('max_subjects') - Count('participants', filter=active_participants)) \
            .filter(free_slots__gte=0)
        return available_sessions

    def get_parent_session(self):
        return Session.objects.filter(pk=self.session.pk)

    def clean_session(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return self.session
        else:
            return self.cleaned_data['session']


class RegistrationForm(forms.ModelForm):
    link_html = '<a data-toggle="modal" data-target="#exampleModal" href="#">privacy policy</a>'
    consent = forms.BooleanField(
        label=mark_safe(f"I confirm that I have read, consent and agree to ExpMotor's {link_html}."),
        required=True,
        error_messages={'required': 'You need to consent in order to register.'}
    )

    class Meta:
        model = Registration
        fields = [
            'session',
            'first_name',
            'last_name',
            'email',
            'phone',
        ]

    def __init__(self, *args, **kwargs):
        self.experiment = kwargs.pop('experiment')
        super().__init__(*args, **kwargs)
        if self.experiment is not None:
            self.fields['session'].queryset = self.get_available_sessions()

    def get_available_sessions(self):
        """Find available sessions"""
        valid_sessions = Session.objects\
            .filter(experiment_id=self.experiment.id)\
            .exclude(is_active=False)\
            .annotate(free_slots=F('max_subjects') - Count('participants', filter=Q(participants__is_active=True)))\
            .filter(free_slots__gt=0)
        return valid_sessions
