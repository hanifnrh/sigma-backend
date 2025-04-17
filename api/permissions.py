from rest_framework.permissions import BasePermission
from .models import Alat
class IsAlat(BasePermission):
    #allows access only to users with the 'alat' role

    def has_permission(self, request, view):
        return isinstance(request.user, Alat)
        


