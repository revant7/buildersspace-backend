from django.http import JsonResponse
from functools import wraps
import os

BUILDERSSPACE_CLIENT_ID = os.environ.get("BUILDERSSPACE_CLIENT_ID")
BUILDERSSPACE_CLIENT_SECRET = os.environ.get("BUILDERSSPACE_CLIENT_SECRET")


def credentials_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        client_id = request.GET.get("CLIENT_ID")
        client_secret = request.GET.get("CLIENT_SECRET")
        print(request.headers)
        print(client_id, "\n", client_secret)
        if (not client_id) or (not client_secret):
            return JsonResponse(
                {"error": "CLIENT_ID OR CLIENT_SECRET IS MISSING"}, status=403
            )

        if (client_id == BUILDERSSPACE_CLIENT_ID) and (
            client_secret == BUILDERSSPACE_CLIENT_SECRET
        ):
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse(
                {"error": "INVALID CLIENT_ID OR CLIENT_SECRET"}, status=403
            )

    return _wrapped_view
