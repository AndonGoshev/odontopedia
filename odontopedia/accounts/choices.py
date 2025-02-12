from django.db import models

class SignupMethodChoices(models.TextChoices):
    ODONTOPEDIA = 'odontopedia', 'Odontopedia'
    GOOGLE = 'google', 'GOOGLE'


class UniversityChoices(models.TextChoices):
    INITIAL = 'Select University'
    PLOVDIV_MED_UNI = 'PLOVDIV MED UNI'
    VARNA_MED_UNI = 'VARNA MED UNI'