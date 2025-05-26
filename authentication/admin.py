from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'age', "id")
    fieldsets = UserAdmin.fieldsets + (
        ('RGPD', {'fields': ('age', 'can_data_be_shared', 'can_be_contacted')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)