from django.contrib import admin

from odontopedia.bookings.models import Booking, AvailableSlots, MeetingRoom


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(AvailableSlots)
class AvailableSlotsAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    pass
