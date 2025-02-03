from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from odontopedia.accounts.forms import RegistrationForm
from odontopedia.accounts.models import CustomUser


class RegistrationView(CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'accounts/auth/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password'])
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    template_name = 'accounts/auth/logout.html'

    def get_success_url(self):
        return reverse_lazy('home')
