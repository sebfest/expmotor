from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, FormView, TemplateView

from .forms import RegistrationForm, SessionCreateForm, SessionUpdateForm, \
    RegistrationCreateOrUpdateForm
from .models import Experiment, Session, Registration
from .tokens import account_activation_token


class ExperimentListView(LoginRequiredMixin, ListView):
    template_name = 'experiment/experiment_list.html'
    context_object_name = 'experiments'
    redirect_field_name = None

    def get_queryset(self):
        """Get all experiments belonging to the logged-in user."""
        return Experiment.objects.filter(manager=self.request.user)


class ExperimentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Experiment
    context_object_name = 'experiment'
    template_name = 'experiment/experiment_detail.html'

    def test_func(self):
        """Only experiment owners allowed to view experiment."""
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
        'title',
        'registration_help',
        'final_instructions',
    ]

    def form_valid(self, form):
        """Add logged in user to new experiment."""
        form.instance.manager = self.request.user
        return super().form_valid(form)


class ExperimentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Experiment
    template_name = 'experiment/experiment_update.html'
    success_message = "Experiment successfully updated"
    fields = [
        'name',
        'email',
        'phone',
        'title',
        'registration_help',
        'final_instructions',
    ]

    def test_func(self):
        """Only experiment owners allowed to update experiment."""
        return True if self.request.user == self.get_object().owner else False


class ExperimentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Experiment
    template_name = 'experiment/confirm_delete.html'
    extra_context = {'typename': 'experiment'}
    success_url = reverse_lazy('experiment:experiment_list')
    success_message = "Experiment successfully deleted"

    def test_func(self):
        """Only experiment owners allowed to delete experiment."""
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
        """Get session belonging to owner of related experiment."""
        return Session.objects.filter(experiment__manager=self.request.user)

    def test_func(self):
        """Only experiment owners allowed to view session."""
        return True if self.request.user == self.get_object().owner else False


class SessionCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Session
    form_class = SessionCreateForm
    template_name = 'experiment/session_create.html'
    success_message = "Session successfully created"
    experiment = None

    def setup(self, request, *args, **kwargs):
        """Get related experiment."""
        super().setup(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=kwargs.get('pk'))

    def test_func(self):
        """Only experiment owners allowed to create session for the experiment."""
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
        """Return to experiment detail view."""
        return self.experiment.get_absolute_url()


class SessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Session
    form_class = SessionUpdateForm
    template_name = 'experiment/session_update.html'
    success_message = "Session successfully updated"

    def test_func(self):
        """Only session owners allowed to update session."""
        return True if self.request.user == self.get_object().owner else False

    def get_success_url(self):
        """Return to experiment detail view."""
        return self.object.experiment.get_absolute_url()


class SessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Session
    template_name = 'experiment/confirm_delete.html'
    extra_context = {'typename': 'session'}
    success_message = "Session successfully deleted"

    def test_func(self):
        """Only session owners allowed to delete session."""
        return True if self.request.user == self.get_object().owner else False

    def get_success_url(self):
        """Return to experiment detail view."""
        return self.object.experiment.get_absolute_url()

    def delete(self, request, *args, **kwargs):
        """Add delete message."""
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class RegistrationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'experiment/registration_list.html'
    context_object_name = 'registrations'
    experiment = None
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        """Add experiment to view"""
        super().setup(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=kwargs.get('pk'))

    def test_func(self):
        """Only owner can view registrations."""
        return True if self.request.user == self.experiment.owner else False

    def get_queryset(self):
        """Get all registrations for experiment."""
        return Registration.objects.filter(session__experiment=self.experiment).order_by('last_name')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add experiment instance to context."""
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['experiment'] = self.experiment
        return context


class RegistrationSearchView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Registration
    context_object_name = 'registrations'
    template_name = 'experiment/registration_list.html'
    experiment = None

    def setup(self, request, *args, **kwargs):
        """Add experiment to view"""
        super().setup(request, *args, **kwargs)
        self.experiment = get_object_or_404(Experiment, pk=kwargs.get('pk'))

    def test_func(self):
        """Only owner can view registrations."""
        return True if self.request.user == self.experiment.owner else False

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add experiment instance to context."""
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['experiment'] = self.experiment
        return context

    def get_queryset(self):
        """Filter search results."""
        query = self.request.GET.get("q")
        object_list = Registration.objects.select_related().filter(
            Q(session__experiment__manager=self.request.user),
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        return object_list


class RegistrationCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Registration
    form_class = RegistrationCreateOrUpdateForm
    template_name = 'experiment/registration_create.html'
    success_message = "Registration successfully created."
    session_full_message = "This session is already full."
    session = None

    def setup(self, request, *args, **kwargs):
        """Add session to view"""
        super().setup(request, *args, **kwargs)
        self.session = get_object_or_404(Session, pk=self.kwargs['pk'])

    def test_func(self):
        """Only session owners can create registrations."""
        return True if self.request.user == self.session.owner else False

    def get_form_kwargs(self):
        """Add session instance to form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'session': self.session})
        return kwargs

    def form_valid(self, form):
        """Check if session has been filled up."""
        session = get_object_or_404(Session, pk=self.kwargs['pk'])
        if session.is_full:
            messages.error(self.request, self.session_full_message)
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Add session instance to context"""
        context = super().get_context_data(**kwargs)
        context['session'] = self.session
        return context

    def get_success_url(self):
        """Return to session index."""
        return self.object.get_absolute_url()


class RegistrationUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Registration
    form_class = RegistrationCreateOrUpdateForm
    template_name = 'experiment/registration_update.html'
    success_message = "Registration successfully updated."

    def test_func(self):
        """Only session owners can update registrations."""
        return True if self.request.user == self.get_object().owner else False

    def get_form_kwargs(self):
        """Add session to form."""
        session = get_object_or_404(Session, pk=self.kwargs.get('pk_ses'))
        kwargs = super().get_form_kwargs()
        kwargs.update({'session': session})
        return kwargs

    def form_valid(self, form):
        """Check if registration can be activated."""
        is_activated = False
        if 'is_active' in form.changed_data and form.cleaned_data['is_active']:
            is_activated = True

        if is_activated and form.instance.session.is_full:
            form.add_error('is_active', "You cannot activate this registration. The session is already full.")
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        """Return to session index."""
        return self.object.get_absolute_url()


class RegistrationDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Registration
    template_name = 'experiment/confirm_delete.html'
    success_message = "Registration successfully deleted"

    def test_func(self):
        """Only owner can delete registration."""
        return True if self.request.user == self.get_object().owner else False

    def delete(self, request, *args, **kwargs):
        """Add delete message."""
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """Return to session index."""
        return self.object.get_absolute_url()


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'experiment/registration.html'
    success_message = "An email will be sent you shortly. Click on the link in that email to complete the registration."

    def get_form_kwargs(self):
        """Add experiment to form."""
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
        """Redirect to registration success page."""
        return reverse('experiment:registration_success', kwargs={'pk': self.kwargs.get('pk')})


class RegistrationPreConfirmView(TemplateView):
    template_name = 'experiment/registration_pre_confirmation.html'


class RegistrationActivateView(View):
    token_invalid_message = "Your link is broken."
    registration_missing_message = "Your registration does not exist."
    already_registered_message = "Your registration has been confirmed already. Check your inbox."
    registration_success_message = "Your registration has been confirmed. An email will be sent you shortly, " \
                                   "confirming the details of which session you are in."

    def get_registration(self):
        """Get registration from encoded uid."""
        uid_decoded = force_text(urlsafe_base64_decode(self.kwargs.get('uidb64')))
        registration = None
        try:
            registration = Registration.objects.get(pk=uid_decoded)
        except Registration.DoesNotExist:
            pass
        except Registration.MultipleObjectsReturned:
            pass
        finally:
            return registration

    def check_token(self, registration):
        """Check if token is valid"""
        is_valid_token = account_activation_token.check_token(
            registration,
            self.kwargs.get('token')
        )
        return is_valid_token

    def get(self, request, *args, **kwargs):
        """Find registration and update confirmed_email field."""
        registration = self.get_registration()
        valid_token = self.check_token(registration)

        if not registration:
            messages.error(self.request, self.registration_missing_message)
        elif registration and registration.confirmed_email:
            messages.success(self.request, self.already_registered_message)
        elif registration and valid_token and not registration.confirmed_email:
            registration.confirmed_email = True
            registration.save(update_fields=['confirmed_email'])
            messages.success(self.request, self.registration_success_message)
        else:
            messages.error(self.request, self.token_invalid_message)

        return HttpResponseRedirect(reverse('experiment:registration_confirm'))


class RegistrationPostConfirmView(TemplateView):
    template_name = 'experiment/registration_post_confirmation.html'


class AboutView(TemplateView):
    template_name = 'experiment/about.html'


class LicenseView(TemplateView):
    template_name = 'experiment/license.html'
