from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from odontopedia.accounts.models import CustomUser


class RegistrationForm(forms.ModelForm):
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


