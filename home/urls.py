from django.urls import path
import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenVerifyView,
)

urlpatterns = [
    # account-creation endpoints
    path(
        "create-attendee-account/",
        views.create_attendee_account,
        name="create_attendee_account",
    ),
    path(
        "create-participant-account/",
        views.create_participant_account,
        name="create_participant_account",
    ),
    # account-verification-endpoints
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("verify-token/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # getting-new-products
    path("fetch-products/", views.fetch_products, name="products"),
    # rendering-products-endpoint
    path("get-products/", views.get_products, name="products"),
]
