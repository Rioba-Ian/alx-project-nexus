from django.urls import path
from .views import (
    JobListView,
    UserListView,
    RegisterUserView,
    JobCreateView,
    JobDetailView,
    JobUpdateView,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .serializers import CustomerTokenObtainPairView
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="jobs/"), name="root"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", CustomerTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("jobs/", JobListView.as_view(), name="job-list"),
    path("jobs/create/", JobCreateView.as_view(), name="job-create"),
    path("jobs/<int:pk>/", JobUpdateView.as_view(), name="job-update-delete"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("users/", UserListView.as_view(), name="user-list"),
]
