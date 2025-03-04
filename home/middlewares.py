from django.http import HttpResponseForbidden
from django.conf import settings
import base64


class ClientCredentialsOrBearerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/api/"):
            auth_header = request.META.get("HTTP_AUTHORIZATION")
            if not auth_header:
                return HttpResponseForbidden(
                    "Client Credentials Are Not Provided. Request Aborted."
                )

            try:
                auth_type, auth_data = auth_header.split(" ", 1)
                if auth_type.lower() == "basic":
                    client_id = settings.CLIENT_CREDENTIALS["client_id"]
                    client_secret = settings.CLIENT_CREDENTIALS["client_secret"]

                    decoded_auth = base64.b64decode(auth_data).decode("utf-8")
                    provided_client_id, provided_client_secret = decoded_auth.split(
                        ":", 1
                    )

                    if (
                        provided_client_id == client_id
                        and provided_client_secret == client_secret
                    ):
                        response = self.get_response(request)
                        return response
                    else:
                        return HttpResponseForbidden("Invalid client credentials.")

                elif auth_type.lower() == "bearer":
                    # Bearer Token Authentication Logic (example, replace with your logic)
                    # Here you would validate the bearer token.
                    # Example, if you are using simplejwt.
                    from rest_framework_simplejwt.authentication import (
                        JWTAuthentication,
                    )

                    try:
                        JWTAuthentication().authenticate(request)
                        return self.get_response(request)
                    except:
                        return HttpResponseForbidden("Invalid bearer token.")

                else:
                    return HttpResponseForbidden("Unsupported authorization type.")

            except (ValueError, IndexError, base64.binascii.Error):
                return HttpResponseForbidden("Invalid authorization header format.")

        else:
            return self.get_response(request)
