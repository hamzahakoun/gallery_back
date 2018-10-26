from rest_framework import permissions
from comments.models import Comment

class UserIsOnwer(permissions.BasePermission) :

    def has_object_permission(self, request, view,obj):
        if view.action in ['update','destroy'] :
            return obj.is_user_owner(request.user)
        return True
