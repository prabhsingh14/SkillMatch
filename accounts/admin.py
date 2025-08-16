from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "phone", "role", "is_active", "is_staff", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "phone")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "phone", "password", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone", "role", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )

# Registering models
admin.site.register(CustomUser, CustomUserAdmin)