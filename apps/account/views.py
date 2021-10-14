from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, TemplateView

from registration.backends.admin_approval.views import RegistrationView

from .forms import UserRegisterForm


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


class MySignUpView(RegistrationView):
    form_class = UserRegisterForm
    template_name = 'account/signup.html'


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
        return reverse('account:profile_detail', kwargs={'pk': self.kwargs.get('pk')})


class MyProfileDeleteView(AccessMixin, DeleteView):
    model = User
    template_name = 'account/profile_delete.html'
    success_url = reverse_lazy('account:profile_delete_success')
    success_message = 'Your profile has been deleted!'
    raise_exception = True

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class MyProfileDeleteDoneView(TemplateView):
    template_name = 'account/profile_delete_success.html'
