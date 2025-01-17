from rest_framework.permissions import BasePermission, SAFE_METHODS

# IsAdminUser: Grants access only to Admin users
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

# IsModeratorOrAdmin: Grants access to Moderators or Admins
class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["moderator", "admin"]

# IsOwnerOrReadOnly: Allows only the owner to modify; read-only for others
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.created_by == request.user or obj.author == request.user

# IsRegularUser: Grants access to logged-in users with role "user"
class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "user"
