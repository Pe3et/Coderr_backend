from rest_framework import permissions

from auth_app.api.models import UserProfile


class IsBusinessOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            userProfile = UserProfile.objects.get(user=request.user)
            if userProfile.type == 'business' or request.user.is_superuser:
                return True
        else:
            return False