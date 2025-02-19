import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from odontopedia.bookings.models import AvailableSlot, Booking, MeetingRoom


class AvailableSlotsJSONView(View):
    def get(self, request):
        slots = AvailableSlot.objects.filter(is_booked=False,).order_by('date', 'time')

        slots_list = []
        for slot in slots:
            slots_list.append({
                'id': slot.id,
                'date': slot.date,
                'time': slot.time,
            })

        return JsonResponse({
            'available_slots': slots_list
        })

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class BookSlotJSONView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            slot_id = data.get('slot_id')
            booking_date = data.get('date')
            booking_time = data.get('time')
            focus_area = data.get('focus_area')
            description = data.get('description')
            if not slot_id:
                return JsonResponse({'error': 'Slot ID is required'}, status=400)

            slot = AvailableSlot.objects.get(id=slot_id, is_booked=False)

        except AvailableSlot.DoesNotExist:
            return JsonResponse({'error': 'Slot not available'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        booking = Booking.objects.create(student=request.user, slot=slot, date=booking_date, time=booking_time, focus_area=focus_area, description=description)

        slot.is_booked = True
        slot.save()
        self.request.user.number_of_tuitions -= 1
        self.request.user.save()

        meeting_room = MeetingRoom.objects.first()
        room_link = meeting_room.room_link if meeting_room else 'no meeting room model'

        return JsonResponse({
            'message': 'Booking successful',
            'booking': {
                'slot_id': slot.id,
                'date': slot.date,
                'time': slot.time,
                'room_link': room_link,
            }
        })







