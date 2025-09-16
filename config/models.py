from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_regex = r"^\+?1?\d{9,15}$"
phone_validator = RegexValidator(
    regex=phone_regex,
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(
        max_length=15, blank=True, null=True, validators=[phone_validator]
    )

    USER = "user"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (USER, "User"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="jobs"
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
