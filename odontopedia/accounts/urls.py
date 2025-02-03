from django.urls import path

from odontopedia.accounts.views import RegistrationView, CustomLoginView, CustomLogoutView, AuthGoogle

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('auth-receiver/', AuthGoogle.as_view(), name='auth-receiver'),
]