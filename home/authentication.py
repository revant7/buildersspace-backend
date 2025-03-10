from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from home.models import User  # Import your custom User model


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Override the default method to fetch the user from our custom User model.
        """
        try:
            email = validated_token["email"]  # JWT uses "user_id" by default
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")
