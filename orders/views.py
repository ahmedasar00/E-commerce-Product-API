from users.models import Address


from django.db import transaction
from django.urls import reverse_lazy
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
    ...

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
    View to create a new order.
    NOTE: This is a highly simplified example for educational purposes.
    A real e-commerce 'create order' process is complex and should be handled
    by a checkout flow, similar to the logic in our API's perform_create.
    """

    model = Order
    template_name = "orders/order_form.html"
    fields = ["address"]
    success_url = reverse_lazy("order_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["address"].queryset = self.request.user.address_set.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.total_amount = 0
        form.instance.status = "Pending"
        return super().form_valid(form)

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
        if order.status != "Pending":
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
