from rest_framework.permissions import BasePermission
from . import views

class CustomPermission(BasePermission):

    def has_permission(self, req, view):
        if req.user.is_authenticated and req.META['REMOTE_ADDR'] == '127.0.0.1':
            return True
        else:
            return False
