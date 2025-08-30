from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Allows viewing OrderItems on the Order admin page.
    All fields are read-only to preserve order integrity.
    """

    model = OrderItem
    # Make all fields read-only. An admin should not change items of a placed order.
    readonly_fields = ("product", "quantity", "price_at_order_time")
    extra = 0  # Don't show extra forms for adding new items.
    can_delete = False  # Prevent deleting items from an order.

    def has_add_permission(self, request, obj=None):
        # Disable the ability to add new items from the inline view.
        return False


@admin.register(Order)  # Using the decorator is a cleaner way to register.
class OrderAdmin(admin.ModelAdmin):
    """
    Custom admin view for the Order model.
    """

    list_display = ("id", "user", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "user__email")
    inlines = [OrderItemInline]

    # Make critical fields read-only on the detail page.
    # The admin's main job here is to update the status.
    readonly_fields = ("user", "address", "total_amount", "created_at")

    # Organize the detail view fields.
    fieldsets = (
        ("Order Information", {"fields": ("id", "user", "status", "created_at")}),
        ("Shipping & Financials", {"fields": ("address", "total_amount")}),
    )

    # Add id to readonly_fields to show it but prevent editing
    readonly_fields = ("id", "user", "address", "total_amount", "created_at")

    def has_add_permission(self, request):
        # Prevent creating orders from the admin panel.
        # Order creation should go through the API to ensure all logic is applied.
        return False


# We no longer need admin.site.register(OrderItem) because it's handled by the inline.
