from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product objects.
    Uses Bootstrap classes for better styling in templates.
    """

    class Meta:
        model = Product
        fields = ["name", "price", "stack", "category", "description", "image"]

        # Customize form fields with widgets for styling
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # Text field for product name
            "price": forms.NumberInput(
                attrs={"class": "form-control"}
            ),  # Numeric field for product price
            "stack": forms.NumberInput(
                attrs={"class": "form-control"}
            ),  # Numeric field for product stock
            "category": forms.Select(
                attrs={"class": "form-select"}
            ),  # Dropdown for product category
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),  # Multi-line text
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),  # Upload product image
        }
