from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.deconstruct import deconstructible

from odontopedia.accounts.choices import SignupMethodChoices, UniversityChoices


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Create and return a superuser with the given email, first name, last name, and password.
        """
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


@deconstructible
class UploadToUserProfileImage:
    def __call__(self, instance, filename):
        # Split the email and get the part before the '@' symbol
        return f'accounts/{instance.email.split("@")[0]}/profile_images/{filename}'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30,)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.ImageField(upload_to=UploadToUserProfileImage(), default='default_images/profile_image.jpg')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    sign_up_method = models.CharField(max_length=20, choices=SignupMethodChoices, default=SignupMethodChoices.ODONTOPEDIA)
    premium_status = models.BooleanField(default=False)
    number_of_tuitions = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True,)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):

        self.first_name = self.first_name if self.first_name else 'User'
        self.last_name = self.last_name if self.last_name else ''
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'User {self.first_name} {self.last_name} with email {self.email}'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True, choices=UniversityChoices, default=UniversityChoices.INITIAL)
    bio = models.CharField(max_length=500, blank=True, null=True , default='Please add some information about you.')



    def __str__(self):
        return self.user.email

