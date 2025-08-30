"""
Admin Site Configuration for the 'users' app.

This file defines how the models from the 'users' app (like Users and Address)
are displayed and managed in the Django admin interface. We customize the
default behavior to create a more intuitive and powerful admin experience.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import StackedInline
from .models import Users, Address, TokenProxy
from rest_framework.authtoken.models import Token


@admin.register(TokenProxy)
class TokenProxyAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created")
    search_fields = ("user__username",)


class TokenInline(StackedInline):
    model = Token
    can_delete = False
    verbose_name_plural = "Auth Token"


@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin configuration for the Users model.

    This class extends the default UserAdmin to display our custom fields
    (like 'role', 'bio', 'profile_image') in the user's detail view. It also
    customizes the columns shown in the main user list for better readability.
    """

    # Define the fields to be displayed in the form for editing a user.
    # We start with the default fields from UserAdmin and add a new section
    # for our custom profile information.
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile Info",
            {"fields": ("role", "phone", "profile_image", "bio", "slug")},
        ),
    )

    # Define the columns to be displayed in the list view of all users.
    # This provides a quick overview of the most important user information.
    list_display = ("username", "email", "name", "role", "is_staff", "is_active")

    # Add filters to the right sidebar for easier data navigation.
    # This allows admins to quickly filter users by their status or role.
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "role")

    # Add a search bar to search for users by these fields.
    search_fields = ("username", "name", "email")
    inlines = [TokenInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Address model.

    This class defines how user addresses are displayed. It includes a search
    bar and filters to make it easy for an admin to find and manage addresses.
    """

    # Define the columns to be displayed in the list view of all addresses.
    list_display = ("user", "street", "city", "country", "is_default")

    # Add filters to the right sidebar.
    list_filter = ("is_default", "city", "country")

    # Add a search bar to search for addresses.
    # The '__' syntax allows searching through related models.
    search_fields = ("user__username", "street", "city", "postal_code")


if admin.site.is_registered(Token):
    admin.site.unregister(Token)
