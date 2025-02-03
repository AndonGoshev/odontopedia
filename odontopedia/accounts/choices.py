from django.db import models

class SignupMethodChoices(models.TextChoices):
    ODONTOPEDIA = 'odontopedia', 'Odontopedia'
    GOOGLE = 'google', 'GOOGLE'