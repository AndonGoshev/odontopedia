from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from odontopedia import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('odontopedia.common.urls')),
    path('accounts/', include('odontopedia.accounts.urls')),
    path('dashboard/', include('odontopedia.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)