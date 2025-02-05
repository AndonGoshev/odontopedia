from django import forms


class AuthFormsPlaceholderMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'password2':
                self.fields[field].label = ''
                self.fields[field].widget.attrs['placeholder'] = 'Confirm password'
                continue

            elif field == 'first_name':
                self.fields[field].label = ''
                self.fields[field].widget.attrs['placeholder'] = 'First name'
                continue

            elif field == 'last_name':
                self.fields[field].label = ''
                self.fields[field].widget.attrs['placeholder'] = 'Last name'
                continue

            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = field.capitalize()


class NewPasswordPlaceholderMixin(forms.Form):
    PASSWORDS_PLACEHOLDERS_MAP = {
        'old_password': 'Old password',
        'new_password1': 'New password',
        'new_password2': 'Confirm password',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].widget.attrs['placeholder'] = self.PASSWORDS_PLACEHOLDERS_MAP[field].capitalize()