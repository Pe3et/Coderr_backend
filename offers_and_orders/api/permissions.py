from rest_framework import permissions

from auth_app.api.models import UserProfile


class IsBusinessAndOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            userProfile = UserProfile.objects.get(user=request.user)
            if userProfile.type == 'business' or request.user.is_superuser:
                return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser
    

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            userProfile = UserProfile.objects.get(user=request.user)
            if userProfile.type == 'customer':
                return True
        else:
            return False or request.user.is_superuser
        
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'customer_user'):
            return obj.customer_user == request.user
        elif hasattr(obj, 'reviewer'):
            return obj.reviewer == request.user
        else:
            return False
        

class IsBusiness(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            userProfile = UserProfile.objects.get(user=request.user)
            if userProfile.type == 'business':
                return True
        else:
            return False or request.user.is_superuser
        
    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
        

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
                return True
        else:
            return False