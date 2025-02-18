import json

from django.contrib.auth.decorators import login_required
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
            if not slot_id:
                return JsonResponse({'error': 'Slot ID is required'}, status=400)

            slot = AvailableSlot.objects.get(id=slot_id, is_booked=False)

        except AvailableSlot.DoesNotExist:
            return JsonResponse({'error': 'Slot not available'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        booking = Booking.objects.create(student=request.user, slot=slot)

        slot.is_booked = True
        slot.save()

        meeting_room = MeetingRoom.objects.first()
        room_link = meeting_room.room_link

        return JsonResponse({
            'message': 'Booking successful',
            'booking': {
                'slot_id': slot.id,
                'date': slot.date,
                'time': slot.time,
                'room_link': room_link,
            }
        })









