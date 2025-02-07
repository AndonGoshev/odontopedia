from lib2to3.fixes.fix_input import context

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from odontopedia import settings
from odontopedia.accounts.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        subject = 'Welcome to Odontopedia!'
        # message = f'Hello {instance.first_name}! Welcome to Odontopedia!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        context = {'first_name': instance.first_name,}
        html_message = render_to_string('emails/welcome-email.html', context)

        send_mail(subject, '', from_email, recipient_list, html_message=html_message)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


