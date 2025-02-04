from django.db import models

class SignupMethodChoices(models.TextChoices):
    ODONTOPEDIA = 'odontopedia', 'Odontopedia'
    GOOGLE = 'google', 'GOOGLE'


class UniversityChoices(models.TextChoices):
    PLOVDIV_MED_UNI = 'plovdiv_med_uni', 'PLOVDIV_MED_UNI'
    VARNA_MED_UNI = 'varna_med_uni', 'VARNA_MED_UNI'