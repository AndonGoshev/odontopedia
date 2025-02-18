from django.db import models

from odontopedia.accounts.models import CustomUser


class AvailableSlot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} at {self.time}"


class Booking(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slot = models.ForeignKey(AvailableSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.student.email} on {self.slot}"


class MeetingRoom(models.Model):
    link = models.URLField()

    def __str__(self):
        return f"Meeting room {self.link}"