from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from django.shortcuts import redirect
from .serializers import (
    JobSerializer,
    UserSerializer,
    CompanySerializer,
    JobCreateSerializer,
    JobApplicationSerializer,
    JobApplicationUpdateSerializer,
    FavoriteSerializer,
)
from .models import Job, CustomUser, JobApplication, Favorite, Company
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminUserRole, IsCompanyOwnerOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import models
from drf_spectacular.utils import extend_schema
from .filters import JobFilter


class TenPerPagePagination(PageNumberPagination):
    page_size = 10


# Create your views here.


# Root view
@extend_schema(
    tags=["root"],
)
class RootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "message": "Welcome to Jobs Board API",
                "version": "v0.0.1",
                "description": """Jobs can be viewed publicly and once logged in, only admins can post jobs, view applications to their companies, and update the status of an applicant's application. The superadmin is the one who can create an admin for a company.""",
                "endpoints": {
                    "admin_panel": "/admin/",
                    "login": "/api/login/",
                    "register": "/api/register/",
                    "docs": "/api/docs/",
                    "jobs": "/api/jobs/",
                    "applications": "/api/applications/",
                    "favorites": "/api/favorites/",
                    "companies": "/api/companies/",
                    "users": "/api/users/",
                    "swagger": "/api/schema/",
                    "redoc": "/api/schema/redoc/",
                },
            }
        )


@extend_schema(
    tags=["companies"],
)
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().select_related("owner")
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "website"]
    ordering_fields = ["name", "created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsCompanyOwnerOrAdmin()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(
    tags=["jobs"],
)
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related("company", "posted_by")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = JobFilter
    search_fields = [
        "title",
        "description",
        "company__name",
        "location",
        "posted_by__email",
        "category",
    ]
    ordering_fields = ["title", "created_at", "salary", "min_experience_years"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return JobCreateSerializer
        return JobSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsCompanyOwnerOrAdmin()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsCompanyOwnerOrAdmin()]
        return [AllowAny()]

    def perform_create(self, serializer):
        company = serializer.validated_data.get("company")
        user = self.request.user
        if not (company.owner == user or user.role == "admin"):
            raise PermissionDenied(
                "You must be the company owner or admin to create a job"
            )
        serializer.save(posted_by=self.request.user)


@extend_schema(
    tags=["applications"],
    request={"multipart/form-data": JobApplicationSerializer},
    responses={
        201: JobApplicationSerializer,
    },
)
class JobApplicationViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = JobApplication.objects.select_related("job", "applicant")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["job__id", "status", "applicant__id", "job__company__id"]
    search_fields = ["job__title", "applicant__email"]
    ordering_fields = ["created_at"]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return JobApplicationUpdateSerializer
        return JobApplicationSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ("update", "partial_update", "destroy"):
            return [IsAuthenticated()]
        if self.action == ("list", "retrieve"):
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return JobApplication.objects.none()

        # Superuser or admin -> see all applications
        if user.is_superuser or getattr(user, "role", None) == "admin":
            return JobApplication.objects.all()

        company_ids = user.companies.values_list("id", flat=True)
        return JobApplication.objects.filter(
            models.Q(applicant=user) | models.Q(job__company__in=company_ids)
        )

    def perform_create(self, serializer):
        job = serializer.validated_data["job"]
        user = self.request.user
        if not job.is_active:
            raise ValidationError("Job is not active")
        serializer.save(applicant=user)


@extend_schema(
    tags=["favorites"],
)
class FavoriteViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.select_related("job", "user").all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["job__id", "user__id"]
    search_fields = ["job__title", "job__company__name", "user__email"]

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    tags=["users"],
)
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUserRole]


@extend_schema(tags=["users"])
class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
