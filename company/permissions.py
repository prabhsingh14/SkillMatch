from rest_framework import permissions

class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "employer")

class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Employers can create/update/delete.
    Candidates/others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user.is_authenticated and hasattr(request.user, "employer")
