from django.contrib import admin
from .models import CustomUser, Company, Job, JobApplication, Favorite
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Role", {"fields": ("role",)}),)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "website", "owner", "created_at")
    search_fields = ("name", "description", "website")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "company",
        "location",
        "posted_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    search_fields = (
        "title",
        "description",
        "company__name",
        "location",
        "posted_by__email",
    )
    list_filter = ("is_active", "company")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("job__title", "applicant__email")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "created_at")
    search_fields = ("user__email", "job__title")
