from rest_framework.permissions import BasePermission


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['viewer', 'analyst', 'admin']


class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['analyst', 'admin']


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'