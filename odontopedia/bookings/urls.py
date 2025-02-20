from django.urls import path

from odontopedia.bookings.views import AvailableSlotsJSONView, BookSlotJSONView, CancelBookingView

urlpatterns = [
    path('available-slots/', AvailableSlotsJSONView.as_view(), name='available-slots'),
    path('book-slot/', BookSlotJSONView.as_view(), name='book-slot'),
    path('cancel-tuition/', CancelBookingView.as_view(), name='cancel-tuition'),
]