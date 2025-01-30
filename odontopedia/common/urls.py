from django.urls import path

from odontopedia.common.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]