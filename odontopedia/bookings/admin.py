from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import admin_actions
from django.utils.timezone import now
from datetime import date as date, timedelta

from odontopedia.bookings.models import Booking, AvailableSlot, MeetingRoom


class ExpiredSlotsFilter(admin.SimpleListFilter):
    title = "Expired Slots"  # Filter title in admin
    parameter_name = "expired_slots"  # Query parameter in URL

    def lookups(self, request, model_admin):
        """Defines filter options"""
        return [
            ("expired", "Expired & Unbooked"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "expired":
            yesterday = now().date() - timedelta(days=1)
            print("Yesterday's date:", yesterday)  # Debugging line
            filtered_queryset = queryset.filter(is_booked=False, date__lte=yesterday)  # <= yesterday

            # Print the final queryset to debug
            print(filtered_queryset.query)  # This will show the SQL query generated

            return filtered_queryset
        return queryset

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass


@admin.register(AvailableSlot)
class AvailableSlotsAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'is_booked']
    list_filter = [ExpiredSlotsFilter, ]



@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    pass
