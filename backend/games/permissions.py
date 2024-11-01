from rest_framework import permissions

class IsAdminDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff or request.user.is_authenticated and request.user.username == obj.admin.username
        else:
            return True

class IsInGameDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user in obj.users.all()
        else:
            return True