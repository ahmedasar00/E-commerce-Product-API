# products/views.py

from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from .forms import ProductForm  # <-- استيراد الفورم الجديد

# --- Django Generic Views for Templates ---
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy


# ===============================================
# API VIEWS (باستخدام ViewSet) - هذا الكود موجود لديك بالفعل
# ===============================================
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for products.
    """

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# =======================================================
# TEMPLATE VIEWS (باستخدام Class-Based Views) - أضف هذا الجزء
# =======================================================


class ProductListView(ListView):
    """View to display a list of all products."""

    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 10  # Optional: for pagination


class ProductDetailView(DetailView):
    """View to display the details of a single product."""

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """View to handle the creation of a new product."""

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy(
        "product-list"
    )  # Redirect to the product list after creation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add New Product"
        return context


class ProductUpdateView(UpdateView):
    """View to handle editing an existing product."""

    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("product-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Edit {self.object.name}"
        return context


class ProductDeleteView(DeleteView):
    """View to confirm and handle the deletion of a product."""

    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("product-list")
    context_object_name = "product"
