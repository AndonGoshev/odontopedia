from django.shortcuts import render
from django.views.generic import TemplateView
from urllib3 import request

from odontopedia.bookings.models import Booking, MeetingRoom, TuitionFocusArea


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_bookings = Booking.objects.filter(student=user)

        completed_tuitions = user_bookings.filter(session_completed=True)
        upcoming_tuitions = user_bookings.filter(session_completed=False)
        meeting_room = MeetingRoom.objects.first()

        tuition_focus_area_options = TuitionFocusArea.objects.all()

        context['completed_tuitions'] = completed_tuitions
        context['upcoming_tuitions'] = upcoming_tuitions
        context['meeting_room'] = meeting_room.room_link
        context['tuition_focus_area_options'] = tuition_focus_area_options

        return context