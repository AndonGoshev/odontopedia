from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from odontopedia.accounts.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(f"Signal triggered for user: {instance.email}")  # Debug print
    if created:
        print("Creating profile for new user...")
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.email}")  # Debug print

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    instance.profile.save()
