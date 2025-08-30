from rest_framework import viewsets, permissions
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

# Local imports from our app
from .models import Category
from .serializers import CategorySerializer
from .forms import CategoryForm


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing categories.

    - Provides default CRUD operations: GET, POST, PUT, PATCH, DELETE.
    - Uses CategorySerializer for data serialization (JSON ⇆ Python).
    - Uses 'slug' instead of 'id' for URL lookups.
    - Read-only access for anonymous users.
    - Full access (create, update, delete) for authenticated users.
    """

    queryset = Category.objects.all().order_by("-created_at")
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # Only authenticated users can modify
    lookup_field = "slug"  # Example: /api/categories/tech/


class CategoryListView(ListView):
    """
    View to display a list of all categories.

    - Uses template: categories/category_list.html
    - Provides the context variable 'categories'.
    """

    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    """
    View to display details of a single category.

    - Uses template: categories/category_detail.html
    - Fetches the category by 'slug' from the URL.
    - Provides the context variable 'category'.
    """

    model = Category
    template_name = "categories/category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "slug"


class CategoryCreateView(CreateView):
    """
    View to create a new category.

    - Uses CategoryForm for the form.
    - On success, redirects to the category list.
    - Provides extra context: 'page_title' for the template.
    """

    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create a New Category"
        return context


class CategoryUpdateView(UpdateView):
    """
    View to update an existing category.

    - Uses CategoryForm for the form.
    - Fetches the category by 'slug'.
    - On success, redirects to the detail page of the updated category.
    - Provides extra context: 'page_title' with the category name.
    """

    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit {self.object.name}"
        return context

    def get_success_url(self):
        return reverse_lazy("category-detail", kwargs={"slug": self.object.slug})


class CategoryDeleteView(DeleteView):
    """
    View to confirm and delete a category.

    - Uses template: categories/category_confirm_delete.html
    - Fetches the category by 'slug'.
    - On success, redirects to the category list.
    - Provides the context variable 'category'.
    """

    model = Category
    template_name = "categories/category_confirm_delete.html"
    slug_url_kwarg = "slug"
    context_object_name = "category"
    success_url = reverse_lazy("category-list")
