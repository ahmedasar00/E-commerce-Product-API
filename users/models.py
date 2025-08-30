from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    Group,
    Permission,
)  # Import Group and Permission
from django.utils.text import slugify
from rest_framework.authtoken.models import Token


class Users(AbstractUser):
    """
    A custom user model that extends Django's default AbstractUser.
    """

    class Roles(models.TextChoices):
        """
        Defines the roles available for users in the system.
        """

        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        SELLER = "SELLER", "Seller"

    # --- Additional Fields ---

    """
    The user's full name. This field was added to resolve a SystemCheckError
    (admin.E108) because it was being referenced in the 'list_display'
    of the CustomUserAdmin class in 'admin.py' but did not exist here.
    """
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=50, choices=Roles.choices, default=Roles.CUSTOMER
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    password_reset_code = models.CharField(max_length=10, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    password_changed_at = models.DateTimeField(blank=True, null=True)

    # --- FIX FOR THE ERROR ---
    # Add related_name to avoid clashes with the default User model

    """
    A many-to-many relationship to the Group model. This field is inherited
    from Django's AbstractUser but overridden here to add a custom
    `related_name`. This is crucial to prevent clashes with the default
    `auth.User` model when Django builds its reverse relationships.
    """
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="custom_user_set",  # Custom related_name
        related_query_name="user",
    )
    """
    A many-to-many relationship to the Permission model. Similar to the
    `groups` field, this is overridden to provide a unique `related_name`
    (`custom_user_permissions_set`), which resolves system check errors
    (E304) by avoiding conflicts with the default `auth.User` model.
    """

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_permissions_set",  # Custom related_name
        related_query_name="user",
    )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to auto-generate a slug from the
        username if one is not already present.
        """
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the username as the string representation of the object.
        This is what you see in the Django admin panel.
        """
        return self.username


# Note: The Address model remains the same. No changes are needed there.
class Address(models.Model):
    """
    Stores shipping addresses for users. Each user can have multiple addresses.
    """

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        """
        Meta options for the Address model. Ensures a user can only have one
        default address.
        """

        constraints = [
            models.UniqueConstraint(
                fields=["user", "is_default"],
                condition=models.Q(is_default=True),
                name="unique_default_address",
            )
        ]

    def __str__(self):
        """
        Returns a full string representation of the address for display.
        """
        return f"{self.street}, {self.city}, {self.country} - ({self.user.username})"


class TokenProxy(Token):
    class Meta:
        proxy = True
        verbose_name = "User Token"
        verbose_name_plural = "User Tokens"
