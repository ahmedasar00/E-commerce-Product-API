from users.models import Address


from django.db import transaction
from django.urls import reverse_lazy, reverse  # Import 'reverse' for dynamic URLs
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem

# from users.models import Address
from .serializers import OrderSerializer, OrderCreateSerializer
from .permissions import IsOwnerOrAdmin
from products.models import Product

# -----------------------------------------------------------------------------
# API Views (using Django REST Framework)
# -----------------------------------------------------------------------------


class OrderViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_staff:  # Admin can see all orders
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve", "create"]:
            permission_classes = [IsAuthenticated]
        else:  # For update, partial_update, destroy
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        validated_data = serializer.validated_data

        items_data = validated_data.pop("items")
        address_id = validated_data.pop("address_id")

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError(
                {"address_id": "This address does not exist or does not belong to you."}
            )

        with transaction.atomic():
            total_amount = 0
            order_items_to_create = []

            for item_data in items_data:
                try:
                    product = Product.objects.get(id=item_data["product_id"])
                    price = product.price
                    quantity = item_data["quantity"]

                    if quantity <= 0:
                        raise serializers.ValidationError(
                            "Quantity must be a positive number."
                        )

                    total_amount += price * quantity

                    order_items_to_create.append(
                        OrderItem(
                            product=product,
                            quantity=quantity,
                            price_at_order_time=price,
                        )
                    )
                except Product.DoesNotExist:
                    raise serializers.ValidationError(
                        {
                            "product_id": f"Product with id {item_data['product_id']} does not exist."
                        }
                    )

            order = Order.objects.create(
                user=user,
                address=address,  #
                total_amount=total_amount,
                **validated_data,
            )

            for item in order_items_to_create:
                item.order = order

            OrderItem.objects.bulk_create(order_items_to_create)

            serializer.instance = order


# -----------------------------------------------------------------------------
# Template-Based Views (using standard Django)
# -----------------------------------------------------------------------------


class OrderListView(LoginRequiredMixin, ListView):
    """
    View to display a list of orders for the currently logged-in user.
    Renders an HTML template.
    """

    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        """
        Overrides the default queryset to ensure that users can only see
        their own orders, ordered by the most recent.
        """
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    View to display the details of a specific order.
    Renders an HTML template.
    """

    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        """
        Overrides the default queryset to ensure that a user can only view
        their own orders, preventing access to others' orders via URL guessing.
        """
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new order. After creation, it redirects to the payment page.
    """

    model = Order
    template_name = "orders/order_form.html"
    fields = ["address"]
    # We no longer need a static success_url because we override get_success_url.

    def get_form(self, form_class=None):
        """Ensures the address dropdown only shows the current user's addresses."""
        form = super().get_form(form_class)
        form.fields["address"].queryset = self.request.user.address_set.all()
        return form

    def form_valid(self, form):
        """Sets the user and updates order status before saving."""
        form.instance.user = self.request.user
        # NOTE: In a real app, this should be calculated from a shopping cart.
        form.instance.total_amount = 0
        # === CHANGE 1: Set status to trigger payment flow ===
        form.instance.status = "Pending Payment"
        return super().form_valid(form)

    def get_success_url(self):
        """
        === CHANGE 2: Redirect to the payment page for the new order ===
        This method is called after the form is successfully validated and the order is saved.
        """
        # 'self.object' is the Order instance that was just created.
        return reverse("create_payment", kwargs={"order_id": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create a New Order"
        return context


class OrderCancelView(LoginRequiredMixin, UpdateView):
    """
    View for a user to cancel their own order.
    This is an UpdateView that only allows changing the status to 'Cancelled'.
    """

    model = Order
    template_name = "orders/order_confirm_cancel.html"
    fields = []
    success_url = reverse_lazy("order_list")

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if (
            order.status != "Pending"
        ):  # You might want to allow cancellation if it's 'Pending Payment' too
            return HttpResponseForbidden("This order cannot be cancelled.")

        order.status = "Cancelled"
        order.save()
        return super().post(request, *args, **kwargs)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for a user to delete their own order.
    WARNING: In a real application, you should almost NEVER delete orders.
    Prefer changing the status to 'Cancelled' or 'Archived'.
    """

    model = Order
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
