from django.contrib.auth.forms import UserCreationForm
from .models import Users


class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration.
    Extends Django's built-in UserCreationForm but uses the custom Users model.
    """

    class Meta:
        model = Users
        fields = (
            "username",  # Username for login
            "email",  # Email address of the user
            "password1",  # First password entry
            "password2",  # Confirmation password entry
        )
