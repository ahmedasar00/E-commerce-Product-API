from django.urls import path
from .views import register_view, login_view, logout_view, profile_view

"""
URL patterns for user authentication.
Includes routes for register, login, logout, and profile.
"""

urlpatterns = [
    path("register/", register_view, name="register"),  # User registration
    path("login/", login_view, name="login"),  # User login
    path("logout/", logout_view, name="logout"),  # User logout
    path("profile/", profile_view, name="profile"),  # User profile page
]
