from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import JobSerializer, UserSerializer
from rest_framework.response import Response
from .models import Job, CustomUser
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminUserRole


class TenPerPagePagination(PageNumberPagination):
    page_size = 10


# Create your views here.
class JobListView(generics.ListAPIView):
    queryset = Job.objects.filter(is_active=True).order_by("-created_at")
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    pagination_class = TenPerPagePagination


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"


class JobCreateView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    lookup_field = "pk"


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUserRole]


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
