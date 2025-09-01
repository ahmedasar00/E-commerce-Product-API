from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    This permission grants read-only access to any user (authenticated
    or not), but write access (like updating or deleting) is restricted
    to the user who created the review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to interact with the given object.

        - If the request method is safe (GET, HEAD, OPTIONS), permission is granted.
        - Otherwise, permission is only granted if the request user is the same
          as the user who owns the review object.
        """
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the review.
        return obj.user == request.user
