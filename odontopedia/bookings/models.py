from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from odontopedia.accounts.models import CustomUser


class Slot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} at {self.time}"


class Booking(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(Slot, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now, )
    time = models.TimeField(default=timezone.now, )
    created_at = models.DateTimeField(auto_now_add=True)
    focus_area = models.CharField(max_length=100, )
    description = models.CharField(max_length=300, )
    video_link = models.URLField(blank=True, null=True)

    session_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.student.email} on {self.slot}"


class MeetingRoom(models.Model):
    room_link = models.URLField()

    def __str__(self):
        return f"Meeting room {self.room_link}"


class TuitionFocusArea(models.Model):
    name = models.CharField(max_length=100, )
