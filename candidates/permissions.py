from rest_framework.permissions import BasePermission

class IsCandidate(BasePermission):
    """
    Allows access only to users with role='candidate'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "candidate"
