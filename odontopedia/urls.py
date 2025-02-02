

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('odontopedia.common.urls')),
    path('accounts/', include('odontopedia.accounts.urls')),
]
