from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, FormView, TemplateView

from .forms import ParticipantUpdateForm, ParticipantRegistrationForm, SessionCreateForm, SessionUpdateForm
from .models import Experiment, Session, Participant
from .tokens import account_activation_token


class ExperimentListView(LoginRequiredMixin, ListView):
    template_name = 'experiment/experiment_list.html'
    context_object_name = 'experiments'
    redirect_field_name = None

    def get_queryset(self):
        return Experiment.objects.filter(manager=self.request.user)


class ExperimentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Experiment
    context_object_name = 'experiment'
    template_name = 'experiment/experiment_detail.html'

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False


class ExperimentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Experiment
    template_name = 'experiment/experiment_create.html'
    success_message = "Experiment successfully created"
    success_url = reverse_lazy('experiment:experiment_list')
    fields = [
        'name',
        'email',
        'phone',
        'registration_help',
        'final_instructions',
    ]

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super(ExperimentCreateView, self).form_valid(form)


class ExperimentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Experiment
    template_name = 'experiment/experiment_update.html'
    success_message = "Experiment successfully updated"
    fields = [
        'name',
        'email',
        'phone',
        'registration_help',
        'final_instructions',
    ]

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False


class ExperimentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experiment
    template_name = 'experiment/confirm_delete.html'
    extra_context = {'typename': 'experiment'}
    success_url = reverse_lazy('experiment:experiment_list')
    success_message = "Experiment successfully deleted"

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class SessionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    context_object_name = 'session'
    template_name = 'experiment/session_detail.html'
    fields = [
        'date',
        'time',
        'place',
        'max_subjects',
    ]

    def get_queryset(self):
        return Session.objects.filter(experiment__manager=self.request.user)

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False


class SingleSessionCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Session
    form_class = SessionCreateForm
    template_name = 'experiment/session_create.html'
    success_message = "Session successfully created"
    experiment = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=kwargs.get('pk'))

    def test_func(self):
        return True if self.request.user == self.experiment.owner else False

    def form_valid(self, form):
        """Add experiment to valid session form."""
        form.instance.experiment = self.experiment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add experiment instance to context"""
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context

    def get_success_url(self):
        """Return to experiment index."""
        return self.experiment.get_absolute_url()


class MultipleSessionCreateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = formset_factory(SessionCreateForm, validate_min=1)
    template_name = 'experiment/session_create_multiple.html'
    success_message = "Session successfully created"
    experiment = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        """Add experiment instance to context."""
        context = super().get_context_data(**kwargs)
        context['experiment'] = self.experiment
        return context

    def form_valid(self, formset):
        """Add experiment instance to valid session form data."""
        for form in formset:
            form.instance.experiment = self.experiment
            form.save()
        return super().form_valid(formset)

    def get_success_url(self):
        """Return to experiment index."""
        return self.experiment.get_absolute_url()


class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Session
    form_class = SessionUpdateForm
    template_name = 'experiment/session_update.html'
    success_message = "Session successfully updated"

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False

    def get_success_url(self):
        return self.object.experiment.get_absolute_url()


class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Session
    template_name = 'experiment/confirm_delete.html'
    extra_context = {'typename': 'session'}
    success_message = "Session successfully deleted"

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False

    def get_success_url(self):
        return self.object.experiment.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class ParticipantCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Participant
    template_name = 'experiment/participant_create.html'
    success_message = "Participant successfully created"
    fail_message = "This session is already full."
    session = None
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
    ]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.session = get_object_or_404(Session, pk=self.kwargs['pk'])

    def test_func(self):
        return True if self.request.user == self.session.owner else False

    def form_valid(self, form):
        """Bind calling session to participant instance."""
        if self.session.is_full:
            messages.error(self.request, self.fail_message)
            return self.form_invalid(form)
        form.instance.session = self.session
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add session instance to context"""
        context = super().get_context_data(**kwargs)
        context['session'] = self.session
        return context

    def get_success_url(self):
        """Return to session index."""
        return self.session.get_absolute_url()


class ParticipantUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Participant
    form_class = ParticipantUpdateForm
    template_name = 'experiment/participant_update.html'
    success_message = "Participant successfully updated"

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False

    def form_valid(self, form):
        """Check if participant can be activated."""
        is_activated = False
        if 'is_active' in form.changed_data and form.cleaned_data['is_active']:
            is_activated = True
        if is_activated and form.instance.session.is_full:
            form.add_error('is_active', "You cannot activate this participant. The session is full.")
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        """Return to session index."""
        return self.object.get_absolute_url()


class ParticipantListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'experiment/participant_list.html'
    context_object_name = 'participants'
    experiment = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=kwargs.get('pk'))

    def test_func(self):
        return True if self.request.user == self.experiment.owner else False

    def get_queryset(self):
        """Limit list of participants to session members."""
        return Participant.objects.filter(session__experiment=self.experiment).order_by('last_name')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['experiment'] = self.experiment
        return context


class ParticipantDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Participant
    template_name = 'experiment/confirm_delete.html'
    extra_context = {'typename': 'participant'}
    success_message = "Participant successfully deleted"

    def test_func(self):
        return True if self.request.user == self.get_object().owner else False

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """Return to session index."""
        return self.object.get_absolute_url()


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = ParticipantRegistrationForm
    template_name = 'experiment/registration_create.html'
    success_message = "An email will be sent you shortly. Click on the link in that email to complete the registration"

    def get_form_kwargs(self):
        experiment = get_object_or_404(Experiment, pk=self.kwargs.get('pk'))
        kwargs = super().get_form_kwargs()
        kwargs.update({'experiment': experiment})
        return kwargs

    def get_context_data(self, **kwargs):
        """Add session instance to context"""
        context = super().get_context_data(**kwargs)
        context['experiment'] = get_object_or_404(Experiment, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('experiment:registration_success', kwargs={'pk': self.kwargs.get('pk')})


class RegistrationPreConfirmView(TemplateView):
    template_name = 'experiment/registration_pre_confirmation.html'


class RegistrationActivateView(View):
    token_invalid_message = "Your link is broken."
    participant_missing_message = "Your registration does not exist"
    already_registered_message = "Your registration has been confirmed already. Check your inbox."
    success_message = "Your registration has been confirmed. An email will be sent you shortly, " \
                      "confirming the details of which session you are in."

    def get_participant(self):
        """Get participant from encoded uid"""
        uid_decoded = force_text(urlsafe_base64_decode(self.kwargs.get('uidb64')))
        try:
            participant = Participant.objects.get(pk=uid_decoded)
        except Participant.DoesNotExist:
            participant = None
        return participant

    def get(self, request, *args, **kwargs):
        """Find participant and update confirmed_email field."""
        participant = self.get_participant()

        if participant and participant.confirmed_email:
            messages.success(self.request, self.already_registered_message)
        elif participant and not participant.confirmed_email:
            valid_token = account_activation_token.check_token(participant, self.kwargs.get('token'))
            print(f'Has a valid token: {valid_token}')
            participant.confirmed_email = True
            participant.save(update_fields=['confirmed_email'])
            messages.success(self.request, self.success_message)
        else:
            messages.error(self.request, self.participant_missing_message)

        return HttpResponseRedirect(reverse('experiment:registration_confirm'))


class RegistrationPostConfirmView(TemplateView):
    template_name = 'experiment/registration_post_confirmation.html'


class AboutView(TemplateView):
    template_name = 'experiment/about.html'


class LicenseView(TemplateView):
    template_name = 'experiment/license.html'
