from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'auto_reply_enabled')
    list_filter = ('is_staff', 'is_active', 'auto_reply_enabled')
    search_fields = ('email', 'username')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('auto_reply_enabled', 'auto_reply_delay')}),  # Додайте це поле
    )

admin.site.register(CustomUser, CustomUserAdmin)