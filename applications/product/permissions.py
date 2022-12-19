from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    # creating, listing
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    # retrieving, updating, deleting
    def has_object_permission(self, request, view, obj):
        print(request.user.is_authenticated)
        print(request.method)
        print(SAFE_METHODS)
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user == obj.owner or request.user.is_stuff)


class IsCommentOwner(BasePermission):
    # creating, listing
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # retrieving, updating, deleting
    def has_object_permission(self, request, view, obj):
        if request.methood in ['PUT', 'PATH']:
            return request.user.is_authenticated and request.user == obj.owner
        return request.user.is_authenticated and (request.user == obj.owner or request.user.is_stuff)