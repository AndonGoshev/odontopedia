from datetime import datetime

from PIL import Image
from decouple import config
from django.contrib.auth import login, get_user
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.core.files.base import ContentFile
from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import CreateView, DeleteView

from google.auth.transport import requests
from google.oauth2 import id_token
from jwt import InvalidTokenError
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from odontopedia import settings
from odontopedia.accounts.choices import SignupMethodChoices, UniversityChoices
from odontopedia.accounts.forms import RegistrationForm, CustomLoginForm, CustomPasswordChangeForm, \
    CustomPasswordResetForm, CustomPasswordSetForm, UserProfileForm
from odontopedia.accounts.models import CustomUser, Profile
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

    def form_invalid(self, form):
        print(form.errors)

        return super().form_invalid(form)




class CustomLoginView(LoginView):
    template_name = 'accounts/auth/login.html'
    form_class = CustomLoginForm

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


class UserProfileUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)  # Ensure profile exists
        date_of_birth = profile.date_of_birth.strftime('%Y-%m-%d') if profile.date_of_birth else 'None'

        return render(request, 'accounts/manage/account-settings.html', {
            'user': user,
            'profile': profile,
            'date_of_birth': date_of_birth,  # Pass it explicitly
        })

    def post(self, request, *args, **kwargs):
        field = request.POST.get('field')
        value = request.POST.get('value')
        print(f"Field: {field}, Value: {value}")  # Debug
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        try:

            if field == 'date_of_birth':
                if not value:
                    return JsonResponse({'error': 'Date of birth cannot be empty'}, status=400)
                # Convert date string to datetime object
                profile.date_of_birth = datetime.strptime(value, '%Y-%m-%d')
                profile.save()
                return JsonResponse({'message': 'Date of birth updated successfully',
                                     'value': profile.date_of_birth.strftime('%Y-%m-%d')})
            # First, check if it's a profile image upload
            if field == 'profile_image' and 'profile_image' in request.FILES:
                uploaded_image = request.FILES['profile_image']
                # Allow only JPG and PNG MIME types
                allowed_types = ['image/jpeg', 'image/png']
                if uploaded_image.content_type not in allowed_types:
                    return JsonResponse({'error': 'Only JPG and PNG files are allowed.'}, status=400)

                user.profile_image = uploaded_image
                user.save()
                return JsonResponse({
                    'message': 'Profile image updated successfully',
                    'value': user.profile_image.url
                })

            # Then handle text fields for first and last name
            elif field in ['first_name', 'last_name']:
                if not value:
                    return JsonResponse({'error': f'{field} cannot be empty'}, status=400)
                setattr(user, field, value)
                user.save()

            # And handle profile fields for age and university
            elif field in ['date_of_birth', 'university', 'bio']:
                if not value:
                    return JsonResponse({'error': f'{field} cannot be empty'}, status=400)
                setattr(profile, field, value)
                profile.save()

            else:
                return JsonResponse({'error': 'Invalid field'}, status=400)

            return JsonResponse({
                'message': f'Field was updated successfully',
                'value': getattr(user, field, None) if field not in ['profile_image'] else user.profile_image.url,
            })

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)


def get_university_data(request):
    # Directly use UniversityChoices' choices
    university_choices = [choice[0] for choice in UniversityChoices.choices]
    print(university_choices)

    user = request.user
    user_university = user.profile.university

    return JsonResponse({
        "universities": university_choices,
        "user_university": user_university
    })


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/auth/password/password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password-change-done')


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/auth/password/password-change-done.html'


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordSetForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    pass

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/account-delete.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'