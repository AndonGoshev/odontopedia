from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from odontopedia.accounts.auth_form_styling_mixin import AuthFormsPlaceholderMixin, NewPasswordPlaceholderMixin
from odontopedia.accounts.models import CustomUser


class RegistrationForm(forms.ModelForm, AuthFormsPlaceholderMixin):
    email = forms.EmailField()
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'password2')

    def clean_first_name(self):
        """Ensure first name only contains letters."""
        first_name = self.cleaned_data.get("first_name")
        if not first_name.isalpha():
            raise ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        """Ensure last name only contains letters."""
        last_name = self.cleaned_data.get("last_name")
        if not last_name.isalpha():
            raise ValidationError("Last name must contain only letters.")
        return last_name

    def clean(self):
        """Ensure passwords match."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password:
            validate_password(password)

        if password and password2 and password != password2:
            self.add_error("password2", "Passwords do not match.")

        return cleaned_data


class CustomLoginForm(AuthenticationForm, AuthFormsPlaceholderMixin):
    pass

class CustomPasswordChangeForm(PasswordChangeForm, NewPasswordPlaceholderMixin):
    pass

class CustomPasswordResetForm(PasswordResetForm, AuthFormsPlaceholderMixin):
    pass


class CustomPasswordSetForm(SetPasswordForm, NewPasswordPlaceholderMixin):
    pass


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True,)
    last_name = forms.CharField(required=True,)
    profile_image = forms.ImageField(required=False)

    age = forms.IntegerField(required=False)
    university = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile_image', 'age', 'university')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["profile_image"].initial = user.profile_image

            if hasattr(user, 'profile'):
                self.fields['age'].initial = user.profile.age
                self.fields['university'].initial = user.profile.university