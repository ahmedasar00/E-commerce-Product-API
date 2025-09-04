# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Address


class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for user registration that includes role selection.
    Users can register as either a Customer or a Seller.
    The Admin role is excluded for security reasons.
    """

    # Add a new field for role selection
    role = forms.ChoiceField(
        choices=[
            (Users.Roles.CUSTOMER, "Register as a Customer"),
            (Users.Roles.SELLER, "Register as a Seller"),
        ],
        required=True,
        label="Account Type",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta(UserCreationForm.Meta):
        model = Users
        # Add the 'role' field to the list of fields to be displayed and saved
        fields = ("username", "email", "role")


class AddressForm(forms.ModelForm):
    """
    A form for creating and updating user addresses.
    """

    class Meta:
        model = Address
        # We exclude 'user' because it will be set automatically in the view
        # We exclude 'is_default' for simplicity now, can be added later
        fields = ["street", "city", "state", "country", "postal_code"]

    def __init__(self, *args, **kwargs):
        """
        Add Bootstrap classes to form fields.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
