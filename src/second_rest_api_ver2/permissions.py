from rest_framework.permissions import BasePermission
from . import views

class CustomPermission(BasePermission):

    def has_permission(self, req, view):
        if req.user.is_authenticated and req.META['REMOTE_ADDR'] == '127.0.0.1':
            return True
        else:
            return False


class ProductPermission(BasePermission):

    def has_object_permission(self, req, view, obj):
        if req.method not in ['GET', 'HEAD', 'OPTIONS']:
            return obj.user == req.user
        return super().has_object_permission(req, view, obj) # True となる
