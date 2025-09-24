from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsCompanyOwnerOrAdmin(BasePermission):
    """
    For actions that should be allowed to: company.owner OR site admin (role == 'admin') OR superuser.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "is_superuser", False):
            return True
        if getattr(user, "role", None) == "admin":
            return True
        if hasattr(obj, "owner") and obj.owner == user:
            return True
        if hasattr(obj, "company") and getattr(obj, "company").owner == user:
            return True
        return False


class IsApplicantOrCompanyAdmin(BasePermission):
    """
    Allow applicants to see their own application; company owner or admin can view applications for their company.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if obj.applicant == user:
            return True
        if getattr(user, "is_superuser", False):
            return True
        if getattr(user, "role", None) == "admin":
            return True
        # if user is company owner for the job
        if hasattr(obj.job, "company") and obj.job.company.owner == user:
            return True
        return False
