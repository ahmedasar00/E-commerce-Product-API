from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Category Name"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description", "rows": 3}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
