from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView

from account.forms import UserRegisterForm


class AccessMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        """
        Test function requires that the logged in user
         is the same as user in the profile view.
        :return:
        """
        requested_user = self.get_object()
        logged_in_user = get_user(self.request)
        return requested_user.id == logged_in_user.id


class MyLoginView(LoginView):
    redirect_authenticated_user = False
    next = reverse_lazy('experiment:experiment_list')
    template_name = 'account/login.html'


class MyLogoutView(LogoutView):
    template_name = 'account/logout.html'


class MySignUpView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'account/registration.html'
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return reverse_lazy('experiment:experiment_list')


class MyProfileDetailView(AccessMixin, DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'account/profile_detail.html'
    raise_exception = True


class MyProfileUpdateView(AccessMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'account/profile_update.html'
    success_message = "Thanks %(first_name)s, your profile has been updated!"
    raise_exception = True

    def get_success_url(self):
        return reverse('account:profile', kwargs={'pk': self.kwargs.get('pk')})


class MyProfileDeleteView(AccessMixin, DeleteView):
    model = User
    template_name = 'account/profile_delete.html'
    success_url = reverse_lazy('profile_delete_success')
    success_message = 'Your profile has been deleted!'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class MyProfileDeleteDoneView(TemplateView):
    template_name = 'account/profile_delete_success.html'
