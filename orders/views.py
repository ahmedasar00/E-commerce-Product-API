from users.models import Address


from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect

from rest_framework import viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order, OrderItem

from .serializers import OrderSerializer, OrderCreateSerializer
from .permissions import IsOwnerOrAdmin
from products.models import Product


# -----------------------------------------------------------------------------
# API Views (using Django REST Framework)
# -----------------------------------------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    # ... (Code remains the same) ...
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
                address=address,
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
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = "orders/order_form.html"
    fields = ["address"]

    def dispatch(self, request, *args, **kwargs):
        """
        This method runs before any other in the view. It checks if the user
        has any addresses. If not, it redirects them to the add-address page.
        """
        if not request.user.address_set.exists():
            # Redirect to the add address page, passing a 'next' parameter
            # to return the user here after successfully adding an address.
            return redirect(reverse("address_add") + "?next=" + reverse("order_create"))
        # If the user has addresses, proceed as normal.
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["address"].queryset = self.request.user.address_set.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.total_amount = 0
        form.instance.status = "Pending Payment"
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the payment page for the newly created order.
        return reverse("create_payment", kwargs={"order_id": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Create a New Order"
        return context


class OrderCancelView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = "orders/order_confirm_cancel.html"
    fields = []
    success_url = reverse_lazy("order_list")

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status not in ["Pending", "Pending Payment"]:
            return HttpResponseForbidden("This order cannot be cancelled.")

        order.status = "Cancelled"
        order.save()
        return super().post(request, *args, **kwargs)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
