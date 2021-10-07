from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class MyLoginView(LoginView):
    redirect_authenticated_user = False
    next = reverse_lazy('experiment:experiment_list')
    template_name = 'account/login.html'


class MyLogoutView(LogoutView):
    template_name = 'account/logout.html'


class MySignUpView(SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'account/registration.html'
    success_message = "Your profile was created successfully"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('experiment:experiment_list')
        else:
            return self.form_invalid(form)
