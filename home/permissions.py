from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)


class IsTokenAuthenticated(permissions.BasePermission):
    """
    Permission class to check for valid JWT tokens.
    """

    def has_permission(self, request, view):
        try:
            JWTAuthentication().authenticate(
                request
            )  # authenticate the request with the jwt token based authentication.
            return True
        except AuthenticationFailed:
            return False
        except:
            return False
