from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import admin_actions
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.utils.timezone import now
from datetime import date as date, timedelta, datetime

from odontopedia.bookings.forms import BulkPredefinedSlotForm
from odontopedia.bookings.models import Booking, Slot, MeetingRoom


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


@admin.register(Slot)
class SlotsAdmin(admin.ModelAdmin):
    change_list_template = "admin/bookings/slot/change_list.html"
    list_display = ['date', 'time', 'is_booked']
    list_filter = [ExpiredSlotsFilter, ]


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-predefined/', self.admin_site.admin_view(self.bulk_predefined_slots_view), name='bulk_predefined_slots'),
        ]
        return custom_urls + urls

    def bulk_predefined_slots_view(self, request):
        form = BulkPredefinedSlotForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            predefined_times = ["08:00", "10:30", "13:00", "15:30", "18:00"]
            created_count = 0
            skipped_count = 0

            current_date = start_date
            while current_date <= end_date:
                # Check if slots already exist for this day
                if Slot.objects.filter(date=current_date).exists():
                    skipped_count += 1
                else:
                    for time_str in predefined_times:
                        time_obj = datetime.strptime(time_str, "%H:%M").time()
                        Slot.objects.create(date=current_date, time=time_obj)
                        created_count += 1
                current_date += timedelta(days=1)

            self.message_user(request, f"{created_count} slot(s) created, {skipped_count} day(s) skipped.")
            return redirect(reverse('admin:bookings_slot_changelist'))

        context = dict(
            self.admin_site.each_context(request),
            form=form,
            title="Bulk Create Predefined Slots",
        )
        return TemplateResponse(request, "admin/bulk_predefined_slots.html", context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_create_url'] = reverse('admin:bulk_predefined_slots')
        return super().changelist_view(request, extra_context=extra_context)



@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    pass
