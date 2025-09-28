from django.urls import path, include
from .views import (
    UserListView,
    RegisterUserView,
    JobViewSet,
    CompanyViewSet,
    FavoriteViewSet,
    JobApplicationViewSet,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .serializers import CustomerTokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"jobs", JobViewSet, basename="jobs")
router.register(r"applications", JobApplicationViewSet, basename="applications")
router.register(r"favorites", FavoriteViewSet, basename="favorites")


urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", CustomerTokenObtainPairView.as_view(), name="login"),
    path("", include(router.urls)),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
