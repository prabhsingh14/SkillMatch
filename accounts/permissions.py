from rest_framework.permissions import BasePermission

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_candidate()

class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_company()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()
