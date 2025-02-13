from django.urls import path

from odontopedia.dashboard.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')
]
