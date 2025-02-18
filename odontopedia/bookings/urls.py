from django.urls import path

from odontopedia.bookings.views import AvailableSlotsJSONView, BookSlotJSONView

urlpatterns = [
    path('available-slots/', AvailableSlotsJSONView.as_view(), name='available-slots'),
    path('book-slot/', BookSlotJSONView.as_view(), name='book-slot'),
]