from rest_framework.permissions import SAFE_METHODS, BasePermission


class SalesManPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 5) or request.user.is_staff


class IsOwnerOrStaffOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff


class IsOwnerProductOrStaffPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.product.user == request.user or request.user.is_staff
