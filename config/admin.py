from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Role", {"fields": ("role",)}),)
