from decouple import config
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import CreateView

from google.auth.transport import requests
from google.oauth2 import id_token
from jwt import InvalidTokenError
from rest_framework.views import APIView

from odontopedia import settings
from odontopedia.accounts.choices import SignupMethodChoices
from odontopedia.accounts.forms import RegistrationForm
from odontopedia.accounts.models import CustomUser
from odontopedia.settings import GOOGLE_OAUTH_CLIENT_ID


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


@method_decorator(csrf_exempt, name='dispatch')
class AuthGoogle(APIView):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    def post(self, request, *args, **kwargs):
        try:
            user_data = self.get_google_user_data(request)
        except (ValueError, InvalidTokenError) as e:
            return HttpResponse(f"Invalid Google token: {str(e)}", status=403)

        email = user_data["email"]
        user, created = CustomUser.objects.get_or_create(
            email=email, defaults={
                "email": email,
                "sign_up_method": SignupMethodChoices.GOOGLE,
                "first_name": user_data.get("given_name"),
                'last_name': user_data.get("family_name"),
            }
        )

        try:
            login(request, user)

        except Exception as e:
            print(e)

        # print(user.email)  # Example usage of the user
        print(f"Was the user created? {'Yes' if created else 'No'}")

        # Add any other logic, such as setting a http only auth cookie as needed here.
        return redirect('home')

    @staticmethod
    def get_google_user_data(request: HttpRequest):
        token = request.POST['credential']
        return id_token.verify_oauth2_token(
            token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID
        )
