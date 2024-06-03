from rest_framework.permissions import BasePermission
from .models import LogicUser
    
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        user = LogicUser.get_user(request = request)
        print(user)
        if user:
            if user.is_staff:
                return True
        return False