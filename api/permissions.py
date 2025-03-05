from rest_framework.permissions import BasePermission

class IsAlatRole(BasePermission):
    #allows access only to users with the 'alat' role

    def has_permission(self, request, view):

        return request.user.is_authenticated and getattr(request.user, "role", None) == "alat"
    