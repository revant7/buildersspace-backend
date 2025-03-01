from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView,
)

urlpatterns = [
    # account-creation endpoints
    path(
        "create-user-account/",
        views.register_user,
        name="create_attendee_account",
    ),
    # account-verification-endpoints
    path(
        "user-login/", views.custom_token_obtain_view, name="custom_token_obtain_view"
    ),  # gives the access token and refresh token
    path(
        "verify-token/", TokenVerifyView.as_view(), name="token_verify"
    ),  # Verifies if an access token is still valid
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Takes a refresh token and returns a new access token
    path(
        "token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"
    ),  # Revokes a Refresh Token
]
