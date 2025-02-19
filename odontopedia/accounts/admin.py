from django.contrib import admin

from odontopedia.accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
