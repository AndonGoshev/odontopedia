from django.urls import path
from django.contrib.auth import views as auth_views

from odontopedia.accounts.views import RegistrationView, CustomLoginView, CustomLogoutView, AuthGoogle, \
    CustomPasswordChangeView, CustomPasswordChangeDoneView, CustomPasswordResetView, CustomPasswordResetDoneView, \
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, UserProfileUpdateView, AccountDeleteView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('account-settings/', UserProfileUpdateView.as_view(), name='account-settings'),
    path('auth-receiver/', AuthGoogle.as_view(), name='auth-receiver'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password-change'),
    path('password-change-done/', CustomPasswordChangeDoneView.as_view(), name='password-change-done'),
    path('password-reset/', CustomPasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('<int:id>/delete-account', AccountDeleteView.as_view(), name='delete-account'),
]
