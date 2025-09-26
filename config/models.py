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


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(
        "config.CustomUser",
        on_delete=models.CASCADE,
        related_name="companies",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ExperienceLevel(models.TextChoices):
    INTERN = "intern", "Intern"
    ENTRY = "entry", "Entry Level"
    MID = "mid", "Mid Level"
    SENIOR = "senior", "Senior"
    LEAD = "lead", "Lead"


class JobMode(models.TextChoices):
    REMOTE = "remote", "Remote"
    ONSITE = "onsite", "Onsite"
    HYBRID = "hybrid", "Hybrid"
    FULLTIME = "full-time", "Full-time"
    CONTRACT = "contract", "Contract"
    PARTTIME = "part-time", "Part-time"


class Currency(models.TextChoices):
    USD = "USD", "USD"
    KES = "KES", "KES"
    NGN = "NGN", "NGN"


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="jobs"
    )
    is_active = models.BooleanField(default=True)
    experience = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        blank=True,
        null=True,
    )
    min_experience_years = models.IntegerField(blank=True, null=True)
    max_experience_years = models.IntegerField(blank=True, null=True)
    mode = models.CharField(
        max_length=20,
        choices=JobMode.choices,
        blank=True,
        null=True,
    )
    salary = models.PositiveIntegerField(blank=True, null=True)
    salary_currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        blank=True,
        null=True,
    )
    category = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.company.name}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("review", "Under Review"),
        ("interview", "Interview"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    applicant = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="applications"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="applied",
    )
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.job.title} - {self.applicant.email}"


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="favorites"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"
