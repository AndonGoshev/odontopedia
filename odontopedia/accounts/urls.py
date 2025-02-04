from django.urls import path

from odontopedia.accounts.views import RegistrationView, CustomLoginView, CustomLogoutView, AuthGoogle, \
    CustomPasswordChangeView, CustomPasswordChangeDoneView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('auth-receiver/', AuthGoogle.as_view(), name='auth-receiver'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password-change-done' ),
]