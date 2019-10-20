from rest_framework import permissions

class IsSlotModificationAllowed(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        print(request.data)
        if hasattr(request.data, 'is_locked'):
            if obj.is_empty:
                self.message('You can not lock an empty slot')

        return True