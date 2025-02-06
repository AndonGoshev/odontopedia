from django import forms


class AuthFormsPlaceholderMixin(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'password2':
                self.fields[field].label = 'Confirm password'
                self.fields[field].widget.attrs['placeholder'] = ''
                continue

            elif field == 'first_name':
                self.fields[field].label = 'First name'
                self.fields[field].widget.attrs['placeholder'] = ''
                continue

            elif field == 'last_name':
                self.fields[field].label = 'Last name'
                self.fields[field].widget.attrs['placeholder'] = ''
                continue

            self.fields[field].label = field.capitalize()
            self.fields[field].widget.attrs['placeholder'] = ''


class NewPasswordPlaceholderMixin(forms.Form):
    PASSWORDS_PLACEHOLDERS_MAP = {
        'old_password': 'Old password',
        'new_password1': 'New password',
        'new_password2': 'Confirm password',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].label = self.PASSWORDS_PLACEHOLDERS_MAP[field].capitalize()
            self.fields[field].widget.attrs['placeholder'] = ''