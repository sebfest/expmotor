from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms
from django.core.validators import MinValueValidator
from django.db.models import F, Count, Q

from experiment.models import Participant, Session


class ParticipantUpdateForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'session',
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_existing_instance = self.instance.pk is not None
        if self.is_existing_instance:
            self.fields['session'].queryset = self.get_available_sessions()

    def get_available_sessions(self):
        """Find available sessions."""
        valid_sessions = Session.objects\
            .filter(experiment_id=self.instance.session.experiment.id) \
            .annotate(free_slots=F('max_subjects') - Count('participants', filter=Q(participants__is_active=True))) \
            .filter(free_slots__gte=0)
        return valid_sessions


class ParticipantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
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
            .annotate(free_slots=F('max_subjects') - Count('participants', filter=Q(participants__is_active=True)))\
            .filter(free_slots__gt=0)
        return valid_sessions


class SessionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_existing_instance = self.instance.pk is not None
        if self.is_existing_instance:
            validator = self.get_validator()
            self.fields['max_subjects'].validators.append(validator)
            self.fields['max_subjects'].widget.attrs['min'] = validator.limit_value

    def get_validator(self):
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
    class Meta(SessionForm.Meta):
        fields = SessionForm.Meta.fields


class SessionUpdateForm(SessionForm):
    class Meta(SessionForm.Meta):
        fields = SessionForm.Meta.fields + ['is_active', ]



