from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from odontopedia import settings
from odontopedia.accounts.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        subject = 'Welcome to Odontopedia!'
        message = f'Hello {instance.first_name}! Welcome to Odontopedia!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


