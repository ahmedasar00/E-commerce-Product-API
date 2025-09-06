from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from .forms import ProductForm

# --- Django Generic Views for Templates ---
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products.
    Provides CRUD operations via REST API.
    """

    queryset = Product.objects.all().order_by("-created_at")  # Latest products first
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Authenticated users can create/update, others can only read


class ProductListView(ListView):
    """
    Display a list of all products (HTML page).
    """

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10  # Show 10 products per page


class ProductDetailView(DetailView):
    """
    Display details of a single product.
    """

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """
    Handle the creation of a new product (form + save).
    """

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")
    # Redirect to product list after creation

    def get_context_data(self, **kwargs):
        """
        Add custom context data for the template (page title).
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add New Product"
        return context


class ProductUpdateView(UpdateView):
    """
    Handle editing an existing product.
    """

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product_list")

    def get_context_data(self, **kwargs):
        """
        Add custom context data (page title with product name).
        """
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit {self.object.name}"
        return context


class ProductDeleteView(DeleteView):
    """
    Confirm and handle the deletion of a product.
    """

    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
    context_object_name = "product"
