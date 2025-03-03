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
    # PATCH Requests For Updating Data
    path("update-user/", views.update_user, name="update_user"),  # update_user details
    path(
        "update-participant/", views.update_participant, name="update_participant"
    ),  # update_participant details
    path(
        "update-project/", views.update_project, name="update_project"
    ),  # update_project details
    path(
        "update-social-links/",
        views.update_social_links,
        name="update_social_links",
    ),  # update_social_links
    path(
        "update-participant-notification/",
        views.update_participant_notification,
        name="update_participant_notification",
    ),  # update_participant_notification
    # Endpoint for getting all details
    path(
        "get-user-details/",
        views.get_user_details,
        name="get_user_details",
    ),  # getting all user details
    # Endpoint for editing any/all details
    path(
        "update-all-details/",
        views.update_all_details,
        name="update_all_details",
    ),
    # Endpoint for casting the attendee's Vote
    path(
        "cast-attendee-vote/", views.cast_vote, name="cast_vote"
    ),  # casting the attendee's Vote
    # Endpoint for doing like
    path("post-like/", views.do_like, name="do_like"),  # doing like
    # Endpoint for getting vote count for all projects
    path(
        "get-vote-count-for-all-projects/",
        views.get_vote_count_for_all_projects,
        name="get_vote_count_for_all_projects",
    ),  # getting vote count for all projects
    # Endpoint for getting like count for all projects
    path(
        "get-like-count-for-all-projects/",
        views.get_like_count_for_all_projects,
        name="get_like_count_for_all_projects",
    ),  # getting like count for all projects
]
