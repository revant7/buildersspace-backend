from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import base64
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
)


class IsTokenAuthenticated(permissions.BasePermission):
    """
    Permission class to check for valid JWT tokens.
    """

    def has_permission(self, request, view):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        # if not auth_header:
        #     return True  # allow if no auth header

        try:
            auth_type, auth_data = auth_header.split(" ", 1)

            if auth_type.lower() == "basic":
                # Basic Authentication Logic
                client_id = settings.CLIENT_CREDENTIALS["client_id"]
                client_secret = settings.CLIENT_CREDENTIALS["client_secret"]

                decoded_auth = base64.b64decode(auth_data).decode("utf-8")
                provided_client_id, provided_client_secret = decoded_auth.split(":", 1)

                if (
                    provided_client_id == client_id
                    and provided_client_secret == client_secret
                ):
                    return True
                else:
                    return False

            elif auth_type.lower() == "bearer":
                # Bearer Token Authentication Logic
                try:
                    JWTAuthentication().authenticate(request)
                    return True
                except AuthenticationFailed:
                    return False
                except:
                    return False

            else:
                return False

        except (ValueError, IndexError, base64.binascii.Error):
            return False
